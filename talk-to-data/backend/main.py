from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.chatbot_controller import router as chatbot_router
from .rag.vector_store import build_vectorstore
from .utils.config import settings


app = FastAPI(
    title="Library RAG Backend",
    description="Auto-schema RAG + SQL Generation + FastAPI backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Startup Event: Rebuild schema + vectorstore automatically
@app.on_event("startup")
async def startup_event():
    print("🔄 Server starting...")

    if settings.RELOAD_VECTORSTORE:
        print("📚 Regenerating schema + rebuilding vectorstore...")
        build_vectorstore()
        print("✅ Vectorstore and schema generated.")
    else:
        print("⚠️ Vectorstore rebuild disabled in config.ini")


# ✅ Register chatbot endpoint
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])


@app.get("/")
async def root():
    return {
        "status": "✅ Library RAG Backend Running",
        "info": "Use POST /chatbot/ask to query system",
        "rag_status": "Auto-schema + RAG enabled"
    }
