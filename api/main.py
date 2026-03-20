from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import tarot, iching

app = FastAPI(title="AI Tarot & IChing API", version="1.0.0", description="FastAPI Backend for AI Divination System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tarot.router)
app.include_router(iching.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Tarot & IChing API. Visit /docs for more info."}
