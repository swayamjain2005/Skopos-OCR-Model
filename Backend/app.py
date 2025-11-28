from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import uuid
from pathlib import Path
from xhtml2pdf import pisa
from io import BytesIO
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
    
    # Generate unique filename to prevent caching
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Check file size
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        os.remove(file_path)
        raise HTTPException(400, "File too large")
    
    try:
        # Process through OCR
        html_result = ocr_service.process_document(file_path)
        
        # Refine HTML using LLM for better formatting
        refined_html = llm_service.generate_html_from_text(html_result, file.filename)
        
        # Set HTML in LLM service
        llm_service.set_html(refined_html)
        
        return {
            "success": True,
            "html": refined_html,
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

@app.get("/api/export/pdf")
async def export_pdf():
    """Export current HTML as PDF"""
    try:
        html_content = llm_service.current_html
        if not html_content:
            raise HTTPException(400, "No content to export")
            
        # Create PDF in memory
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
        
        if pisa_status.err:
            raise HTTPException(500, "PDF generation failed")
            
        pdf_content = pdf_buffer.getvalue()
        pdf_buffer.close()
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=document.pdf"}
        )
    except Exception as e:
        raise HTTPException(500, f"Export failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=BACKEND_PORT)
