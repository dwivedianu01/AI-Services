import React, { useState } from 'react'

const API_BASE = 'http://localhost:8000'

export default function App() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  async function handleAiAssistance() {
    if (!text.trim()) {
      setError('Please enter some text before using AI Assistance.')
      setMessage('')
      return
    }

    setLoading(true)
    setError('')
    setMessage('Processing text with AI...')

    try {
      const response = await fetch(`${API_BASE}/grammerly/fix`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ payload: text }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `API error: ${response.status}`)
      }

      const data = await response.json()
      setText(data.fixed ?? '')
      setMessage('Text updated from AI Assistance.')
    } catch (err) {
      setError(err.message || 'Failed to process text.')
      setMessage('')
    } finally {
      setLoading(false)
    }
  }

  async function handleSubmit() {
    if (!text.trim()) {
      setError('Please enter some text before submitting.')
      setMessage('')
      return
    }

    setLoading(true)
    setError('')
    setMessage('Submitting text...')

    try {
      const response = await fetch(`${API_BASE}/grammerly/fix`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ payload: text }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `API error: ${response.status}`)
      }

      const data = await response.json()
      setText(data.fixed ?? text)
      setMessage('Submission complete. The text was cleaned and updated.')
    } catch (err) {
      setError(err.message || 'Failed to submit text.')
      setMessage('')
    } finally {
      setLoading(false)
    }
  }

  function handleClear() {
    setText('')
    setMessage('')
    setError('')
  }

  return (
    <div className="shell">
      <div className="card">
        <h1>AI Text Assistant</h1>
        <p className="subtitle">Paste your text here, then use AI Assistance to remove unwanted HTML/CSS and clean it up.</p>

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter or paste your text here..."
          aria-label="Text input"
        />

        <div className="button-row">
          <button type="button" className="button secondary" onClick={handleClear} disabled={loading}>
            Clear
          </button>
          <button type="button" className="button accent" onClick={handleAiAssistance} disabled={loading}>
            AI Assistance
          </button>
          <button type="button" className="button primary" onClick={handleSubmit} disabled={loading}>
            Submit
          </button>
        </div>

        <div className="status-row">
          {loading && <span className="status">Working…</span>}
          {message && <span className="status success">{message}</span>}
          {error && <span className="status error">{error}</span>}
        </div>
      </div>
    </div>
  )
}
