import io
import json
import re
from typing import Any

import pdfplumber
from docx import Document
from openai import OpenAI

from .utils.config import settings


SECTION_HINTS = ("summary", "experience", "skills", "projects", "education")


class OpenAIAnalysisError(Exception):
    pass


def extract_text_from_resume(filename: str, content: bytes) -> tuple[str, str]:
    extension = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if extension == "pdf":
        text = _extract_pdf_text(content)
    elif extension == "docx":
        text = _extract_docx_text(content)
    elif extension == "doc":
        text = _extract_doc_text(content)
    elif extension == "txt":
        text = content.decode("utf-8", errors="ignore")
    else:
        raise ValueError("Unsupported file type. Upload PDF, DOC, DOCX, or TXT.")

    normalized_text = _normalize_whitespace(text)
    if len(normalized_text) < 80:
        raise ValueError("The uploaded file does not contain enough readable resume text.")

    return normalized_text, extension or "unknown"


def analyze_resume(
    resume_text: str,
    job_title: str,
    job_description: str,
    required_skills: str,
) -> tuple[dict[str, Any], str, str]:
    if settings.OPENAI_ENABLED:
        try:
            return (
                _analyze_with_openai(
                    resume_text=resume_text,
                    job_title=job_title,
                    job_description=job_description,
                    required_skills=required_skills,
                ),
                "openai",
                "Result generated with the configured OpenAI model.",
            )
        except Exception as exc:
            raise OpenAIAnalysisError(
                f"OpenAI call failed. {type(exc).__name__}: {str(exc)}"
            )

    return (
        _analyze_with_heuristics(
            resume_text=resume_text,
            job_title=job_title,
            job_description=job_description,
            required_skills=required_skills,
        ),
        "heuristic",
        "No OpenAI API key is configured, so the app used local heuristic scoring.",
    )


def _extract_pdf_text(content: bytes) -> str:
    pages: list[str] = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n".join(pages)


def _extract_docx_text(content: bytes) -> str:
    document = Document(io.BytesIO(content))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def _extract_doc_text(content: bytes) -> str:
    decoded = content.decode("latin-1", errors="ignore")
    fragments = re.findall(r"[A-Za-z0-9@:/.,+()#%&' -]{4,}", decoded)
    filtered = [fragment.strip() for fragment in fragments if any(char.isalpha() for char in fragment)]
    return "\n".join(filtered)


def _normalize_whitespace(text: str) -> str:
    compact_lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    non_empty = [line for line in compact_lines if line]
    return "\n".join(non_empty)


def _analyze_with_openai(
    resume_text: str,
    job_title: str,
    job_description: str,
    required_skills: str,
) -> dict[str, Any]:
    client = OpenAI(**settings.OPENAI_CLIENT_KWARGS)
    prompt = f"""
Evaluate the resume against the target role.

Target role: {job_title}
Required skills: {required_skills}
Job description:
{job_description}

Resume:
{resume_text}

Return only valid JSON with this exact shape:
{{
  "candidate_name": "",
  "summary": "",
  "overall_score": 0,
  "skill_score": 0,
  "experience_score": 0,
  "structure_score": 0,
  "ats_score": 0,
  "matched_skills": [],
  "missing_skills": [],
  "strengths": [],
  "weaknesses": [],
  "improvement_suggestions": []
}}
""".strip()

    response = client.chat.completions.create(
        model=settings.OPENAI_CHAT_MODEL,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a strict ATS resume evaluator. Return JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    message = response.choices[0].message.content or "{}"
    payload = json.loads(message)
    return _coerce_analysis_shape(payload, resume_text, job_title, job_description, required_skills)


def _analyze_with_heuristics(
    resume_text: str,
    job_title: str,
    job_description: str,
    required_skills: str,
) -> dict[str, Any]:
    required = _extract_required_skills(required_skills, job_description)
    resume_lower = resume_text.lower()
    matched_skills = [skill for skill in required if skill.lower() in resume_lower]
    missing_skills = [skill for skill in required if skill not in matched_skills]

    skill_score = min(40, round((len(matched_skills) / max(len(required), 1)) * 40))
    experience_score = min(25, _estimate_experience_score(resume_text))
    structure_score = min(20, _estimate_structure_score(resume_text))
    ats_score = min(15, _estimate_ats_score(resume_text, matched_skills))
    overall_score = skill_score + experience_score + structure_score + ats_score

    strengths = []
    weaknesses = []
    suggestions = []

    if matched_skills:
        strengths.append(f"Matched {len(matched_skills)} required skills for the {job_title} role.")
    if experience_score >= 18:
        strengths.append("Resume shows enough experience signals for an initial recruiter screen.")
    if structure_score >= 14:
        strengths.append("Resume is structured with recognizable ATS-friendly sections.")

    if missing_skills:
        weaknesses.append(f"Missing or unclear evidence for: {', '.join(missing_skills[:6])}.")
        suggestions.append("Add measurable examples for the missing skills that matter most for the role.")
    if experience_score < 15:
        weaknesses.append("Experience depth is not clearly quantified across past roles.")
        suggestions.append("Quantify years of experience, scope, and outcomes for each role.")
    if structure_score < 12:
        weaknesses.append("Section headings or formatting may be too weak for reliable ATS parsing.")
        suggestions.append("Use clear sections such as Summary, Skills, Experience, Projects, and Education.")
    if ats_score < 10:
        weaknesses.append("ATS basics like contact details, keywords, or resume length need improvement.")
        suggestions.append("Ensure the resume includes email, phone, role keywords, and concise bullet points.")

    if not strengths:
        strengths.append("Resume contains enough text to run an automated baseline review.")
    if not weaknesses:
        weaknesses.append("No major baseline gaps detected by heuristic analysis.")
    if not suggestions:
        suggestions.append("Tailor the summary and top bullet points to the target role before applying.")

    return {
        "candidate_name": _extract_candidate_name(resume_text),
        "summary": _build_summary(overall_score, matched_skills, missing_skills),
        "overall_score": overall_score,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "structure_score": structure_score,
        "ats_score": ats_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "strengths": strengths[:4],
        "weaknesses": weaknesses[:4],
        "improvement_suggestions": suggestions[:4],
    }


def _coerce_analysis_shape(
    payload: dict[str, Any],
    resume_text: str,
    job_title: str,
    job_description: str,
    required_skills: str,
) -> dict[str, Any]:
    fallback = _analyze_with_heuristics(resume_text, job_title, job_description, required_skills)
    response = dict(fallback)
    response.update({key: value for key, value in payload.items() if value is not None})

    for numeric_key, maximum in {
        "overall_score": 100,
        "skill_score": 40,
        "experience_score": 25,
        "structure_score": 20,
        "ats_score": 15,
    }.items():
        response[numeric_key] = max(0, min(maximum, int(response.get(numeric_key, 0))))

    for list_key in ("matched_skills", "missing_skills", "strengths", "weaknesses", "improvement_suggestions"):
        value = response.get(list_key, [])
        response[list_key] = value if isinstance(value, list) else [str(value)]

    response["candidate_name"] = str(response.get("candidate_name") or _extract_candidate_name(resume_text))
    response["summary"] = str(response.get("summary") or fallback["summary"])
    return response


def _extract_required_skills(required_skills: str, job_description: str) -> list[str]:
    source = required_skills or job_description
    parts = re.split(r"[,\n;/|]", source)
    normalized: list[str] = []
    seen: set[str] = set()

    for part in parts:
        skill = re.sub(r"\s+", " ", part).strip(" -•\t")
        skill_key = skill.lower()
        if len(skill) < 2 or len(skill) > 40 or skill_key in seen:
            continue
        seen.add(skill_key)
        normalized.append(skill)

    return normalized[:15]


def _estimate_experience_score(resume_text: str) -> int:
    matches = re.findall(r"(\d{1,2})\+?\s+years?", resume_text, flags=re.IGNORECASE)
    max_years = max((int(value) for value in matches), default=0)
    if max_years >= 8:
        return 25
    if max_years >= 6:
        return 22
    if max_years >= 4:
        return 18
    if max_years >= 2:
        return 13
    if max_years >= 1:
        return 9
    return 6


def _estimate_structure_score(resume_text: str) -> int:
    found_sections = sum(1 for section in SECTION_HINTS if section in resume_text.lower())
    bullet_count = len(re.findall(r"(^|\n)[-•*] ", resume_text))
    score = found_sections * 4
    if bullet_count >= 5:
        score += 4
    return score


def _estimate_ats_score(resume_text: str, matched_skills: list[str]) -> int:
    score = 0
    if re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", resume_text, re.IGNORECASE):
        score += 4
    if re.search(r"\+?\d[\d\s().-]{7,}\d", resume_text):
        score += 3
    if 250 <= len(resume_text.split()) <= 1400:
        score += 4
    if matched_skills:
        score += min(4, len(matched_skills))
    return score


def _extract_candidate_name(resume_text: str) -> str:
    for line in resume_text.splitlines()[:6]:
        candidate = line.strip()
        if 2 <= len(candidate.split()) <= 5 and all(char.isalpha() or char in " -.'" for char in candidate):
            return candidate.title()
    return "Candidate"


def _build_summary(overall_score: int, matched_skills: list[str], missing_skills: list[str]) -> str:
    matched = ", ".join(matched_skills[:4]) or "no clearly matched skills"
    missing = ", ".join(missing_skills[:3]) or "no major missing skills"
    return (
        f"Overall score {overall_score}/100. Strongest alignment appears in {matched}. "
        f"The main gaps are {missing}."
    )
