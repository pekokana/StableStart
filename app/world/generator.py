import random
import hashlib


# ==========================
# Seed生成
# ==========================
def make_seed(text: str) -> int:
    return int(hashlib.sha256(text.encode()).hexdigest(), 16) % (10**8)


def create_seeds(user_key: str, date: str):
    global_seed = make_seed(f"{user_key}_{date}")

    return {
        "global": global_seed,
        "country": make_seed(f"{global_seed}_country"),
        "owner": make_seed(f"{global_seed}_owner"),
        "trainer": make_seed(f"{global_seed}_trainer"),
        "horse": make_seed(f"{global_seed}_horse"),
    }


# ==========================
# WorldGenerator
# ==========================
class WorldGenerator:

    def __init__(self, seeds):
        self.seeds = seeds

    # ==========================
    # メイン生成
    # ==========================
    def generate(self):

        countries = self.generate_countries()

        for c in countries:
            c["horses"] = self.generate_horses(c)

        return {"countries": countries}

    # ==========================
    # 国
    # ==========================
    def generate_countries(self):

        templates = [
            {"name": "A", "speed_bias": 0.1, "stamina_bias": -0.05},
            {"name": "B", "speed_bias": -0.05, "stamina_bias": 0.1},
            {"name": "C", "speed_bias": 0.0, "stamina_bias": 0.0},
        ]

        countries = []

        for t in templates:
            country = {
                "name": t["name"],
                "traits": t,
                "owners": self.generate_owners(t["name"]),
                "trainers": self.generate_trainers(t["name"]),
                "horses": []
            }
            countries.append(country)

        return countries

    # ==========================
    # オーナー
    # ==========================
    def generate_owners(self, country_name):

        rng = random.Random(self.seeds["owner"] + hash(country_name))

        owners = []

        for i in range(8):
            owners.append({
                "name": f"{country_name}_Owner_{i}",
                "ideology": rng.choice(["trend", "anti", "spin"]),
                "money": rng.randint(500_000, 1_500_000)
            })

        return owners

    # ==========================
    # 調教師
    # ==========================
    def generate_trainers(self, country_name):

        rng = random.Random(self.seeds["trainer"] + hash(country_name))

        trainers = []

        for i in range(5):
            trainers.append({
                "name": f"{country_name}_Trainer_{i}",
                "skill": rng.choice(["bad", "normal", "god"]),
                "personality": rng.choice(["A", "B", "C", "D"])
            })

        return trainers

    # ==========================
    # 馬（最重要）
    # ==========================
    def generate_horses(self, country):

        rng = random.Random(self.seeds["horse"] + hash(country["name"]))

        horses = []

        for i in range(24):

            owner = rng.choice(country["owners"])
            trainer = rng.choice(country["trainers"])

            # --------------------------
            # 能力（simulation思想を反映）
            # --------------------------
            base_speed = rng.uniform(0.4, 0.6)
            base_stamina = rng.uniform(0.4, 0.6)

            speed = base_speed + country["traits"]["speed_bias"]
            stamina = base_stamina + country["traits"]["stamina_bias"]

            # --------------------------
            # 追加パラメータ（Simulation用）
            # --------------------------
            horse = {
                "name": f"{country['name']}_Horse_{i}",

                "speed": max(0, min(1, speed)),
                "stamina": max(0, min(1, stamina)),

                # SimulationEngineで使う要素
                "fatigue": rng.uniform(0, 0.1),
                "health": rng.uniform(0.7, 1.0),
                "mental": rng.uniform(0.5, 1.0),

                "temper": rng.choice(["normal", "aggressive", "fragile"]),

                "running_style": rng.choice(
                    ["escape", "front", "stalk", "close", "versatile"]
                ),

                "front_affinity": rng.uniform(0.8, 1.2),
                "back_affinity": rng.uniform(0.8, 1.2),

                # 紐付け
                "owner": owner["name"],
                "trainer": trainer["name"],

                "sex": rng.choice(["male", "female"]),
            }

            horses.append(horse)

        return horses