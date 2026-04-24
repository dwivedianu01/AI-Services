from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.resume_controller import router as resume_router
from .utils.config import settings
from .utils.database import get_database_status


from .routes.jobs_controller import router as jobs_router

app = FastAPI(
    title="Resume Analyzer API",
    version="1.0.0",
    description="Upload a resume and compare it against a target role.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    database_status = get_database_status()
    return {
        "status": "ok",
        "environment": settings.ENV,
        "ai_enabled": settings.OPENAI_ENABLED,
        "database": database_status,
    }


app.include_router(resume_router)
app.include_router(jobs_router)

@app.get("/api/health")
def health_api():
    # Expose a lightweight health endpoint for frontend health checks
    database_status = get_database_status()
    return {
        "status": "ok",
        "environment": settings.ENV,
        "ai_enabled": settings.OPENAI_ENABLED,
        "database": database_status,
    }
