from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.init_db import init_db
from app.core.database import engine, SessionLocal

app = FastAPI(
    title="Inventory POS B2B System",
    description="A lightweight, POS-integrated inventory management system with B2B marketplace",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Inventory POS B2B System",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }

@app.on_event("startup")
async def startup_event():
    # Initialize database with sample data
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close() 