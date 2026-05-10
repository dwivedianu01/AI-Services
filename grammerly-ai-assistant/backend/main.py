from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.grammerly_controller import router as grammerly_router
from utils.config import settings

app = FastAPI(
    title="Grammerly AI Text Assistant API",
    version="1.0.0",
    description="AI-powered text cleaning and formatting using OpenAI with markdown instructions.",
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
    return {
        "status": "ok",
        "environment": settings.ENV,
        "ai_enabled": settings.OPENAI_ENABLED,
    }


app.include_router(grammerly_router)

@app.get("/api/health")
def health_api():
    # Expose a lightweight health endpoint for frontend health checks
    return {
        "status": "ok",
        "environment": settings.ENV,
        "ai_enabled": settings.OPENAI_ENABLED,
    }
