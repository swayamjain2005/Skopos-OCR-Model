import requests
import os
import html
from config import CHANDRA_OCR_URL

class OCRService:
    def __init__(self):
        self.ocr_url = CHANDRA_OCR_URL

    def process_document(self, file_path: str) -> str:
        """Process document through Chandra OCR (Florence-2) and return HTML"""
        try:
            print(f"Sending file to OCR: {file_path}")
            print(f"Target URL: {self.ocr_url}")
            
            with open(file_path, "rb") as f:
                # Prepare the file and data payload
                # Note: 'file' matches the FastAPI endpoint argument name
                files = {"file": (os.path.basename(file_path), f, "image/jpeg")}
                data = {"task_prompt": "<OCR>"} 
                
                response = requests.post(self.ocr_url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("OCR processing successful")
                
                # Extract the generated text
                # The API returns {"filename": ..., "result": parsed_answer}
                ocr_result = result.get("result", "")
                
                # Handle dictionary output from Florence-2 post-processing
                if isinstance(ocr_result, dict):
                    # Extract values from dictionary (e.g. {'<OCR>': 'text...'})
                    text_content = "\n".join([str(v) for v in ocr_result.values()])
                else:
                    text_content = str(ocr_result)
                
                return self._text_to_html(text_content, os.path.basename(file_path))
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                print(error_msg)
                return self._error_html(error_msg)
                
        except Exception as e:
            print(f"OCR processing error: {e}")
            return self._error_html(str(e))

    def _text_to_html(self, text: str, filename: str) -> str:
        """Convert raw OCR text to formatted HTML"""
        # Escape HTML characters to prevent injection/breakage
        safe_text = html.escape(text)
        
        lines = safe_text.split('\n')
        html_lines = [f"<p>{line}</p>" for line in lines if line.strip()]
        content = "\n".join(html_lines)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OCR Result</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; padding: 40px; max-width: 800px; margin: 0 auto; background: #fff; color: #333; }}
        .header {{ border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; color: #2c3e50; font-size: 24px; }}
        .meta {{ color: #7f8c8d; font-size: 14px; margin-top: 5px; }}
        .content {{ white-space: pre-wrap; background: #f9f9f9; padding: 30px; border-radius: 8px; border: 1px solid #eee; }}
        p {{ margin-bottom: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Document Content</h1>
        <div class="meta">Source File: {filename}</div>
    </div>
    <div class="content">
        {content}
    </div>
</body>
</html>"""

    def _error_html(self, error: str) -> str:
        return f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: sans-serif; padding: 50px; text-align: center; color: #721c24; background-color: #f8d7da; }}
        .error-box {{ border: 1px solid #f5c6cb; padding: 20px; border-radius: 5px; background: white; display: inline-block; }}
    </style>
</head>
<body>
    <div class="error-box">
        <h2>OCR Processing Failed</h2>
        <p>{error}</p>
        <p>Please check the backend logs and ensure the OCR service is running.</p>
    </div>
</body>
</html>"""
