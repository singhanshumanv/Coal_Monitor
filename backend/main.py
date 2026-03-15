from fastapi import FastAPI
from routes.compliance import router as compliance_router
from database import engine
from models.base import Base
from models.project import Project
from fastapi.middleware.cors import CORSMiddleware
from models.task import Task
from models.report import Report


Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Compliance Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compliance_router)

@app.get("/")
def home():
    return {"message": "AI Compliance Platform Running"}