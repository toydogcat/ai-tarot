from dotenv import load_dotenv
load_dotenv(override=True)
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from api.routes import tarot, iching, history, zhuge, daliuren

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="AI Tarot & IChing API", version="1.0.0", description="FastAPI Backend for AI Divination System")

@app.on_event("startup")
def startup_event():
    from core.tasks import start_scheduler
    from core.firebase_config import init_firebase
    start_scheduler()
    init_firebase()

@app.on_event("shutdown")
def shutdown_event():
    from core.tasks import shutdown_scheduler
    shutdown_scheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|ai-factory-tarot\.web\.app|ai-factory-tarot\.firebaseapp\.com)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import tarot, iching, history, zhuge, daliuren, xiaoliuren, ws, admin, auth, social

app.include_router(tarot.router)
app.include_router(iching.router)
app.include_router(history.router)
app.include_router(zhuge.router)
app.include_router(xiaoliuren.router)
app.include_router(daliuren.router)
app.include_router(ws.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(social.router)

assets_dir = BASE_DIR / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

history_dir = BASE_DIR / "history" 
if history_dir.exists():
    app.mount("/history", StaticFiles(directory=str(history_dir)), name="history")

from pydantic import BaseModel
class SystemConfig(BaseModel):
    bgm_id: int
    profile: str
    language: str
    guide_name: str
    enable_multiuser_login: bool
    usage_limit: int
    google_client_id: str | None = None

@app.get("/api/system/config", response_model=SystemConfig)
def get_system_config():
    from core.config_manager import config_manager
    conf = config_manager.get()
    lang = getattr(conf, "language", "繁體中文")
    return SystemConfig(
        bgm_id=conf.app.get("bgm_id", 1),
        profile=config_manager.active_profile,
        language=lang,
        guide_name=conf.app.get("guide_name", "toby"),
        enable_multiuser_login=conf.app.get("enable_multiuser_login", False),
        usage_limit=config_manager.get_remaining_usage(),
        google_client_id=os.getenv("GOOGLE_CLIENT_ID")
    )

@app.get("/api/config/keys")
def get_config_keys():
    import os
    # Return Gemini Key for Page-Agent frontend
    return {"gemini_key": os.getenv("GEMINI_API_KEY") or ""}

frontend_dir = BASE_DIR.parent / "frontend" / "dist"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
else:
    @app.get("/")
    def read_root():
        return {"message": "Welcome to AI Tarot & IChing API. Frontend build not found."}

