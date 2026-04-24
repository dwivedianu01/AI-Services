## Adzuna Integration

- Endpoints:
  - GET /api/jobs/adzuna?role=&location=&results_per_page=
  - POST /api/jobs/summary (multipart form with optional resume_file)

- How it works:
  - User provides a role from the UI
  - The system fetches Adzuna job descriptions for that role and location, and derives trend/skill signals
  - If a resume is uploaded, the system analyzes the resume against the role and derives improvement suggestions
  - Results can be persisted if DB is enabled

- Configuration:
  - Adzuna credentials can be provided via environment variables ADZUNA_APP_ID and ADZUNA_APP_KEY
  - Or in backend/config.ini under [ADZUNA]
    - app_id = YOUR_ADZUNA_APP_ID
    - app_key = YOUR_ADZUNA_APP_KEY

- Example config.ini addition:
  [ADZUNA]
  app_id = YOUR_ADZUNA_APP_ID
  app_key = YOUR_ADZUNA_APP_KEY
