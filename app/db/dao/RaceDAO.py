from sqlalchemy.orm import Session
from app.db.schema import Race, RaceCalendar

class RaceDAO:

    def create_race(self, db: Session, race: Race):
        db.add(race)
        return race

    def get_race(self, db: Session, race_id: int):
        return db.query(Race).filter(Race.race_id == race_id).first()

    def list_by_country(self, db: Session, country_id: int):
        return db.query(Race).filter(Race.country_id == country_id).all()

    def add_calendar(self, db: Session, calendar: RaceCalendar):
        db.add(calendar)
        return calendar

    def get_races_by_date(self, db: Session, year: int, month: int, week: int):
        return (
            db.query(Race)
            .join(RaceCalendar)
            .filter(
                RaceCalendar.year == year,
                RaceCalendar.month == month,
                RaceCalendar.week == week
            )
            .all()
        )
    
    def list_all(self, db):
        return db.query(Race).all()