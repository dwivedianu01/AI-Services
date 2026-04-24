from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from typing import List, Optional

from ..utils.adzuna_api import fetch_jobs
from ..service import extract_text_from_resume, analyze_resume
from ..utils.config import settings
from ..utils.database import save_analysis_run

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("/adzuna")
def adzuna_jobs(
    role: str = Query(...),
    location: str = Query("India"),
    results_per_page: int = Query(5),
):
    try:
        jobs = fetch_jobs(role, location, results_per_page)
        return {
            "role": role,
            "location": location,
            "results_per_page": results_per_page,
            "count": len(jobs),
            "jobs": jobs,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/summary")
async def summary(
    role: str = Form(...),
    location: str = Form("India"),
    resume_file: Optional[UploadFile] = File(None),
):
    # Fetch current job market signals for the given role
    jobs = fetch_jobs(role, location, results_per_page=5)

    # Derive simple keyword trends from job descriptions
    import re
    from collections import Counter
    all_text = " ".join([j.get("description", "") or "" for j in jobs]).lower()
    words = re.findall(r"[a-zA-Z]{4,}", all_text)
    STOPWORDS = {
        "this","that","will","these","these","with","for","from","into",
        "when","where","which","what","also","more","than","have","has",
        "such","these","their","there","about",
    }
    filtered = [w for w in words if w not in STOPWORDS]
    top_keywords = [w for w, _ in Counter(filtered).most_common(8)]

    response = {
        "role": role,
        "location": location,
        "top_keywords": top_keywords,
        "jobs_found": len(jobs),
        "jobs": jobs,
    }

    # Determine the most relevant job description based on keyword overlap
    best_job = None
    if jobs:
        def overlap_score(job_item):
            desc = (job_item.get("description") or "").lower()
            score = sum(1 for kw in top_keywords if kw.lower() in desc)
            return score

        best_job = max(jobs, key=lambda ji: overlap_score(ji))
        if best_job and overlap_score(best_job) > 0:
            response["best_job"] = {
                "title": best_job.get("title"),
                "company": best_job.get("company"),
                "location": best_job.get("location"),
                "description": best_job.get("description"),
                "top_keywords": top_keywords,
            }
        else:
            response["best_job"] = None

    if resume_file is not None:
        # Analyze the provided resume against the role using existing analyzer
        content = await resume_file.read()
        # Build a safe filename for extraction (use a stable placeholder to avoid Optional typing issues)
        filename_for_extraction = "resume"
        try:
            extracted_text, file_ext = extract_text_from_resume(filename_for_extraction, content)
        except Exception:
            extracted_text = ""
            file_ext = ""

        if extracted_text:
            try:
                analysis, analysis_source, analysis_source_detail = analyze_resume(
                    resume_text=extracted_text,
                    job_title=role.strip(),
                    job_description="",
                    required_skills=",".join(top_keywords),
                )
                # Resolve a safe filename string for database storage (avoid Optional warnings)
                filename_for_extraction = str(resume_file.filename) if (resume_file and resume_file.filename) else ""
                saved_id = save_analysis_run(
                    file_name=filename_for_extraction,
                    file_type=file_ext,
                    resume_text=extracted_text,
                    job_title=role.strip(),
                    job_description="",
                    required_skills=",".join(top_keywords),
                    analysis=analysis,
                )
                response.update({
                    "analysis": analysis,
                    "analysis_source": analysis_source,
                    "analysis_source_detail": analysis_source_detail,
                    "resume_saved_id": saved_id,
                })
            except Exception as exc:
                response.update({"analysis_error": str(exc)})

    return response
