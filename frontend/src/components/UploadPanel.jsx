import { useState } from 'react'
import './UploadPanel.css'

const API_URL = 'http://localhost:8000'

function UploadPanel({ onUploadSuccess }) {
    const [uploading, setUploading] = useState(false)
    const [preview, setPreview] = useState(null)
    const [dragActive, setDragActive] = useState(false)

    const handleFile = async (file) => {
        if (!file) return

        if (file.type.startsWith('image/')) {
            const reader = new FileReader()
            reader.onload = (e) => setPreview(e.target.result)
            reader.readAsDataURL(file)
        } else {
            setPreview(null)
        }

        setUploading(true)
        const formData = new FormData()
        formData.append('file', file)

        try {
            const response = await fetch(`${API_URL}/api/upload`, {
                method: 'POST',
                body: formData
            })
            const data = await response.json()
            onUploadSuccess(data)
        } catch (error) {
            alert('Upload failed: ' + error.message)
        } finally {
            setUploading(false)
        }
    }

    const handleDrag = (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true)
        } else if (e.type === 'dragleave') {
            setDragActive(false)
        }
    }

    const handleDrop = (e) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)
        if (e.dataTransfer.files?.[0]) {
            handleFile(e.dataTransfer.files[0])
        }
    }

    return (
        <div className="panel upload-panel">
            <div className="panel-header">
                <h2>
                    <span className="icon">📤</span> Uploaded Document
                </h2>
            </div>
            <div
                className={`upload-area ${dragActive ? 'drag-active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                {uploading ? (
                    <div className="upload-content">
                        <div className="spinner"></div>
                        <p>Processing...</p>
                    </div>
                ) : preview ? (
                    <div className="preview-container">
                        <img src={preview} alt="Preview" />
                    </div>
                ) : (
                    <div className="upload-content">
                        <div className="upload-icon">📄</div>
                        <p>Drag & drop to upload</p>
                        <input
                            type="file"
                            accept=".pdf,.png,.jpg,.jpeg,.tiff,.bmp"
                            onChange={(e) => handleFile(e.target.files[0])}
                        />
                    </div>
                )}
            </div>
        </div>
    )
}

export default UploadPanel
