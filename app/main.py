from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from app.api.sim_api import router
from fastapi.responses import HTMLResponse
from app.services.query_service import (
    get_logs_service,
    get_horses_service
)
from contextlib import asynccontextmanager
from app.services.bootstrap_service import bootstrap
from app.core.templates import templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時
    bootstrap()
    yield
    # 終了時（今回は何もしない）

# APIルーターの設定
app = FastAPI(lifespan=lifespan)
app.include_router(router)
# 静的ファイルとテンプレートの設定
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

# ==========================
# ページルーティング
# ==========================
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/horses_page", response_class=HTMLResponse)
def horses_page(request: Request):
    data = get_horses_service()
    return templates.TemplateResponse("horses.html", {
        "request": request,
        "horses": data
    })

@app.get("/races_page", response_class=HTMLResponse)
def races_page(request: Request):
    return templates.TemplateResponse("races.html", {"request": request})


@app.get("/results_page", response_class=HTMLResponse)
def results_page(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})

@app.get("/logs", response_class=HTMLResponse)
def logs(request: Request):
    data = get_logs_service()
    return templates.TemplateResponse("logs.html", {
        "request": request,
        "logs": data
    })