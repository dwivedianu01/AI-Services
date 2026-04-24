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

## Adzuna Integration (New)

- Role-driven job fetch and resume-based analysis for UI workflow
- Endpoints:
  - GET /api/jobs/adzuna?role=<role>&location=<location>&results_per_page=<n>
    - Returns: role, location, results_per_page, count, jobs
  - POST /api/jobs/summary
    - multipart form: role (required), location (default India), resume_file (optional)
    - If a resume is provided, the backend analyzes it against the role and derives keyword trends from Adzuna job descriptions
    - If a DB is configured, the analysis results are persisted
- Credentials:
  - Adzuna APP_ID and APP_KEY can be supplied via environment variables ADZUNA_APP_ID, ADZUNA_APP_KEY
  - Or in backend/config.ini under [ADZUNA]:
    - app_id = YOUR_ADZUNA_APP_ID
    - app_key = YOUR_ADZUNA_APP_KEY
- Usage examples:
  - Fetch jobs for a role:
    curl -s "http://localhost:8000/api/jobs/adzuna?role=Data%20Scientist&location=India&results_per_page=5"
  - Summary with resume (multipart):
    curl -F "role=Data Scientist" -F "location=India" -F "resume_file=@/path/to/resume.pdf" http://localhost:8000/api/jobs/summary
- Notes:
  - Adzuna credentials are optional for local tests; without valid credentials the API will return an error.
  - DB persistence happens only when DATABASE.enabled=true and DB config is complete.
