from app.db.connection import SessionLocal
from app.db.models import Horse
from app.services.init_service import init_world
from app.db.init_db import init_db

from sqlalchemy.exc import OperationalError
import subprocess

def bootstrap():
    # AlembicでDB最新化
    subprocess.run(["alembic", "upgrade", "head"])

    db = SessionLocal()

    try:
        has_data = db.query(Horse).count() > 0
    except OperationalError:
        # テーブルまだない → 初期化
        db.close()
        init_world()
        return

    db.close()

    if not has_data:
        init_world()
