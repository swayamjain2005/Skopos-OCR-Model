import { useState, useRef, useEffect } from 'react'
import './ChatPanel.css'

const API_URL = 'http://localhost:8000'

function ChatPanel({ html, onHtmlUpdate }) {
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(scrollToBottom, [messages])

    const handleSend = async () => {
        if (!input.trim() || !html) return

        const userMessage = { role: 'user', content: input }
        setMessages(prev => [...prev, userMessage])
        setInput('')
        setLoading(true)

        try {
            const response = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input })
            })

            const data = await response.json()

            setMessages(prev => [...prev, { role: 'assistant', content: data.message }])
            onHtmlUpdate(data.html)
        } catch (error) {
            setMessages(prev => [...prev, { role: 'error', content: 'Failed to process request' }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="panel chat-panel">
            <div className="panel-header">
                <h2>
                    <span className="icon">💬</span> AI Chat
                </h2>
            </div>
            <div className="messages">
                {messages.length === 0 && !html && (
                    <div className="empty-state">
                        <p>Hello! Upload a document to get started.</p>
                    </div>
                )}
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        <div className="message-content">{msg.content}</div>
                    </div>
                ))}
                {loading && <div className="message assistant loading">Thinking...</div>}
                <div ref={messagesEndRef} />
            </div>
            <div className="input-area">
                <div className="input-container">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Type your message..."
                        disabled={!html || loading}
                    />
                    <button
                        className="send-btn"
                        onClick={handleSend}
                        disabled={!html || loading || !input.trim()}
                    >
                        ➤
                    </button>
                </div>
            </div>
        </div>
    )
}

export default ChatPanel
