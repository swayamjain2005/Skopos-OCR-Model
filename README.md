# Skopos OCR - AI-Powered Document Processing

An intelligent document processing application that uses Chandra OCR for document conversion and Gemini API for interactive HTML editing.

## Features

- **Document Upload**: Support for PDF, PNG, JPG, JPEG, TIFF, and BMP files
- **OCR Processing**: Powered by Chandra OCR for accurate document-to-HTML conversion
- **AI Chat Interface**: Interact with your documents using natural language via Gemini API
- **Live Preview**: Toggle between HTML code view and rendered preview
- **Export**: Download processed HTML documents

## Tech Stack

### Backend
- FastAPI
- LangChain + Gemini API
- Gradio Client (Chandra OCR integration)
- Python 3.x

### Frontend
- React 18
- Vite
- Modern CSS with glassmorphism effects

## Setup Instructions

### Backend Setup

1. Navigate to the Backend directory:
```bash
cd Backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python app.py
```

The backend will start on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

## Usage

1. **Upload a Document**: Drag and drop or click to upload a document (PDF or image)
2. **Wait for Processing**: The OCR will process your document and convert it to HTML
3. **Chat to Edit**: Use the chat panel to request modifications (e.g., "Make all headings bold")
4. **Preview Changes**: Toggle between code and preview to see your changes
5. **Export**: Download the final HTML document

## Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
CHANDRA_OCR_URL=http://34.27.210.23:8001/predict
BACKEND_PORT=8000
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/upload` - Upload and process document
- `POST /api/chat` - Chat with LLM to modify HTML
- `GET /api/export` - Export current HTML

## Architecture

```
┌─────────────────┐
│  React Frontend │
│  (3 Panels)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Server │
├─────────────────┤
│  OCR Service    │──► Chandra OCR
│  LLM Service    │──► Gemini API
└─────────────────┘
```
