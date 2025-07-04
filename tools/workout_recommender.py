from context import UserSessionContext
from hooks import RunHooks
import google.generativeai as genai

class WorkoutRecommenderTool:
    def generate_workout_plan(self, context: UserSessionContext) -> str:
        RunHooks.on_tool_start(context, "WorkoutRecommenderTool")
        prompt = f"Generate a 7-day workout plan for a user with goal: {context.goal or 'general fitness'} and injury notes: {context.injury_notes or 'none'}."
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            if response.text:
                workout_plan = response.text
                context.workout_plan = {"plan": workout_plan.split("\n")}
                RunHooks.on_tool_end(context, "WorkoutRecommenderTool")
                return f"\n7-Day Workout Plan:\n{workout_plan}"
            else:
                raise ValueError("Empty response from Gemini API")
        except Exception as e:
            error_message = f"Error generating workout plan: {str(e)}. Using fallback plan."
            print(error_message)
            fallback_plan = """
            Day 1: 30-min walk
            Day 2: Bodyweight squats, push-ups
            Day 3: Rest
            Day 4: Yoga
            Day 5: Light jogging
            Day 6: Stretching
            Day 7: Rest
            """
            context.workout_plan = {"plan": fallback_plan.split("\n")}
            RunHooks.on_tool_end(context, "WorkoutRecommenderTool")
            return f"\n7-Day Workout Plan (Fallback):\n{fallback_plan}"