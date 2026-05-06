from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey,
    Text, UniqueConstraint, Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ==============================
# 共通：時間管理
# ==============================
class TimeStampMixin:
    year = Column(Integer, index=True)
    month = Column(Integer)
    week = Column(Integer)


# ==============================
# コードマスタ
# ==============================
class CodeMaster(Base):
    __tablename__ = "code_master"

    code_type = Column(String, primary_key=True)
    code = Column(String, primary_key=True)
    value = Column(String)


class CodeTranslation(Base):
    __tablename__ = "code_translation"

    code_type = Column(String, primary_key=True)
    code = Column(String, primary_key=True)
    lang = Column(String, primary_key=True)

    label = Column(String)
    description = Column(Text)


# ==============================
# Trait
# ==============================
class Trait(Base):
    __tablename__ = "traits"

    trait_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True)

    category = Column(String)
    inherit_rate = Column(Float)
    mutation_rate = Column(Float)

    translations = relationship("TraitTranslation", back_populates="trait")


class TraitTranslation(Base):
    __tablename__ = "trait_translation"

    trait_id = Column(Integer, ForeignKey("traits.trait_id"), primary_key=True)
    lang = Column(String, primary_key=True)

    name = Column(String)
    description = Column(Text)

    trait = relationship("Trait", back_populates="translations")


# ==============================
# 国
# ==============================
class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    climate = Column(String)
    track_bias = Column(String)

    owners = relationship("Owner", back_populates="country")
    trainers = relationship("Trainer", back_populates="country")


# ==============================
# オーナー
# ==============================
class Owner(Base):
    __tablename__ = "owners"

    owner_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String)
    ideology = Column(String)
    ideology_strength = Column(Float)

    money = Column(Float)

    country_id = Column(Integer, ForeignKey("countries.country_id"))

    country = relationship("Country", back_populates="owners")
    horses = relationship("Horse", back_populates="owner")


# ==============================
# 調教師
# ==============================
class Trainer(Base):
    __tablename__ = "trainers"

    trainer_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String)

    skill = Column(String)
    personality = Column(String)

    reputation = Column(Float)

    age = Column(Integer)
    retire_age = Column(Integer)

    country_id = Column(Integer, ForeignKey("countries.country_id"))

    country = relationship("Country", back_populates="trainers")
    horses = relationship("Horse", back_populates="trainer")


# ==============================
# 馬
# ==============================
class Horse(Base):
    __tablename__ = "horses"

    horse_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, index=True)

    birth_year = Column(Integer, index=True)

    sex = Column(String)   # male / female
    color = Column(String)

    speed = Column(Float)
    stamina = Column(Float)

    father_id = Column(Integer, ForeignKey("horses.horse_id"))
    mother_id = Column(Integer, ForeignKey("horses.horse_id"))

    owner_id = Column(Integer, ForeignKey("owners.owner_id"))
    trainer_id = Column(Integer, ForeignKey("trainers.trainer_id"))

    status = Column(String)

    # 自己参照
    father = relationship("Horse", remote_side=[horse_id], foreign_keys=[father_id])
    mother = relationship("Horse", remote_side=[horse_id], foreign_keys=[mother_id])

    owner = relationship("Owner", back_populates="horses")
    trainer = relationship("Trainer", back_populates="horses")

    traits = relationship("HorseTrait", back_populates="horse")
    results = relationship("RaceResult", back_populates="horse")

    # 最終出走レース情報
    last_race_year = Column(Integer)
    last_race_month = Column(Integer)
    last_race_week = Column(Integer)

    fatigue = Column(Float, default=0.0)
    health = Column(Float, default=1.0)

    mental = Column(Float)  # 0〜1
    temper = Column(String)  # calm / normal / aggressive / fragile

    # スタート特性
    start_skill = Column(Float)
    # 折り合い
    control = Column(Float)

    # 走行スタイル
    running_style = Column(String)  # escape / front / stalk / close / versatile

    # 脚質適性（0〜1）
    front_affinity = Column(Float)   # 前で競馬が得意
    back_affinity = Column(Float)    # 後方競馬が得意


# ==============================
# 血統（5代）
# ==============================
class Pedigree(Base):
    __tablename__ = "pedigrees"

    horse_id = Column(Integer, ForeignKey("horses.horse_id"), primary_key=True)
    ancestor_id = Column(Integer, ForeignKey("horses.horse_id"), primary_key=True)

    generation = Column(Integer)  # 1〜5

    __table_args__ = (
        Index("idx_pedigree_horse", "horse_id"),
    )


# ==============================
# Trait紐付け
# ==============================
class HorseTrait(Base):
    __tablename__ = "horse_traits"

    horse_id = Column(Integer, ForeignKey("horses.horse_id"), primary_key=True)
    trait_id = Column(Integer, ForeignKey("traits.trait_id"), primary_key=True)

    strength = Column(Float)

    horse = relationship("Horse", back_populates="traits")
    trait = relationship("Trait")


class TrainerTrait(Base):
    __tablename__ = "trainer_traits"

    trainer_id = Column(Integer, ForeignKey("trainers.trainer_id"), primary_key=True)
    trait_id = Column(Integer, ForeignKey("traits.trait_id"), primary_key=True)

    value = Column(Float)


class OwnerTrait(Base):
    __tablename__ = "owner_traits"

    owner_id = Column(Integer, ForeignKey("owners.owner_id"), primary_key=True)
    trait_id = Column(Integer, ForeignKey("traits.trait_id"), primary_key=True)

    value = Column(Float)


# ==============================
# レースマスタ
# ==============================
class Race(Base):
    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, index=True)

    country_id = Column(Integer, ForeignKey("countries.country_id"))

    grade = Column(String)

    distance = Column(Integer)

    surface = Column(String)
    turn = Column(String)
    slope = Column(String)

    results = relationship("RaceResult", back_populates="race")


# ==============================
# レース開催
# ==============================
class RaceCalendar(Base):
    __tablename__ = "race_calendar"

    race_id = Column(Integer, ForeignKey("races.race_id"), primary_key=True)

    year = Column(Integer, primary_key=True)
    month = Column(Integer, primary_key=True)
    week = Column(Integer, primary_key=True)


# ==============================
# レース結果（超重要拡張）
# ==============================
class RaceResult(Base):
    __tablename__ = "race_results"

    race_id = Column(Integer, ForeignKey("races.race_id"), primary_key=True)
    horse_id = Column(Integer, ForeignKey("horses.horse_id"), primary_key=True)

    year = Column(Integer, primary_key=True)  # ← 重要（履歴保持）
    month = Column(Integer, primary_key=True)
    week = Column(Integer, primary_key=True)

    rank = Column(Integer)
    time = Column(Float)
    prize = Column(Float)

    race = relationship("Race", back_populates="results")
    horse = relationship("Horse", back_populates="results")


# ==============================
# 歴史ログ
# ==============================
class HistoricalEvent(Base):
    __tablename__ = "historical_events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)

    year = Column(Integer, index=True)
    month = Column(Integer)
    week = Column(Integer)

    category = Column(String)
    description = Column(Text)


# ==============================
# 世代統計
# ==============================
class GenerationStat(Base):
    __tablename__ = "generation_stats"

    stat_id = Column(Integer, primary_key=True, autoincrement=True)

    year = Column(Integer, unique=True)

    avg_speed = Column(Float)
    avg_stamina = Column(Float)

    trend_distance = Column(Float)

    speed_ratio = Column(Float)
    stamina_ratio = Column(Float)
    balance_ratio = Column(Float)

# ==============================
# 出走登録
# ==============================
class RaceEntry(Base):
    __tablename__ = "race_entries"

    entry_id = Column(Integer, primary_key=True, autoincrement=True)

    race_id = Column(Integer, ForeignKey("races.race_id"), nullable=False)
    horse_id = Column(Integer, ForeignKey("horses.horse_id"), nullable=False)

    owner_id = Column(Integer, ForeignKey("owners.owner_id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.trainer_id"), nullable=False)

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)

    # 状態
    status = Column(String, default="entry", nullable=False)

    # 意思決定ログ
    expected_fitness = Column(Float)
    priority = Column(Float)

    # リスク
    risk = Column(Float)

    reason = Column(Text)

    horse = relationship("Horse")
    race = relationship("Race")

    __table_args__ = (
        UniqueConstraint(
            "race_id",
            "horse_id",
            "year",
            "month",
            "week",
            name="uq_entry"
        ),
    )

class GameState(Base):
    __tablename__ = "game_state"

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    week = Column(Integer)

class Snapshot(Base):
    __tablename__ = "snapshots"

    snapshot_id = Column(Integer, primary_key=True, autoincrement=True)

    year = Column(Integer)
    month = Column(Integer)
    week = Column(Integer)

    data = Column(Text)  # JSON保存