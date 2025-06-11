import './MessageBubble.css'

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user'
  const isAssistant = message.role === 'assistant'

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        {isAssistant && (
          <div className="buddy-avatar">
            🤖
          </div>
        )}
        <div className="message-text">
          <p>{message.content}</p>
          <span className="message-time">
            {formatTime(message.timestamp)}
          </span>
        </div>
        {isUser && (
          <div className="user-avatar">
            👤
          </div>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
