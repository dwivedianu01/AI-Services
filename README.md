# AI Projects Workspace

This repository is a collection of AI, RAG, resume analysis, and data assistant projects built with FastAPI, React, Vite, OpenAI, FAISS, and supporting Python tooling. It is structured as a multi-project workspace for learning, prototyping, and showcasing practical AI applications.

If someone is searching GitHub for AI portfolio projects, FastAPI React AI apps, resume analyzer projects, RAG PDF chatbots, or natural language to SQL tools, this workspace is designed to surface those use cases clearly.

## Projects Included

### 1. Job Analysis Tool

Folder: `job-analysis-tool/`

A full-stack AI job search and resume analysis tool that combines live Adzuna job data with ATS-style resume scoring.

Key capabilities:

- search jobs by role and location
- extract top keywords from live job descriptions
- recommend the most relevant job posting
- compare resumes against market demand
- run OpenAI-based or heuristic resume analysis

Best for searches like:

- AI resume analyzer
- job description analyzer
- ATS checker project
- Adzuna API FastAPI React app

### 2. Resume Analyzer

Folder: `resume-analyzer/`

A focused resume review application built with FastAPI and React. It accepts uploaded resumes and evaluates them against a target job title, description, and required skills.

Key capabilities:

- upload PDF, DOC, DOCX, and TXT resumes
- score resumes for skills, structure, experience, and ATS readiness
- use OpenAI when configured
- fall back to heuristic analysis when AI is unavailable
- optionally persist results to a database

Best for searches like:

- resume analyzer
- ATS resume scanner
- FastAPI resume screening tool
- OpenAI resume feedback app

### 3. Talk-To-Data

Folder: `talk-to-data/`

An AI data assistant that lets users ask natural-language questions, retrieve relevant context, and generate data insights with a FastAPI backend and React frontend.

Key capabilities:

- natural language querying
- retrieval-augmented generation with FAISS
- knowledge-base powered responses
- schema-aware prompting for structured data exploration
- OpenAI-backed insight generation

Best for searches like:

- talk to your data
- natural language SQL project
- RAG data assistant
- FastAPI React analytics chatbot

### 4. RAG PDF Reader

Folder: `rag-pdf-reader/`

A retrieval-augmented generation app for chatting with PDF documents using vector search and AI-generated answers.

Key capabilities:

- upload and query PDF content
- ask questions about document collections
- use FAISS for semantic retrieval
- run with Docker Compose
- serve a chat-style React interface

Best for searches like:

- RAG PDF chatbot
- chat with PDF
- FastAPI React document QA
- FAISS PDF question answering

## Tech Stack Across the Workspace

**Backend**

- FastAPI
- Uvicorn
- OpenAI Python SDK
- FAISS
- PyMySQL
- pdfplumber
- python-docx

**Frontend**

- React
- Vite
- CSS

**AI and Retrieval**

- OpenAI-compatible LLM workflows
- Retrieval-Augmented Generation
- FAISS vector search
- prompt-based analysis and scoring

**Infrastructure**

- Docker and Docker Compose in selected projects
- local config-based development setup

## Repository Structure

```text
AI/
  job-analysis-tool/
  rag-pdf-reader/
  resume-analyzer/
  talk-to-data/
  knowledge_base/
  vectorstore/
```

## Who This Workspace Is For

- developers building AI portfolio projects
- students learning FastAPI and React full-stack development
- engineers exploring resume analysis, RAG, and data assistants
- recruiters or reviewers looking for practical applied AI examples

## Quick Start

Each project is self-contained and has its own backend and frontend setup.

General backend workflow:

```powershell
cd <project>/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

General frontend workflow:

```powershell
cd <project>/frontend
npm install
npm run dev
```

Notes:

- some projects use `requirement.txt` instead of `requirements.txt`
- some projects expose `main.py`, while others expose `api.py`
- several apps require OpenAI configuration in a local config file or environment variables

## Recommended Entry Points

- Start with `job-analysis-tool` if you want a polished AI + jobs + resume workflow.
- Start with `resume-analyzer` if you want a narrower ATS-style screening project.
- Start with `talk-to-data` if you want a natural-language data assistant.
- Start with `rag-pdf-reader` if you want a document chatbot or RAG demo.

## Search Keywords

This workspace is relevant to these GitHub search terms:

- AI projects portfolio
- FastAPI React AI apps
- resume analyzer project
- ATS checker app
- RAG PDF chatbot
- chat with documents
- natural language to SQL
- AI data assistant
- OpenAI FastAPI project
- FAISS vector search app

## Suggested GitHub Topics

If this workspace will be public, add repository topics such as:

- `ai-projects`
- `fastapi`
- `react`
- `vite`
- `openai`
- `rag`
- `resume-analyzer`
- `ats-checker`
- `pdf-chatbot`
- `faiss`
- `job-search`
- `nlp`

## Project Navigation

- See `job-analysis-tool/README.md` for the job market and resume analysis app.
- See `resume-analyzer/README.md` for the standalone resume analyzer.
- See `talk-to-data/README.md` for the data assistant project.
- See `rag-pdf-reader/README.md` for the document chat application.

## Future Improvements

- unify README quality across all subprojects
- add screenshots and demo GIFs for each app
- add licenses to each public-facing project
- standardize setup commands and naming conventions
- add a top-level comparison table for features and stack

## License

No top-level license file is present yet. If you plan to publish the workspace publicly, add a license so usage terms are explicit.
