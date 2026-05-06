from app.db.models import Race, RaceCalendar
import random

class RaceSeeder:

    def __init__(self, db, seed=42):
        self.db = db
        self.rng = random.Random(seed)

    def seed(self, countries):

        for country in countries:

            races = self._create_races(country)
            self._create_calendar(races)

        self.db.commit()

    # ==========================
    # レース生成
    # ==========================
    def _create_races(self, country):

        races = []

        templates = [
            ("G1", 2400),
            ("G2", 2000),
            ("G3", 1600),
            ("G3", 1200),
        ]

        for i in range(12):  # 月1本ペース

            grade, distance = self.rng.choice(templates)

            race = Race(
                name=f"{country.name}_Race_{i}",

                country_id=country.country_id,

                grade=grade,

                distance=distance,

                surface="turf",
                turn=self.rng.choice(["left", "right"]),
                slope=self.rng.choice(["flat", "slope"])
            )

            self.db.add(race)
            self.db.flush()

            races.append(race)

        return races

    # ==========================
    # カレンダー生成
    # ==========================
    def _create_calendar(self, races):

        for i, race in enumerate(races):

            # 月固定開催
            month = i + 1

            # G1は月末
            if race.grade == "G1":
                weeks = [4]

            # G2は中盤
            elif race.grade == "G2":
                weeks = [2, 3]

            # G3は分散
            else:
                weeks = [self.rng.randint(1, 4)]

            for w in weeks:
                cal = RaceCalendar(
                    race_id=race.race_id,
                    year=1,
                    month=month,
                    week=w
                )
                self.db.add(cal)