import { useState } from 'react'
import ChatPanel from './components/ChatPanel'
import UploadPanel from './components/UploadPanel'
import PreviewPanel from './components/PreviewPanel'
import './App.css'

function App() {
  const [html, setHtml] = useState('')
  const [uploadedFile, setUploadedFile] = useState(null)

  const handleUploadSuccess = (result) => {
    setHtml(result.html)
    setUploadedFile(result.filename)
  }

  const handleHtmlUpdate = (newHtml) => {
    setHtml(newHtml)
  }

  return (
    <div className="app">
      <div className="panels-container">
        <ChatPanel html={html} onHtmlUpdate={handleHtmlUpdate} />
        <UploadPanel onUploadSuccess={handleUploadSuccess} />
        <PreviewPanel html={html} />
      </div>
    </div>
  )
}

export default App
