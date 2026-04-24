# Job Analysis Tool

Job Analysis Tool is a full-stack AI job search and resume analysis project built with FastAPI, React, Vite, and Adzuna. It helps users explore live job descriptions, extract trending keywords for a target role, and compare a resume against role requirements using either OpenAI or a built-in heuristic analyzer.

If someone is searching GitHub for resume analyzer, ATS checker, job description analyzer, job trend analysis, FastAPI resume screening, or React job dashboard, this repository is intended to match those use cases directly.

## Features

- Search live job listings by role and location using the Adzuna API.
- Generate role summaries from current job descriptions.
- Extract high-signal keywords from live market data.
- Recommend the most relevant job description for a given role search.
- Upload resumes in PDF, DOC, DOCX, or TXT format.
- Run AI resume analysis with OpenAI when an API key is configured.
- Fall back to a local heuristic ATS-style evaluator when AI is unavailable.
- Persist analysis results to MySQL when database support is enabled.
- Check backend health and database connectivity from the UI.

## Why This Project Stands Out

- Combines job market research and resume analysis in one workflow.
- Uses real job listing data instead of static demo text.
- Works in both AI-enabled and offline heuristic modes.
- Has a simple FastAPI backend and a lightweight React frontend, which makes it easy to extend for portfolio or internship projects.

## Tech Stack

**Frontend**

- React 19
- Vite 5

**Backend**

- FastAPI
- Uvicorn
- OpenAI Python SDK
- pdfplumber
- python-docx
- PyMySQL
- Requests

**Data Sources and Services**

- Adzuna Jobs API
- Optional OpenAI chat model integration
- Optional MySQL storage

## Project Structure

```text
job-analysis-tool/
  backend/
    main.py
    service.py
    config.ini
    routes/
      jobs_controller.py
      resume_controller.py
    utils/
      adzuna_api.py
      config.py
      database.py
  frontend/
    App.jsx
    main.jsx
    package.json
    vite.config.js
```

## How It Works

1. A user enters a target role and location.
2. The backend fetches matching jobs from Adzuna.
3. The app extracts common keywords from job descriptions.
4. The backend selects the best matching job description from the search results.
5. The user can upload a resume for ATS-style analysis against that role.
6. The analysis is generated either with OpenAI or with built-in heuristic scoring.

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd job-analysis-tool
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure backend settings

Edit `backend/config.ini` and set the values you need.

Typical configuration areas include:

- OpenAI API key and model
- allowed frontend origins
- upload size limit
- MySQL connection settings
- Adzuna API credentials

Example sections:

```ini
[OPENAI]
api_key = YOUR_OPENAI_API_KEY
chat_model = gpt-4o-mini

[SERVER]
environment = development
allowed_origins = http://localhost:5173
max_upload_size_mb = 8

[DATABASE]
enabled = false
host = localhost
port = 3306
user = root
password =
database = job_analysis

[ADZUNA]
app_id = YOUR_ADZUNA_APP_ID
app_key = YOUR_ADZUNA_APP_KEY
```

### 4. Run the backend

```bash
uvicorn main:app --reload --app-dir .
```

The API will start on `http://localhost:8000`.

### 5. Set up the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will start on `http://localhost:5173`.

## Configuration Notes

### OpenAI integration

- If `api_key` is present in the `OPENAI` section, the app uses OpenAI for structured resume analysis.
- If no API key is configured, the app automatically falls back to heuristic scoring.

### Adzuna integration

- The jobs workflow depends on Adzuna credentials.
- Add `app_id` and `app_key` in the `ADZUNA` section of `backend/config.ini`.

### Database support

- Database writes are optional.
- Set `enabled = true` in the `DATABASE` section to persist analysis runs.

## API Endpoints

### Health

- `GET /health`
- `GET /api/health`

Returns environment, AI status, and database connectivity information.

### Jobs

- `GET /api/jobs/adzuna?role=<role>&location=<location>&results_per_page=<n>`

Fetches live jobs for a target role and location.

- `POST /api/jobs/summary`

Form fields:

- `role`
- `location`
- `resume_file` optional

Returns:

- role summary context
- extracted top keywords
- matched jobs
- best job description
- optional resume analysis result when a file is included

### Resume Analysis

- `POST /api/resume/analyze`

Form fields:

- `resume_file`
- `job_title`
- `job_description`
- `required_skills`

Returns:

- overall score
- skill score
- experience score
- structure score
- ATS score
- matched skills
- missing skills
- strengths
- weaknesses
- improvement suggestions

## Supported Resume Formats

- PDF
- DOC
- DOCX
- TXT

## Local Development Notes

- The Vite dev server proxies `/api` and `/health` to `http://localhost:8000`.
- The default frontend origin is `http://localhost:5173`.
- The backend enforces a maximum upload size from `config.ini`.

## Example Use Cases

- Build a smart resume screening project for a portfolio.
- Analyze job trends for software engineer, data analyst, or product manager roles.
- Compare resumes against live hiring demand.
- Extend the app into an ATS scoring dashboard or career assistant.

## GitHub Search Keywords

This project is relevant to these search terms:

- AI resume analyzer
- ATS resume checker
- job description analyzer
- Adzuna API project
- FastAPI React full stack project
- job market trend analysis
- resume screening tool
- OpenAI resume feedback app

## Suggested Repository Topics

If you want better GitHub discoverability, add repository topics such as:

- `fastapi`
- `react`
- `vite`
- `openai`
- `resume-analyzer`
- `ats-checker`
- `job-search`
- `career-tools`
- `adzuna-api`
- `full-stack-project`

## Future Improvements

- Add authentication and saved user sessions.
- Visualize keyword trends and role demand over time.
- Add resume version comparison.
- Export reports as PDF.
- Support more job providers beyond Adzuna.

## License

No license has been added yet. If you plan to share or open source this project publicly, add a license file so others know how they can use it.
