from app.db.models import RaceEntry

class RaceEntryDAO:

    def create_entry(self, db, entry):
        db.add(entry)

    def get_entries_by_race(self, db, race_id):
        return db.query(RaceEntry).filter_by(race_id=race_id).all()

    def get_active_entries(self, db, year, month, week):
        return db.query(RaceEntry).filter_by(
            year=year,
            month=month,
            week=week,
            status="entry"
        ).all()

    def get_active_entries_by_race(self, db, race_id, year, month, week):
        return (
            db.query(RaceEntry)
            .filter_by(
                race_id=race_id,
                year=year,
                month=month,
                week=week,
                status="entry"
            )
            .all()
        )