from sqlalchemy.orm import Session
from app.db.schema import Horse

class HorseDAO:

    def create(self, db: Session, horse: Horse):
        db.add(horse)
        return horse

    def get(self, db: Session, horse_id: int):
        return db.query(Horse).filter(Horse.horse_id == horse_id).first()

    def list_by_owner(self, db: Session, owner_id: int):
        return db.query(Horse).filter(Horse.owner_id == owner_id).all()

    def list_active(self, db: Session):
        return db.query(Horse).filter(Horse.status == "active").all()

    def retire(self, db: Session, horse: Horse, status: str):
        horse.status = status
        return horse
    
    def list_all(self, db):
        return db.query(Horse).all()