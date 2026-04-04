import React from "react";
import Chatbot from "./Chatbot";

function App() {
  return (
    <main className="app-shell">
      <section className="chat-panel">
        <div className="hero">
          <p className="eyebrow">RAG PDF Reader</p>
          <h1>Document QA Chatbot</h1>
          <p className="subtitle">
            Ask questions about your PDF documents and get instant answers powered by AI.
          </p>
        </div>
        <Chatbot />
      </section>
    </main>
  );
}

export default App;