import React, { useState } from 'react'

const starterMessages = [
  {
    id: 1,
    role: 'assistant',
    text: 'Ask me about your library data - books, authors, members, etc.',
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
      const response = await fetch('/chatbot/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: trimmed }),
      })
      const data = await response.json()

      if (data.error) {
        throw new Error(data.error)
      }

      const sqlDisplay = data.generated_sql ? `\n\n\`\`\`sql\n${data.generated_sql}\n\`\`\`` : ''
      const resultsDisplay = data.results?.length > 0
        ? `\n\n📊 Results (${data.results.length} rows):\n${JSON.stringify(data.results, null, 2)}`
        : ''

      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          text: `${sqlDisplay}${resultsDisplay}`,
        },
      ])
    } catch (err) {
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'assistant',
          text: `Error: ${err.message}. Make sure backend is running on port 8000.`,
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
          <p className="eyebrow">Library RAG</p>
          <h1>Data Chatbot</h1>
          <p className="subtitle">
            Query your library database using natural language.
          </p>
        </div>

        <div className="messages" aria-live="polite">
          {messages.map((message) => (
            <article
              key={message.id}
              className={`message ${message.role === 'user' ? 'user' : 'assistant'}`}
            >
              <span className="badge">{message.role === 'user' ? 'You' : 'Bot'}</span>
              <p style={{ whiteSpace: 'pre-wrap' }}>{message.text}</p>
            </article>
          ))}
          {loading ? <p className="status">Generating SQL and fetching data...</p> : null}
        </div>

        <form className="composer" onSubmit={sendMessage}>
          <input
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about books, authors, members..."
            maxLength={500}
          />
          <button type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </section>
    </main>
  )
}
