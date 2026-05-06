import json
from db.connection import SessionLocal
from db.models import Snapshot, Horse

def save_snapshot():
    db = SessionLocal()

    horses = db.query(Horse).all()

    data = [
        {
            "id": h.horse_id,
            "speed": h.speed,
            "stamina": h.stamina,
            "health": h.health,
        }
        for h in horses
    ]

    snap = Snapshot(
        year=1,
        month=1,
        week=1,
        data=json.dumps(data)
    )

    db.add(snap)
    db.commit()
    db.close()

    return {"status": "snapshot_saved"}