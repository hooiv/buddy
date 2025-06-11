import { useState, useEffect } from 'react'
import ChatInterface from './components/ChatInterface'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 Chat with Your Buddy</h1>
        <p>Your friendly virtual companion who knows all about you!</p>
      </header>
      <main className="app-main">
        <ChatInterface />
      </main>
    </div>
  )
}

export default App
