from app.db.connection import SessionLocal
from app.core.simulation_engine import SimulationEngine
from app.services.init_service import init_world
from app.db.models import GameState

def init_world_service():
    init_world()
    return {"status": "initialized"}

# ==========================
# 状態保存
# ==========================
def save_state(db, engine):
    state = db.query(GameState).first()

    if not state:
        state = GameState()
        db.add(state)

    state.year = engine.year
    state.month = engine.month
    state.week = engine.week

def load_state(db, engine):
    state = db.query(GameState).first()

    if state:
        engine.year = state.year
        engine.month = state.month
        engine.week = state.week

# ==========================
# 実行
# ==========================
def run_year_service():
    db = SessionLocal()

    engine = SimulationEngine(db)
    load_state(db, engine)

    engine.run_one_year()

    save_state(db, engine)
    db.commit()

    result = {
        "year": engine.year,
        "month": engine.month,
        "week": engine.week
    }

    db.close()
    return result

# ==========================
# ステータス
# ==========================
def get_status_service():
    db = SessionLocal()

    state = db.query(GameState).first()

    if not state:
        db.close()
        return {"year": 1, "month": 1, "week": 1}

    result = {
        "year": state.year,
        "month": state.month,
        "week": state.week
    }

    db.close()
    return result