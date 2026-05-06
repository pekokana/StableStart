from app.world.seed import create_seeds
from app.world.generator import WorldGenerator
from app.db.connection import SessionLocal
from app.db.seeder.world_seeder import WorldSeeder

def main():

    seeds = create_seeds("myworld", "2026-05-06")

    wg = WorldGenerator(seeds)
    world = wg.generate()

    db = SessionLocal()
    seeder = WorldSeeder(db)
    seeder.seed(world)

    print("World initialized!")

if __name__ == "__main__":
    main()