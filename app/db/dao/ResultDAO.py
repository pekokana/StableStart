from sqlalchemy.orm import Session
from app.db.schema import RaceResult

class ResultDAO:

    def create_result(self, db: Session, result: RaceResult):
        db.add(result)
        return result

    def get_results_by_race(self, db: Session, race_id: int, year: int):
        return (
            db.query(RaceResult)
            .filter(
                RaceResult.race_id == race_id,
                RaceResult.year == year
            )
            .all()
        )

    def get_results_by_horse(self, db: Session, horse_id: int):
        return (
            db.query(RaceResult)
            .filter(RaceResult.horse_id == horse_id)
            .all()
        )
    
    def get_results_by_year(self, db, year):
        return db.query(RaceResult).filter(
            RaceResult.year == year
        ).all()