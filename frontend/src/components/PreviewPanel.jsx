import { useState } from 'react'
import './PreviewPanel.css'

const API_URL = 'http://localhost:8000'

function PreviewPanel({ html }) {
    const [viewMode, setViewMode] = useState('preview')

    const handleExport = () => {
        const blob = new Blob([html], { type: 'text/html' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'document.html'
        a.click()
        URL.revokeObjectURL(url)
    }

    const handleExportPdf = async () => {
        try {
            const response = await fetch(`${API_URL}/api/export/pdf`)
            if (!response.ok) throw new Error('Export failed')

            const blob = await response.blob()
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = 'document.pdf'
            document.body.appendChild(a)
            a.click()
            window.URL.revokeObjectURL(url)
            document.body.removeChild(a)
        } catch (error) {
            alert('PDF Export failed: ' + error.message)
        }
    }

    return (
        <div className="panel preview-panel">
            <div className="panel-header">
                <h2>
                    <span className="icon">👁️</span> Generated Document
                </h2>
                <div className="preview-controls">
                    <button
                        className={`control-btn ${viewMode === 'preview' ? 'active' : ''}`}
                        onClick={() => setViewMode('preview')}
                    >
                        Preview
                    </button>
                    <button
                        className={`control-btn ${viewMode === 'code' ? 'active' : ''}`}
                        onClick={() => setViewMode('code')}
                    >
                        Code
                    </button>
                    {html && (
                        <button className="control-btn" onClick={handleExport}>
                            Export HTML
                        </button>
                    )}
                    {html && (
                        <button className="control-btn" onClick={handleExportPdf}>
                            Export PDF
                        </button>
                    )}
                </div>
            </div>
            <div className="preview-content">
                {!html ? (
                    <div className="empty-state" style={{ color: '#666', display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                        No document generated
                    </div>
                ) : viewMode === 'preview' ? (
                    <iframe srcDoc={html} title="Preview" />
                ) : (
                    <pre className="code-view">{html}</pre>
                )}
            </div>
        </div>
    )
}

export default PreviewPanel
