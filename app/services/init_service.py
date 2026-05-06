from app.db.connection import SessionLocal
from app.db.init_db import init_db
from app.db.seeder.world_seeder import WorldSeeder
from app.db.seeder.race_seeder import RaceSeeder
from app.world.generator import create_seeds, WorldGenerator
from app.db.models import Country

def init_world():

    init_db()

    db = SessionLocal()

    # ワールド生成
    seeds = create_seeds("myworld", "2026-05-06")
    wg = WorldGenerator(seeds)
    world = wg.generate()

    # DB投入
    WorldSeeder(db).seed(world)

    # レース生成
    countries = db.query(Country).all()
    RaceSeeder(db).seed(countries)

    db.close()

    return {"status": "initialized"}