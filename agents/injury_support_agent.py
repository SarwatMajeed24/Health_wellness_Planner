from context import UserSessionContext
from hooks import RunHooks
import google.generativeai as genai

class InjurySupportAgent:
    def handle_injury_query(self, user_input: str, context: UserSessionContext) -> str:
        RunHooks.on_agent_start(context, "InjurySupportAgent")
        prompt = f"Provide injury support advice for a user with query: {user_input} and injury notes: {context.injury_notes or 'none'}."
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        context.injury_notes = user_input
        RunHooks.on_agent_end(context, "InjurySupportAgent")
        return response.text