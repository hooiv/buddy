import './TypingIndicator.css'

const TypingIndicator = () => {
  return (
    <div className="typing-indicator">
      <div className="buddy-avatar">
        🤖
      </div>
      <div className="typing-content">
        <div className="typing-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <span className="typing-text">Buddy is thinking...</span>
      </div>
    </div>
  )
}

export default TypingIndicator
