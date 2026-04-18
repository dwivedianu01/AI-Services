Talk-To-Data (Simple Readme)

Overview: A lightweight stack that translates natural-language questions into SQL queries via a FastAPI backend and a React frontend.

Quick Start
- Prereqs: Python 3.8+, Node.js, and an OpenAI API key.
- Backend:
  - cd talk-to-data/backend
  - python -m venv .venv
  - .venv\Scripts\activate
  - pip install -r requirements.txt
  - uvicorn main:app --reload --port 8000
- Frontend:
  - cd talk-to-data/frontend
  - npm install
  - npm run dev
- Open the UI at http://localhost:5173

API
- POST /chatbot/chat with JSON body: { "question": "Your natural language question" }
- Response: { "question": "...", "generated_sql": "...", "results": [...] }

Configuration
- Backend config in talk-to-data/backend/config.ini
- Ensure OPENAI.api_key is set

Notes
- This is a minimal README to onboard quickly. Update as you evolve the project.
