import os
import google.generativeai as genai
from context import UserSessionContext
from dotenv import load_dotenv

class HealthWellnessAgent:
    def __init__(self, user_context: UserSessionContext):
        self.user_context = user_context
        # Load environment variables
        load_dotenv()
        # Explicitly configure Gemini API with API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables or Streamlit secrets")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')  # Adjust model name as needed

    def process_query(self, query: str) -> str:
        try:
            # Process query using Gemini API
            response = self.model.generate_content(query)
            return response.text
        except Exception as e:
            return f"Error processing query: {str(e)}"
