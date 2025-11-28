from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
from services.ocr_service import OCRService
from services.llm_service import LLMService
from config import UPLOAD_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS, BACKEND_PORT

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ocr_service = OCRService()
llm_service = LLMService()

# Create upload directory
Path(UPLOAD_DIR).mkdir(exist_ok=True)

class ChatRequest(BaseModel):
    message: str

class ExportResponse(BaseModel):
    html: str

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process document through OCR"""
    # Validate file
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}")
    
    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Check file size
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        os.remove(file_path)
        raise HTTPException(400, "File too large")
    
    try:
        # Process through OCR
        html_result = ocr_service.process_document(file_path)
        
        # Set HTML in LLM service
        llm_service.set_html(html_result)
        
        return {
            "success": True,
            "html": html_result,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat with LLM to modify HTML"""
    try:
        result = llm_service.chat(request.message)
        return result
    except Exception as e:
        raise HTTPException(500, f"Chat failed: {str(e)}")

@app.get("/api/export")
async def export_html():
    """Export current HTML"""
    return {"html": llm_service.current_html}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
