from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..service import OpenAIAnalysisError, analyze_resume, extract_text_from_resume
from ..utils.config import settings
from ..utils.database import save_analysis_run


router = APIRouter(prefix="/api/resume", tags=["Resume Analyzer"])


@router.post("/analyze")
async def analyze_resume_file(
    resume_file: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    required_skills: str = Form(default=""),
):
    if not resume_file.filename:
        raise HTTPException(status_code=400, detail="Resume file is required.")

    file_bytes = await resume_file.read()
    file_size_mb = len(file_bytes) / (1024 * 1024)
    if file_size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"Resume exceeds the {settings.MAX_UPLOAD_SIZE_MB} MB upload limit.",
        )

    try:
        extracted_text, file_type = extract_text_from_resume(resume_file.filename, file_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Unable to parse the uploaded resume.") from exc

    try:
        analysis, analysis_source, analysis_source_detail = analyze_resume(
            resume_text=extracted_text,
            job_title=job_title.strip(),
            job_description=job_description.strip(),
            required_skills=required_skills.strip(),
        )
    except OpenAIAnalysisError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    saved_analysis_id = save_analysis_run(
        file_name=resume_file.filename,
        file_type=file_type,
        resume_text=extracted_text,
        job_title=job_title.strip(),
        job_description=job_description.strip(),
        required_skills=required_skills.strip(),
        analysis=analysis,
    )

    return {
        "analysis_source": analysis_source,
        "analysis_source_label": "OpenAI" if analysis_source == "openai" else "Built-in heuristic",
        "analysis_source_detail": analysis_source_detail,
        "database_saved": saved_analysis_id is not None,
        "saved_analysis_id": saved_analysis_id,
        "file_name": resume_file.filename,
        "file_type": file_type,
        "extracted_characters": len(extracted_text),
        "resume_preview": extracted_text[:1200],
        "analysis": analysis,
    }
