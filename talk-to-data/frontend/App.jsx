import React, { useState } from 'react'

const starterMessages = [
  {
    id: 1,
    role: 'assistant',
    text: 'Ask about the time, date, or say hello.',
  },
]

export default function App() {
  const [messages, setMessages] = useState(starterMessages)
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  async function sendMessage(event) {
    event.preventDefault()

    const trimmed = input.trim()
    if (!trimmed || loading) {
      return
    }

    const userMessage = {
      id: Date.now(),
      role: 'user',
      text: trimmed,
    }

    setMessages((current) => [...current, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch(`/api/chat?message=${encodeURIComponent(trimmed)}`)
      const data = await response.json()

      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          text: data.reply,
        },
      ])
    } catch {
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          text: 'The backend could not be reached. Start FastAPI on port 8000.',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="chat-panel">
        <div className="hero">
          <p className="eyebrow">React + FastAPI</p>
          <h1>Chatbot UI</h1>
          <p className="subtitle">
            A simple chat-style frontend connected to a Python GET API.
          </p>
        </div>

        <div className="messages" aria-live="polite">
          {messages.map((message) => (
            <article
              key={message.id}
              className={`message ${message.role === 'user' ? 'user' : 'assistant'}`}
            >
              <span className="badge">{message.role === 'user' ? 'You' : 'Bot'}</span>
              <p>{message.text}</p>
            </article>
          ))}
          {loading ? <p className="status">Waiting for backend response...</p> : null}
        </div>

        <form className="composer" onSubmit={sendMessage}>
          <input
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Type a message"
            maxLength={200}
          />
          <button type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </section>
    </main>
  )
}
