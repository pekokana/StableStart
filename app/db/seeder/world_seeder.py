from app.db.models import Country, Owner, Trainer, Horse, Pedigree
import random

class WorldSeeder:

    def __init__(self, db):
        self.db = db

    def seed(self, world):

        for c in world["countries"]:

            # --------------------------
            # 国
            # --------------------------                
            country = Country(
                name=c["name"],
                climate="temperate",
                track_bias="normal"
            )
            self.db.add(country)
            self.db.flush()

            # --------------------------
            # オーナー
            # --------------------------
            owner_map = {}
            for o in c["owners"]:
                owner = Owner(
                    name=o["name"],
                    ideology=o["ideology"],
                    ideology_strength=0.5,
                    money=o["money"],
                    country_id=country.country_id
                )
                self.db.add(owner)
                self.db.flush()
                owner_map[o["name"]] = owner.owner_id

            # --------------------------
            # 調教師
            # --------------------------
            trainer_map = {}
            for t in c["trainers"]:
                trainer = Trainer(
                    name=t["name"],
                    skill=t["skill"],
                    personality=t["personality"],
                    reputation=0.5,
                    age=35,
                    retire_age=65,
                    country_id=country.country_id
                )
                self.db.add(trainer)
                self.db.flush()
                trainer_map[t["name"]] = trainer.trainer_id

            # --------------------------
            # 馬
            # --------------------------
            for h in c["horses"]:

                # 親をランダム選択（簡易）
                father = None
                mother = None

                if len(self.db.query(Horse).all()) > 2:
                    parents = random.sample(self.db.query(Horse).all(), 2)
                    father = parents[0]
                    mother = parents[1]

                horse = Horse(
                    name=h["name"],
                    birth_year=1,
                    sex=h["sex"],
                    color="bay",

                    speed=h["speed"],
                    stamina=h["stamina"],
                    health=h["health"],

                    fatigue=h["fatigue"],
                    mental=h["mental"],
                    temper=h["temper"],

                    running_style=h["running_style"],
                    front_affinity=h["front_affinity"],
                    back_affinity=h["back_affinity"],

                    owner_id=owner_map[h["owner"]],
                    trainer_id=trainer_map[h["trainer"]],

                    father_id=father.horse_id if father else None,
                    mother_id=mother.horse_id if mother else None,

                    status="active"
                )

                self.db.add(horse)

        self.db.commit()