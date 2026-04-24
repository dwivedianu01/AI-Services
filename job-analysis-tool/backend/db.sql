aaaaCREATE TABLE IF NOT EXISTS resume_analysis_runs (
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
) ENGINE=InnoDB;

CREATE INDEX idx_resume_analysis_runs_created_at
    ON resume_analysis_runs (created_at);

CREATE INDEX idx_resume_analysis_runs_job_title
    ON resume_analysis_runs (job_title);
