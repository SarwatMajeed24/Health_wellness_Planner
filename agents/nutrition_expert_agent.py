from context import UserSessionContext
from hooks import RunHooks
import google.generativeai as genai

class NutritionExpertAgent:
    def handle_nutrition_query(self, user_input: str, context: UserSessionContext) -> str:
        RunHooks.on_agent_start(context, "NutritionExpertAgent")
        prompt = f"Provide nutrition advice for a user with query: {user_input} and preferences: {context.diet_preferences or 'none'}."
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        RunHooks.on_agent_end(context, "NutritionExpertAgent")
        return response.text