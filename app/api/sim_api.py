from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.simulation_service import (
    init_world_service,
    run_year_service,
    get_status_service
)
from app.services.query_service import (
    get_horses_service,
    get_races_service,
    get_results_service,
    get_year_stats_service,
    get_generation_stats,
    get_logs_service
)
from app.core.templates import templates
from app.db.connection import SessionLocal
from app.db.models import Horse


router = APIRouter()

@router.post("/init")
def init():
    return init_world_service()

@router.post("/run_year")
def run():
    return run_year_service()

@router.get("/status")
def status():
    return get_status_service()

@router.get("/horses", response_class=HTMLResponse)
def horses(request: Request):
    data = get_horses_service()
    return templates.TemplateResponse("horses.html", {
        "request": request,
        "horses": data
    })

@router.get("/races")
def races():
    return get_races_service()

@router.get("/results")
def results(year: int):
    return get_results_service(year)

@router.get("/stats/year/{year}")
def stats(year: int):
    return get_year_stats_service(year)

@router.get("/stats/generation")
def generation():
    return get_generation_stats()

@router.get("/logs")
def logs():
    return get_logs_service()

@router.get("/horse/{horse_id}/pedigree", response_class=HTMLResponse)
def pedigree(request: Request, horse_id: int):
    db = SessionLocal()
    horse = db.query(Horse).get(horse_id)
    db.close()

    return templates.TemplateResponse("pedigree.html", {
        "request": request,
        "horse": horse
    })
