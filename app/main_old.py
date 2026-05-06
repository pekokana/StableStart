from world.generator import create_seeds, WorldGenerator
from db.connection import SessionLocal
from db.init_db import init_db
from db.seeder.world_seeder import WorldSeeder
from db.seeder.race_seeder import RaceSeeder

def main():

    # ① DB初期化
    init_db()

    db = SessionLocal()

    # ② 世界生成
    seeds = create_seeds("myworld", "2026-05-06")
    wg = WorldGenerator(seeds)
    world = wg.generate()

    # ③ DB投入
    ws = WorldSeeder(db)
    ws.seed(world)

    # ④ レース生成
    countries = db.query(Country).all()
    rs = RaceSeeder(db)
    rs.seed(countries)

    db.close()

if __name__ == "__main__":
    main()