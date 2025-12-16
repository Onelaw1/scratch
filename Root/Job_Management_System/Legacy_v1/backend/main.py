from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import ai_commander, fairness_audit
from .database import engine, Base

# Create Tables (Auto-migrate for new schema)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Native Public HR System",
    description="The World's First AI-Driven Job Architect & Fairness Engine",
    version="3.0.0-Revolution"
)

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount The New Engines
app.include_router(ai_commander.router) # The generic "Job Architect"
app.include_router(fairness_audit.router) # The "Compliance Guard"

@app.get("/")
def read_root():
    return {
        "system": "AI-Native Public HR Platform",
        "status": "OPERATIONAL",
        "engines": ["AI Job Architect", "Fairness Audit", "NCS Integration"]
    }
