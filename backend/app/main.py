from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import collector
from app.db.session import engine
from app.models.schemas import Base

# Create tables for SQLite (In production, use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LLM Agent Eval & Tracing Infrastructure")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(collector.router, prefix="/api", tags=["Tracing"])

@app.get("/")
async def root():
    return {"message": "LLM Tracing Infrastructure API"}
