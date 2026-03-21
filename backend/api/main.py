from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from api.routes import tarot, iching, history, zhuge, daliuren

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="AI Tarot & IChing API", version="1.0.0", description="FastAPI Backend for AI Divination System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import tarot, iching, history, zhuge, daliuren, ws, admin

app.include_router(tarot.router)
app.include_router(iching.router)
app.include_router(history.router)
app.include_router(zhuge.router)
app.include_router(daliuren.router)
app.include_router(ws.router)
app.include_router(admin.router)

assets_dir = BASE_DIR / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

history_dir = BASE_DIR / "history" 
if history_dir.exists():
    app.mount("/history", StaticFiles(directory=str(history_dir)), name="history")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Tarot & IChing API. Visit /docs for more info."}

from pydantic import BaseModel
class SystemConfig(BaseModel):
    bgm_id: int
    profile: str
    language: str
    guide_name: str

@app.get("/api/system/config", response_model=SystemConfig)
def get_system_config():
    from core.config_manager import config_manager
    conf = config_manager.get()
    lang = getattr(conf, "language", "繁體中文")
    return SystemConfig(
        bgm_id=conf.app.get("bgm_id", 1),
        profile=config_manager.active_profile,
        language=lang,
        guide_name=conf.app.get("guide_name", "toby")
    )
