# Grammerly AI Assistant

A simple, AI-powered text assistant that cleans and formats text using OpenAI with markdown-based instructions.

## Features

- **Text Input**: Paste any text into a clean, centered UI
- **AI Assistance**: Click to send text to OpenAI for intelligent cleaning
- **Markdown Context**: Instructions are read from `backend/aois/instructions.md` and passed to the LLM
- **Simple API**: Single `/aois/fix` endpoint for text processing

## Getting Started

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Configure `backend/config.ini`:
```ini
[OPENAI]
api_key = sk-proj-YOUR_OPENAI_API_KEY_HERE
base_url = https://api.openai.com/v1
chat_model = gpt-4o-mini

[SERVER]
environment = development
allowed_origins = http://localhost:5173
```

Run the backend:
```bash
uvicorn main:app --reload --port 8000
```
##Example:
```bash
(.venv) PS C:\Users\dwive\AI-Python\AI-Services\grammerly-ai-assistant\backend> python -m uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173`

## API Endpoint

**POST /aois/fix**

Request:
```json
{
  "payload": "Your text here..."
}
```

Response:
```json
{
  "fixed": "Cleaned text here...",
  "notes": ["Processed by OpenAI using instructions from instructions.md."]
}
```

## Instructions

Edit `backend/aois/instructions.md` to customize how the AI processes text.

  app_id = YOUR_ADZUNA_APP_ID
  app_key = YOUR_ADZUNA_APP_KEY
