from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import traceback
from typing import Optional

from utils.config import settings
try:
    from openai import OpenAI
    import openai
except Exception:  # pragma: no cover
    OpenAI = None
    openai = None


router = APIRouter(prefix="/grammerly", tags=["grammerly"])


class FixRequest(BaseModel):
    payload: str


def read_and_validate_instructions_md() -> str:
    base = os.path.join(os.path.dirname(__file__), os.pardir, "aois")
    instructions_path = os.path.abspath(os.path.join(base, "instructions.md"))
    try:
        with open(instructions_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No instructions available."


def openai_call(text: str) -> Optional[str]:
    if not settings.OPENAI_ENABLED:
        print(f"DEBUG: OPENAI_ENABLED = {settings.OPENAI_ENABLED}")
        print(f"DEBUG: OPENAI_API_KEY = {settings.OPENAI_API_KEY[:20]}..." if settings.OPENAI_API_KEY else "DEBUG: OPENAI_API_KEY is empty")
        return None
    if OpenAI is None:
        print("DEBUG: OpenAI class not available from openai package")
        return None

    try:
        instructions = read_and_validate_instructions_md()
        prompt = (
            "You are an AI assistant. Use the instructions from the markdown file to process the input text. "
            + "Instructions:\n"
            + instructions
            + "\n\nInput:\n"
            + text
            + "\n\nOutput:\n"
        )
        print(f"DEBUG: Calling OpenAI with model={settings.OPENAI_CHAT_MODEL}")

        client = OpenAI(**settings.OPENAI_CLIENT_KWARGS)
        response = client.chat.completions.create(
            model=settings.OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful text processor that follows the provided instructions."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=2048,
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"DEBUG: OpenAI call failed: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        return None


@router.post("/fix")
async def fix_content(req: FixRequest):
    payload = req.payload or ""
    if not payload.strip():
        raise HTTPException(status_code=400, detail="Payload text is required.")
    fixed = openai_call(payload)
    if fixed is None:
        raise HTTPException(
            status_code=503,
            detail="OpenAI is not configured or the model request failed. Ensure OPENAI_API_KEY is set and the OpenAI client is available."
        )

    return {
        "fixed": fixed.strip(),
        "notes": ["Processed by OpenAI using instructions from instructions.md."]
    }


@router.get("/debug")
async def debug_config():
    """Debug endpoint to check configuration status"""
    return {
        "openai_enabled": settings.OPENAI_ENABLED,
        "api_key_set": bool(settings.OPENAI_API_KEY),
        "api_key_preview": settings.OPENAI_API_KEY[:20] + "..." if settings.OPENAI_API_KEY else "NOT SET",
        "chat_model": settings.OPENAI_CHAT_MODEL,
        "base_url": settings.OPENAI_BASE_URL,
        "openai_module_available": openai is not None,
    }


@router.get("/instructions")
async def get_instructions():
    content = read_and_validate_instructions_md()
    return {"instructions": content}
