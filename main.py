from dotenv import load_dotenv
from fastapi import FastAPI
import os
from src.routers.auth import router as auth_router
from src.routers.student import router as student_router
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import engine, Base

# Create tables that don't already exist
Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(student_router)

@app.get("/")
def root():
    return {
        "message": "AstraX backend running"
    }