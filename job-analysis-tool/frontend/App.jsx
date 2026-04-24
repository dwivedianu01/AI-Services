import React, { useState } from 'react'

export default function App() {
  // Flow: 1) Enter role, 2) fetch descriptions, 3) analyze role (LLM), 4) show final job and allow resume analysis
  const [role, setRole] = useState('')
  const [location, setLocation] = useState('India')
  const [jobs, setJobs] = useState([])
 const [bestJob, setBestJob] = useState(null)
  const [loadingJobs, setLoadingJobs] = useState(false)
  const [loadingSummary, setLoadingSummary] = useState(false)
  const [resumeFile, setResumeFile] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [error, setError] = useState('')
  const [health, setHealth] = useState(null)

  async function fetchJobs() {
    if (!role.trim()) return
    setLoadingJobs(true)
    setError('')
    try {
      const resp = await fetch(`/api/jobs/adzuna?role=${encodeURIComponent(role)}&location=${encodeURIComponent(location)}&results_per_page=5`)
      const data = await resp.json()
      if (!resp.ok) throw new Error(data?.detail || 'Failed to fetch jobs')
      setJobs(data.jobs || [])
      setBestJob(null)
    } catch (e) {
      setError(e?.message || 'Failed to fetch jobs')
    } finally {
      setLoadingJobs(false)
    }
  }

  async function checkHealth() {
    try {
      const resp = await fetch('/api/health')
      const data = await resp.json()
      if (!resp.ok) throw new Error(data?.detail || 'Health check failed')
      setHealth(data)
    } catch (e) {
      setHealth({ status: 'unknown', error: e?.message })
    }
  }

  async function analyzeRole() {
    if (!role.trim()) return
    setLoadingSummary(true)
    setError('')
    try {
      const resp = await fetch(`/api/jobs/summary`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ role, location }).toString(),
      })
      const data = await resp.json()
      if (!resp.ok) throw new Error(data?.detail || 'Failed to analyze role')
      // best job is provided by backend as best_job field
      setBestJob(data.best_job)
      // store top keywords for resume analysis
      // attach to bestJob for later use
      setJobs((j) => j)
      setAnalysis(null)
    } catch (e) {
      setError(e?.message || 'Analysis failed')
    } finally {
      setLoadingSummary(false)
    }
  }

  async function analyzeResume() {
    if (!resumeFile) return
    // Prepare job description and skills from bestJob
    const jobDescription = bestJob?.description || bestJob?.title || ''
    const requiredSkills = bestJob?.top_keywords?.join(', ') || ''
    const form = new FormData()
    form.append('resume_file', resumeFile)
    form.append('job_title', role)
    form.append('job_description', jobDescription)
    form.append('required_skills', requiredSkills)

    try {
      const resp = await fetch('/api/resume/analyze', {
        method: 'POST',
        body: form,
      })
      const data = await resp.json()
      if (!resp.ok) throw new Error(data?.detail || 'Resume analysis failed.')
      setAnalysis(data)
    } catch (e) {
      setError(e?.message || 'Resume analysis failed')
    }
  }

  return (
    <main className="app-shell">
      <header className="top-header">
        <h2>Job Role Explorer</h2>
        <p>Enter a job role to fetch matching descriptions, analyze trends, and optionally upload a resume for role-aligned feedback.</p>
        <div style={{ marginTop: 8 }}>
          <button className="secondary-button" onClick={checkHealth}>Check Backend Health</button>
          {health ? (
            <span style={{ marginLeft: 12 }}>
              Health: {health.status} {health.environment ? `· Env: ${health.environment}` : ''}
              {health.database && health.database.connected ? ' · DB connected' : ''}
            </span>
          ) : <span style={{ marginLeft: 8, color: '#666' }}>Click to verify backend</span>}
        </div>
      </header>

      <section className="content-two-col" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <section className="panel form-panel" style={{ padding: '16px' }}>
          <label className="field">
            <span>Job role</span>
            <input value={role} onChange={(e) => setRole(e.target.value)} placeholder="e.g. Senior Backend Engineer" />
          </label>
          <label className="field">
            <span>Location</span>
            <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="e.g. India" />
          </label>
          <button className="primary-button" onClick={fetchJobs} disabled={loadingJobs || !role}>
            {loadingJobs ? 'Fetching descriptions...' : 'Fetch Descriptions'}
          </button>

          <div style={{ marginTop: 12 }}>
            <input type="file" accept=".pdf,.doc,.docx,.txt" onChange={(e) => setResumeFile(e.target.files?.[0] ?? null)} />
          </div>
          <div style={{ marginTop: 8 }}>
            <button className="secondary-button" onClick={analyzeRole} disabled={loadingSummary || !role}>
              {loadingSummary ? 'Analyzing role...' : 'Analyze Role (LLM)'}
            </button>
          </div>
          {error && <p className="error-banner" style={{ marginTop: 8 }}>{error}</p>}
        </section>

        <section className="panel results-panel" style={{ padding: '16px' }}>
          <h3>Job Descriptions</h3>
          {jobs && jobs.length > 0 ? (
            <ul>
              {jobs.map((j, idx) => (
                <li key={idx} style={{ marginBottom: 8 }}>
                  <strong>{j.title}</strong> — {j.company} ({j.location})
                  <div style={{ color: '#555' }}>{j.description}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="placeholder-copy">No descriptions loaded yet.</p>
          )}
          {bestJob ? (
            <div style={{ marginTop: 16 }}>
              <h4>Final Recommended Description</h4>
              <div style={{ border: '1px solid #ddd', padding: 12, borderRadius: 6 }}>
                <strong>{bestJob.title}</strong> — {bestJob.company} ({bestJob.location})
                <p style={{ whiteSpace: 'pre-wrap' }}>{bestJob.description}</p>
              </div>
            </div>
          ) : null}
        </section>
      </section>

      <section className="content-two-col" style={{ marginTop: '-12px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <section className="panel" style={{ padding: 16 }}>
          <h3>Resume Analysis for This Role</h3>
          <p>After selecting a final job description, upload a resume to receive LLm-guided insights and an improvement plan.</p>
          <div>
            <input type="file" accept=".pdf,.doc,.docx,.txt" onChange={(e) => setResumeFile(e.target.files?.[0] ?? null)} />
          </div>
          <button className="primary-button" onClick={analyzeResume} disabled={!resumeFile} style={{ marginTop: 8 }}>
            Analyze Resume for Role
          </button>
        </section>
        <section className="panel results-panel" style={{ padding: 16 }}>
          {analysis ? (
            <div>
              <h3>Analysis Result</h3>
              <p>Overall score: {analysis.overall_score}/100</p>
              <p>Summary: {analysis.summary}</p>
              {/* You could expand with more fields here similarly to the Resume Analyzer UI */}
            </div>
          ) : (
            <p className="placeholder-copy">No analysis yet. Upload a resume and click to analyze.</p>
          )}
        </section>
      </section>
    </main>
  )
}
