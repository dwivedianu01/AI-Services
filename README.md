# Chatbot Demo

Minimal full-stack chatbot demo with a Python backend and React frontend.

## Stack

- Backend: FastAPI
- Frontend: React + Vite

## Project structure

```text
backend/
frontend/
```

## Backend setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on `http://localhost:8000`.

Configure `backend/config.ini` before starting the backend. For OpenAI-compatible providers, set:

```ini
[OPENAI]
api_key = your_provider_key
base_url = https://your-openai-compatible-endpoint/v1
chat_model = your-chat-model
embedding_model = your-embedding-model
```

## Frontend setup

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`.

## APIs

- `GET /api/health`
- `GET /api/chat?message=hello`
