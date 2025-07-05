from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
from context import UserSessionContext

class HealthWellnessAgent:
    def __init__(self, context: UserSessionContext):
        self.context = context
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = GenerativeModel("gemini-2.0-flash")
    
    def process_query(self, query: str) -> str:
        """Process user query with context and return response."""
        # Build prompt with user details
        prompt = f"""
        You are a health and wellness planner. Use the following user details to personalize the response if provided:
        Name: {self.context.name}
        Age: {self.context.age or 'unknown'}
        Height: {self.context.height or 'unknown'} cm
        Weight: {self.context.weight or 'unknown'} kg
        Query: {query}
        
        Provide a concise, personalized response if details are available; otherwise, provide a general response. For goals, include a plan. For schedules, use scheduler tools. For tracking, log progress.
        """
        try:
            response = self.model.generate_content(prompt).text
        except Exception as e:
            response = f"Error processing query: {str(e)}"
        return response