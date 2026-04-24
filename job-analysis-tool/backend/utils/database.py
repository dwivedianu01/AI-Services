import json

import pymysql

from .config import settings


CREATE_ANALYSIS_RUNS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS resume_analysis_runs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(20) NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    required_skills TEXT,
    job_description LONGTEXT,
    candidate_name VARCHAR(255),
    overall_score INT,
    skill_score INT,
    experience_score INT,
    structure_score INT,
    ats_score INT,
    matched_skills JSON,
    missing_skills JSON,
    strengths JSON,
    weaknesses JSON,
    improvement_suggestions JSON,
    summary TEXT,
    resume_text LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
"""


def get_database_status() -> dict[str, object]:
    if not settings.DB_ENABLED:
        return {"enabled": False, "connected": False}

    if not settings.DB_CONFIGURED:
        return {"enabled": True, "connected": False, "detail": "Database settings are incomplete."}

    try:
        connection = _connect()
        connection.close()
        return {
            "enabled": True,
            "connected": True,
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "database": settings.DB_NAME,
        }
    except Exception as exc:
        return {
            "enabled": True,
            "connected": False,
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "database": settings.DB_NAME,
            "detail": str(exc),
        }


def save_analysis_run(
    *,
    file_name: str,
    file_type: str,
    resume_text: str,
    job_title: str,
    job_description: str,
    required_skills: str,
    analysis: dict,
) -> int | None:
    if not settings.DB_CONFIGURED:
        return None

    try:
        connection = _connect()
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ANALYSIS_RUNS_TABLE_SQL)
            cursor.execute(
                """
                INSERT INTO resume_analysis_runs (
                    file_name,
                    file_type,
                    job_title,
                    required_skills,
                    job_description,
                    candidate_name,
                    overall_score,
                    skill_score,
                    experience_score,
                    structure_score,
                    ats_score,
                    matched_skills,
                    missing_skills,
                    strengths,
                    weaknesses,
                    improvement_suggestions,
                    summary,
                    resume_text
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    file_name,
                    file_type,
                    job_title,
                    required_skills,
                    job_description,
                    analysis.get("candidate_name"),
                    analysis.get("overall_score"),
                    analysis.get("skill_score"),
                    analysis.get("experience_score"),
                    analysis.get("structure_score"),
                    analysis.get("ats_score"),
                    json.dumps(analysis.get("matched_skills", [])),
                    json.dumps(analysis.get("missing_skills", [])),
                    json.dumps(analysis.get("strengths", [])),
                    json.dumps(analysis.get("weaknesses", [])),
                    json.dumps(analysis.get("improvement_suggestions", [])),
                    analysis.get("summary"),
                    resume_text,
                ),
            )
        connection.commit()
        return int(connection.insert_id())
    except Exception:
        return None
    finally:
        if 'connection' in locals():
            connection.close()


def _connect():
    return pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        database=settings.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.Cursor,
        autocommit=False,
    )
