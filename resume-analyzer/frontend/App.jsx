import React, { useState } from 'react'

const initialForm = {
  jobTitle: 'Frontend Engineer',
  requiredSkills: 'React, JavaScript, TypeScript, HTML, CSS, REST APIs',
  jobDescription:
    'We are hiring a frontend engineer to build accessible web interfaces, collaborate with designers, and deliver production-ready React applications.',
}

export default function App() {
  const [form, setForm] = useState(initialForm)
  const [resumeFile, setResumeFile] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function updateField(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (!resumeFile || loading) {
      setError('Attach a PDF, DOC, or DOCX resume before analyzing.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const payload = new FormData()
      payload.append('resume_file', resumeFile)
      payload.append('job_title', form.jobTitle.trim())
      payload.append('job_description', form.jobDescription.trim())
      payload.append('required_skills', form.requiredSkills.trim())

      const response = await fetch('/api/resume/analyze', {
        method: 'POST',
        body: payload,
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Resume analysis failed.')
      }

      setResult(data)
    } catch (submitError) {
      setError(submitError.message)
    } finally {
      setLoading(false)
    }
  }

  const analysis = result?.analysis
  const analysisSource = result?.analysis_source
  const analysisSourceLabel = result?.analysis_source_label
  const analysisSourceDetail = result?.analysis_source_detail

  return (
    <main className="app-shell">
      <header className="top-header">
        <h2>Resume Analyzer</h2>
        <p>Upload a resume and score it against a role.</p>
      </header>
      <section className="content-two-col" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <form className="panel form-panel" onSubmit={handleSubmit}>
          <label className="field field-upload">
            <span>Resume file</span>
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={(event) => setResumeFile(event.target.files?.[0] ?? null)}
            />
            <small>{resumeFile ? resumeFile.name : 'No file selected'}</small>
          </label>

          <label className="field">
            <span>Job title</span>
            <input
              name="jobTitle"
              value={form.jobTitle}
              onChange={updateField}
              placeholder="Senior Backend Engineer"
              maxLength={120}
            />
          </label>

          <label className="field">
            <span>Required skills</span>
            <input
              name="requiredSkills"
              value={form.requiredSkills}
              onChange={updateField}
              placeholder="Python, FastAPI, SQL, Docker"
              maxLength={300}
            />
          </label>

          <label className="field">
            <span>Job description</span>
            <textarea
              name="jobDescription"
              value={form.jobDescription}
              onChange={updateField}
              rows={7}
              placeholder="Paste the job description here"
            />
          </label>

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>

          {error ? <p className="error-banner">{error}</p> : null}
        </form>

        <section className="panel results-panel" aria-live="polite">
          <div className="results-header">
            <div>
              <p className="section-label">Analysis</p>
              <h2>{analysis?.candidate_name || 'Waiting for upload'}</h2>
            </div>
            <div className="score-chip">{analysis ? `${analysis.overall_score}/100` : '--/100'}</div>
          </div>

          {analysis ? (
            <>
              <div className={`source-banner ${analysisSource === 'openai' ? 'source-openai' : 'source-heuristic'}`}>
                <div>
                  <p className="section-label">Result source</p>
                  <strong>{analysisSourceLabel}</strong>
                </div>
                <p>
                  {analysisSource === 'openai'
                    ? 'This result was generated with the configured OpenAI model.'
                    : 'This result was generated locally using the built-in heuristic fallback because no API key was used or the AI call was unavailable.'}
                </p>
                {analysisSourceDetail ? <p className="source-detail">{analysisSourceDetail}</p> : null}
              </div>

              <p className="summary-copy">{analysis.summary}</p>

              <div className="score-grid">
                <Metric label="Skill match" value={analysis.skill_score} max={40} />
                <Metric label="Experience" value={analysis.experience_score} max={25} />
                <Metric label="Structure" value={analysis.structure_score} max={20} />
                <Metric label="ATS" value={analysis.ats_score} max={15} />
              </div>

              <TagSection title="Matched skills" items={analysis.matched_skills} />
              <TagSection title="Missing skills" items={analysis.missing_skills} tone="muted" />
              <ListSection title="Strengths" items={analysis.strengths} />
              <ListSection title="Weaknesses" items={analysis.weaknesses} />
              <ListSection title="Improvements" items={analysis.improvement_suggestions} />

              <div className="preview-box">
                <p className="section-label">Extracted preview</p>
                <p>{result.resume_preview}</p>
              </div>
            </>
          ) : (
            <p className="placeholder-copy">
              Your results will appear here after you upload a resume and submit the role details.
            </p>
          )}
        </section>
      </section>
    </main>
  )
}

function Metric({ label, value, max }) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>
        {value}/{max}
      </strong>
    </div>
  )
}

function TagSection({ title, items, tone = 'default' }) {
  return (
    <section>
      <p className="section-label">{title}</p>
      <div className="tag-row">
        {items?.length ? (
          items.map((item) => (
            <span key={`${title}-${item}`} className={`tag ${tone}`}>
              {item}
            </span>
          ))
        ) : (
          <span className="empty-state">No items</span>
        )}
      </div>
    </section>
  )
}

function ListSection({ title, items }) {
  return (
    <section>
      <p className="section-label">{title}</p>
      {items?.length ? (
        <ul className="list-block">
          {items.map((item) => (
            <li key={`${title}-${item}`}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="empty-state">No items</p>
      )}
    </section>
  )
}
