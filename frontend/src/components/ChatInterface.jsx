import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'
import './ChatInterface.css'

const API_BASE_URL = 'https://buddy-uge1.onrender.com'

const ChatInterface = () => {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Load buddy's intro message when component mounts
    loadBuddyIntro()
  }, [])

  const loadBuddyIntro = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/buddy/intro`)
      const introMessage = {
        id: Date.now(),
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toISOString()
      }
      setMessages([introMessage])
    } catch (error) {
      console.error('Error loading buddy intro:', error)
      // Fallback intro message
      const fallbackMessage = {
        id: Date.now(),
        role: 'assistant',
        content: "Yo! What's up, dude! 🤙 I'm your buddy and I'm pumped to chat with you! What's on your mind?",
        timestamp: new Date().toISOString()
      }
      setMessages([fallbackMessage])
    }
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    
    if (!inputMessage.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)
    setIsTyping(true)

    try {
      // Prepare conversation history for context
      const conversationHistory = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }))

      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: userMessage.content,
        conversation_history: conversationHistory
      })

      // Simulate typing delay for more natural feel
      setTimeout(() => {
        const buddyMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.data.response,
          timestamp: new Date().toISOString()
        }

        setMessages(prev => [...prev, buddyMessage])
        setIsTyping(false)
        setIsLoading(false)
      }, 1000 + Math.random() * 1000) // Random delay between 1-2 seconds

    } catch (error) {
      console.error('Error sending message:', error)
      setIsTyping(false)
      setIsLoading(false)
      
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: "Yo dude, something went wrong on my end! 😅 Can you try that again? My brain's having a moment!",
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(e)
    }
  }

  return (
    <div className="chat-interface">
      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
            />
          ))}
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={sendMessage} className="message-form">
          <div className="input-container">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here... (Press Enter to send)"
              className="message-input"
              rows="1"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || isLoading}
              className="send-button"
            >
              {isLoading ? '...' : '🚀'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ChatInterface
