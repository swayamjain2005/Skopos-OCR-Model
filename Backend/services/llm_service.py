import google.generativeai as genai
from config import GEMINI_API_KEY

class LLMService:
    def __init__(self):
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-flash-latest')
            self.chat_session = None
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            self.model = None
            
        self.current_html = ""
    
    def set_html(self, html: str):
        """Set the current HTML document"""
        self.current_html = html
        self.chat_session = self.model.start_chat(history=[])
        
        # Initialize context
        initial_prompt = f"""You are an HTML editing assistant. The user has a document converted to HTML.
Current HTML:
{self.current_html}

When the user asks for changes, respond with:
1. A brief explanation of what you'll change
2. The complete modified HTML

Format your response as:
EXPLANATION: <your explanation>
HTML: <complete modified html>"""
        
        try:
            self.chat_session.send_message(initial_prompt)
        except Exception as e:
            print(f"Error starting chat: {e}")
    
    def chat(self, user_message: str) -> dict:
        """Process user message and return response with updated HTML"""
        if not self.model:
            return {"message": "LLM not initialized", "html": self.current_html}
            
        try:
            if not self.chat_session:
                self.set_html(self.current_html)
                
            response = self.chat_session.send_message(user_message)
            response_text = response.text
            
            # Parse response
            explanation = ""
            updated_html = self.current_html
            
            if "EXPLANATION:" in response_text and "HTML:" in response_text:
                parts = response_text.split("HTML:")
                explanation = parts[0].replace("EXPLANATION:", "").strip()
                updated_html = parts[1].strip()
                # Clean up markdown code blocks if present
                if updated_html.startswith("```html"):
                    updated_html = updated_html.replace("```html", "", 1)
                if updated_html.startswith("```"):
                    updated_html = updated_html.replace("```", "", 1)
                if updated_html.endswith("```"):
                    updated_html = updated_html[:-3]
                
                self.current_html = updated_html.strip()
            else:
                explanation = response_text
            
            return {
                "message": explanation,
                "html": updated_html
            }
        except Exception as e:
            print(f"Chat error: {e}")
            return {
                "message": f"Error processing request: {str(e)}",
                "html": self.current_html
            }

    def generate_html_from_text(self, text: str, filename: str) -> str:
        """Generate structured HTML from raw text using LLM"""
        if not self.model:
            return text
            
        prompt = f"""You are an expert document formatter. Your task is to convert the following text (which is raw OCR output) into a clean, structured HTML document that PRESERVES THE ORIGINAL LAYOUT AND FORMATTING as much as possible.
        
        Filename: {filename}
        
        Input Text:
        {text}
        
        Instructions:
        1. **Preserve Layout**: Try to maintain the visual structure of the original document. If it looks like a form, use tables or grid layouts. If it's a letter, maintain the header/footer positioning.
        2. **Semantic HTML**: Use appropriate tags (<h1>-<h6>, <table>, <ul>, <ol>, <p>, <div>).
        3. **Styling**: Use inline CSS to make it look professional and similar to the original. 
           - Use fonts like 'Arial', 'Helvetica', or 'Times New Roman' where appropriate.
           - Add padding, margins, and borders to separate sections.
           - For tables, ensure borders are visible if they were in the original (or if it helps readability).
        4. **Tables**: If the input contains tabular data, you MUST format it as an HTML <table> with proper headers (<th>) and rows (<tr>). Add `border-collapse: collapse; width: 100%;` to tables.
        5. **No Markdown**: Do NOT include any markdown code blocks (like ```html). Just return the raw HTML code.
        6. **Complete Document**: Ensure the HTML is complete with <html>, <head>, and <body> tags.
        7. **Inference**: Infer the document type (e.g., Invoice, Resume, Report) and apply standard styling for that type.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Safely extract text from response
            if response.candidates and response.candidates[0].content.parts:
                html_content = response.candidates[0].content.parts[0].text
            else:
                # Fallback or check for safety blocks
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    print(f"Response blocked: {response.prompt_feedback.block_reason}")
                    return text
                html_content = response.text # This might still raise if blocked, but we handled common block cases
            
            # Clean up markdown if present
            if html_content.startswith("```html"):
                html_content = html_content.replace("```html", "", 1)
            if html_content.startswith("```"):
                html_content = html_content.replace("```", "", 1)
            if html_content.endswith("```"):
                html_content = html_content[:-3]
                
            return html_content.strip()
        except Exception as e:
            print(f"Error generating HTML: {e}")
            return text
