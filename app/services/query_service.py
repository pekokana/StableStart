from app.db.connection import SessionLocal
from app.db.dao.HorseDAO import HorseDAO
from app.db.dao.RaceDAO import RaceDAO
from app.db.dao.ResultDAO import ResultDAO
from app.db.models import GenerationStat, HistoricalEvent

horse_dao = HorseDAO()
race_dao = RaceDAO()
result_dao = ResultDAO()


def get_horses_service():
    db = SessionLocal()
    horses = horse_dao.list_all(db)

    data = [
        {
            "id": h.horse_id,
            "name": h.name,
            "father": h.father.name if h.father else None,
            "mother": h.mother.name if h.mother else None,
            "speed": h.speed,
            "stamina": h.stamina,
            "style": h.running_style,
            "status": h.status
        }
        for h in horses
    ]
    db.close()
    return data

def get_races_service():
    db = SessionLocal()
    races = race_dao.list_all(db)

    data = [
        {
            "id": r.race_id,
            "name": r.name,
            "grade": r.grade,
            "distance": r.distance
        }
        for r in races
    ]
    db.close()
    return data


def get_results_service(year: int):
    db = SessionLocal()
    results = result_dao.get_results_by_year(db, year)

    data = [
        {
            "race_id": r.race_id,
            "horse_id": r.horse_id,
            "rank": r.rank,
            "prize": r.prize
        }
        for r in results
    ]
    db.close()
    return data

def get_year_stats_service(year: int):
    db = SessionLocal()
    results = result_dao.get_results_by_year(db, year)

    win_count = {}
    for r in results:
        if r.rank == 1:
            win_count[r.horse_id] = win_count.get(r.horse_id, 0) + 1

    db.close()
    return win_count

def get_generation_stats():
    db = SessionLocal()

    stats = db.query(GenerationStat).all()

    data = [
        {
            "year": s.year,
            "speed": s.avg_speed,
            "stamina": s.avg_stamina
        }
        for s in stats
    ]

    db.close()
    return data

def get_logs_service():
    db = SessionLocal()

    logs = db.query(HistoricalEvent)\
        .order_by(HistoricalEvent.year.desc(),
                  HistoricalEvent.month.desc(),
                  HistoricalEvent.week.desc())\
        .limit(100)\
        .all()

    data = [
        {
            "date": f"{l.year}/{l.month}/{l.week}",
            "text": l.description
        }
        for l in logs
    ]

    db.close()
    return data


