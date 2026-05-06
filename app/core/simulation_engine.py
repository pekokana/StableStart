from app.db.connection import SessionLocal
from app.db.models import RaceResult, RaceEntry, GenerationStat, HistoricalEvent
from app.db.dao.HorseDAO import HorseDAO
from app.db.dao.RaceDAO import RaceDAO
from app.db.dao.ResultDAO import ResultDAO
from app.db.dao.RaceEntryDAO import RaceEntryDAO
from app.utils.time_utils import calc_week_diff
import random

class SimulationEngine:

    def __init__(self, db):
        self.db = db

        self.horse_dao = HorseDAO()
        self.race_dao = RaceDAO()
        self.result_dao = ResultDAO()
        self.entry_dao = RaceEntryDAO()

        self.year = 1
        self.month = 1
        self.week = 1

        # 年間統計バッファ
        self.style_stats = {
            "escape": [],
            "front": [],
            "stalk": [],
            "close": [],
            "versatile": []
        }

    # ==========================
    # メインループ
    # ==========================
    def run(self, years=10):
        for _ in range(years):
            self.run_year()

    # ==========================
    # 年間処理
    # ==========================
    def run_year(self):
        for m in range(1, 13):
            for w in range(1, 5):
                self.month = m
                self.week = w

                self.run_week()

        self.end_of_year()
        self.year += 1

    def run_one_year(self):
        self.run_year()
        return {
            "year": self.year
        }

    def get_status(self):

        return {
            "year": self.year,
            "month": self.month,
            "week": self.week
        }

    # ==========================
    # 週処理
    # ==========================
    def run_week(self):

        # ① 調教
        self.training_phase()

        # ②レース登録
        self.entry_phase()

        # ③レース開催
        self.race_phase()

        # ④ イベント（事故・引退など）
        self.event_phase()

        self.db.commit()

    # ==========================
    # 調教
    # ==========================
    def training_phase(self):
        horses = self.horse_dao.list_active(self.db)

        for h in horses:
            h.speed += 0.01
            h.stamina += 0.01
            h.fatigue += 0.05
            h.health -= 0.01

    # ==========================
    # レース
    # ==========================
    def race_phase(self):

        races = self.race_dao.get_races_by_date(
            self.db,
            self.year,
            self.month,
            self.week
        )

        for race in races:

            entries = self.entry_dao.get_active_entries_by_race(
                self.db,
                race.race_id,
                self.year,
                self.month,
                self.week
            )

            if len(entries) < 2:
                continue

            self.run_race(race)

    def run_race(self, race):

        entries = self.entry_dao.get_active_entries_by_race(
            self.db,
            race.race_id,
            self.year,
            self.month,
            self.week
        )

        horses = [e.horse for e in entries]

        # ==========================
        # ペース決定
        # ==========================
        pace = self.determine_pace(horses)
        print(f"{self.year}/{self.month}/{self.week} {race.name} pace={pace}")
        scored = []

        # 逃げ馬の競り合い
        escapes = [h for h in horses if h.running_style == "escape"]

        if len(escapes) >= 2:
            for h in escapes:
                # 競り合って消耗
                h.fatigue += 0.1

        for horse in horses:

            # --------------------------
            # 基本能力
            # --------------------------
            fitness = (
                0.5 * horse.speed +
                horse.stamina * (race.distance / 2400)
            )

            # 血統を少し反映
            fitness += self.pedigree_bonus(horse)

            injury_risk = horse.fatigue * (1 - horse.health)

            # --------------------------
            # 脚質補正
            # --------------------------
            style_bonus = self.apply_style_bonus(horse, pace)
            fitness += style_bonus

            # ==========================
            # 気性
            # ==========================

            # スタート失敗
            if random.random() > horse.mental:
                fitness *= 0.8

            # 気性タイプ
            if horse.temper == "aggressive":
                fitness *= random.uniform(0.9, 1.2)

            elif horse.temper == "fragile":
                injury_risk *= 1.5
            
            # 万能型の扱い
            if horse.running_style == "versatile":
                fitness += 0.1  # 安定補正

            # 逃げ × 気性
            if horse.running_style == "escape" and horse.temper == "aggressive":
                fitness *= 1.1  # ハマると爆発

            # 差し × fragile
            if horse.running_style == "close" and horse.temper == "fragile":
                fitness *= 0.9  # メンタル負け

            # レース中イベント
            fitness = self.apply_race_events(horse, fitness)

            # --------------------------
            # 故障イベント
            # --------------------------
            if injury_risk > 0.5 and random.random() < injury_risk:
                horse.status = "dead"
                continue  # レース脱落

            scored.append((horse, fitness))


        # --------------------------
        # ランキング
        # --------------------------
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)

        for i, (horse, _) in enumerate(ranked):

            result = RaceResult(
                race_id=race.race_id,
                horse_id=horse.horse_id,
                year=self.year,
                month=self.month,
                week=self.week,
                rank=i+1,
                time=100 - i,
                prize=10000 if i == 0 else 0
            )

            self.db.add(result)

            # 更新
            horse.last_race_year = self.year
            horse.last_race_month = self.month
            horse.last_race_week = self.week

            horse.fatigue += 0.2
            horse.health -= 0.02

            # ログ追加
            event = HistoricalEvent(
                year=self.year,
                month=self.month,
                week=self.week,
                category="race",
                description=f"{race.name}: {i+1}位 {horse.name}"
            )
            self.db.add(event)

        # --------------------------
        # 脚質×結果ログ
        # --------------------------
        style_result = {
            "escape": [],
            "front": [],
            "stalk": [],
            "close": [],
            "versatile": []
        }

        for i, (horse, _) in enumerate(ranked):
            style_result[horse.running_style].append(i+1)

        # 年間バッファに追加
        for style, ranks in style_result.items():
            self.style_stats[style].extend(ranks)

    # ==========================
    # レース中ランダムイベント
    # ==========================
    def apply_race_events(self, horse, fitness):

        if random.random() < 0.05:
            fitness *= random.uniform(0.7, 1.1)
        
        # 不利
        if random.random() < 0.05:
            fitness *= 0.85
        
        # 神騎乗
        if random.random() < 0.03:
            fitness *= 1.1

        # 暴走（気性悪い）
        if horse.temper == "aggressive" and random.random() < 0.1:
            fitness *= 0.8

        # 位置取り
        if horse.running_style in ["escape", "front"]:
            fitness *= 0.98  # 消耗
        else:
            fitness *= 1.02  # 末脚

        return fitness


    def pedigree_bonus(self, horse):
        bonus = 0
        if horse.father:
            bonus += horse.father.speed * 0.1
            bonus += horse.father.stamina * 0.1
        if horse.mother:
            bonus += horse.mother.speed * 0.1
            bonus += horse.mother.stamina * 0.1
        return bonus

    # ==========================
    # イベント
    # ==========================
    def event_phase(self):
        horses = self.horse_dao.list_active(self.db)

        for h in horses:
            if h.health < 0.2:
                self.horse_dao.retire(self.db, h, "dead")

    # ==========================
    # 年末処理（超重要）
    # ==========================
    def end_of_year(self):

        print(f"{self.year}年終了")

        # --------------------------
        # 脚質バランス分析
        # --------------------------
        if hasattr(self, "style_stats"):
            print("=== 脚質別平均着順 ===")

            for style, ranks in self.style_stats.items():
                if ranks:
                    avg = sum(ranks) / len(ranks)
                    print(f"{style}: avg_rank={avg:.2f} (n={len(ranks)})")

        # ★ 次の年のためにリセット
        self.style_stats = {
            "escape": [],
            "front": [],
            "stalk": [],
            "close": [],
            "versatile": []
        }

        horses = self.horse_dao.list_active(self.db)

        avg_speed = sum(h.speed for h in horses) / len(horses)
        avg_stamina = sum(h.stamina for h in horses) / len(horses)

        stat = GenerationStat(
            year=self.year,
            avg_speed=avg_speed,
            avg_stamina=avg_stamina,
            trend_distance=0,
            speed_ratio=0,
            stamina_ratio=0,
            balance_ratio=0
        )

        self.db.add(stat)

    # ==========================
    # 出走条件
    # ==========================
    def can_run(self, horse, current_year, current_month, current_week):
        if horse.last_race_year is None:
            return True

        diff = (current_year - horse.last_race_year) * 48 + \
            (current_month - horse.last_race_month) * 4 + \
            (current_week - horse.last_race_week)

        return diff >= 4  # 4週空ける

    # ==========================
    # 出走登録
    # ==========================
    def register_entries(self, race):

        horses = self.horse_dao.list_active(self.db)

        candidates = [
            h for h in horses
            if self.can_run(h, self.year, self.month, self.week)
        ]

        import random
        selected = random.sample(candidates, k=min(10, len(candidates)))

        for h in selected:
            entry = RaceEntry(
                race_id=race.race_id,
                horse_id=h.horse_id,
                owner_id=h.owner_id,
                trainer_id=h.trainer_id,
                year=self.year,
                month=self.month,
                week=self.week,
                status="entry"
            )
            self.entry_dao.create_entry(self.db, entry)


    # ==========================
    # 休養出走
    # ==========================
    def decide_race_entry(self, db, horse, races):

        owner = horse.owner
        trainer = horse.trainer

        candidates = []

        for race in races:

            # --------------------------
            # 適性
            # --------------------------
            fitness = (
                0.5 * horse.speed +
                horse.stamina * (race.distance / 2400)
            )

            # --------------------------
            # 疲労リスク
            # --------------------------
            fatigue_penalty = horse.fatigue

            # --------------------------
            # 連闘ペナルティ（固定ではない）
            # --------------------------
            gap_penalty = 0

            if horse.last_race_week is not None:
                gap = calc_week_diff(
                    horse.last_race_year,
                    horse.last_race_month,
                    horse.last_race_week,
                    race.year,
                    race.month,
                    race.week
                )

                # 調教師の性格で変える
                if trainer.personality == "A":  # 安全派
                    if gap < 4:
                        gap_penalty = 0.3

                elif trainer.personality == "B":  # 攻め
                    if gap < 2:
                        gap_penalty = 0.1

                elif trainer.personality == "C":  # ランダム
                    gap_penalty = random.uniform(0, 0.2)

            # --------------------------
            # オーナー思想
            # --------------------------
            if owner.ideology == "trend":
                bonus = fitness * 0.2

            elif owner.ideology == "anti":
                bonus = (1 - fitness) * 0.2

            elif owner.ideology == "spin":
                bonus = random.uniform(0, 0.3)

            else:
                bonus = 0

            # --------------------------
            # 総合スコア
            # --------------------------
            score = fitness + bonus - fatigue_penalty - gap_penalty

            candidates.append((race, score, fitness, gap_penalty))

        if not candidates:
            return None

        best = max(candidates, key=lambda x: x[1])

        return best


    def entry_phase(self):

        races = self.race_dao.get_races_by_date(
            self.db,
            self.year,
            self.month,
            self.week
        )

        horses = self.horse_dao.list_active(self.db)

        for horse in horses:

            action, race, score = self.decide_action(horse, races)

            if action == "rest":
                # 休養処理
                horse.fatigue *= 0.5
                horse.health += 0.05
                horse.health = min(1.0, horse.health)
                continue

            entry = RaceEntry(
                race_id=race.race_id,
                horse_id=horse.horse_id,
                owner_id=horse.owner_id,
                trainer_id=horse.trainer_id,
                year=self.year,
                month=self.month,
                week=self.week,
                status="entry",
                priority=score
            )

            self.db.add(entry)

    def decide_action(self, horse, races):

        candidates = []

        # --------------------------
        # レース候補
        # --------------------------
        for race in races:
            score = self.evaluate_race(horse, race)
            candidates.append(("race", race, score))

        # --------------------------
        # 休養（超重要）
        # --------------------------
        rest_score = self.evaluate_rest(horse)
        candidates.append(("rest", None, rest_score))
        

        return max(candidates, key=lambda x: x[2])

    def evaluate_rest(self, horse):

        # 疲労が高いほど休養したくなる
        fatigue_factor = horse.fatigue * 0.8

        # 健康が低いほど休養優先
        health_factor = (1 - horse.health) * 0.5

        return fatigue_factor + health_factor

    # --------------------------
    # 故障イベント
    # --------------------------
    def injury_event(self, horse):

        risk = horse.fatigue * (1 - horse.health)

        if risk > 0.5 and random.random() < risk:
            horse.status = "retired"
            return True

        return False

    # --------------------------
    # 格補正
    # --------------------------
    def grade_bonus(self, owner, trainer, race):

        if race.grade == "G1":
            base = 0.3
        elif race.grade == "G2":
            base = 0.2
        elif race.grade == "G3":
            base = 0.1
        else:
            base = 0.05

        # オーナー思想
        if owner.ideology == "trend":
            return base * 1.5  # ビッグレース大好き

        elif owner.ideology == "anti":
            return base * 0.5  # あえて避ける

        elif owner.ideology == "spin":
            return random.uniform(0, base * 2)

        return base

    # --------------------------
    # 総合評価
    # --------------------------
    def evaluate_race(horse, race):

        owner = horse.owner
        trainer = horse.trainer

        # --------------------------
        # 適性
        # --------------------------
        fitness = (
            0.5 * horse.speed +
            horse.stamina * (race.distance / 2400)
        )

        # --------------------------
        # 疲労ペナルティ
        # --------------------------
        fatigue_penalty = horse.fatigue * 0.5

        # --------------------------
        # 故障リスク
        # --------------------------
        injury_risk = horse.fatigue * (1 - horse.health)

        # --------------------------
        # レース格
        # --------------------------
        grade = self.grade_bonus(owner, trainer, race)


        # 目標レース補正
        target_bonus = 0
        if horse.target_race_id == race.race_id:
            target_bonus = 0.5
        # 気性（軽く影響）
        mental_penalty = (1 - horse.mental) * 0.2

        # --------------------------
        # 最終スコア
        # --------------------------
        score = fitness + grade + target_bonus - fatigue_penalty - injury_risk

        return score

    # --------------------------
    # ペース判定
    # --------------------------
    def determine_pace(self, horses):

        front_count = sum(
            1 for h in horses if h.running_style in ["escape", "front"]
        )

        if front_count >= 5:
            return "high"   # ハイペース
        elif front_count <= 2:
            return "slow"   # スローペース
        else:
            return "mid"

    # --------------------------
    # 脚質 × ペース補正
    # --------------------------
    def apply_style_bonus(self, horse, pace):

        bonus = 0

        if pace == "high":
            # ハイペース → 差し有利
            if horse.running_style in ["stalk", "close"]:
                bonus += 0.2 * horse.back_affinity
            else:
                bonus -= 0.1

        elif pace == "slow":
            # スロー → 前有利
            if horse.running_style in ["escape", "front"]:
                bonus += 0.2 * horse.front_affinity
            else:
                bonus -= 0.1

        return bonus

