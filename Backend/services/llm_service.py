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
            
        prompt = f"""You are an expert document formatter. Convert the following text (which might be raw OCR output or basic HTML) into a clean, structured, and visually appealing HTML document.
        
        Filename: {filename}
        
        Input Text:
        {text}
        
        Instructions:
        1. Analyze the text to identify headers, tables, lists, and key-value pairs.
        2. Create a modern, clean HTML structure using semantic tags.
        3. Use inline CSS for styling to make it look professional (like a real document, e.g., a mark sheet, invoice, or report).
        4. If there are tables, format them properly with borders, padding, and distinct headers.
        5. Do NOT include any markdown code blocks (like ```html). Just return the raw HTML code.
        6. Ensure the HTML is complete with <html>, <head>, and <body> tags.
        7. If the input is already HTML, improve its structure and styling.
        """
        
        try:
            response = self.model.generate_content(prompt)
            html_content = response.text
            
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
