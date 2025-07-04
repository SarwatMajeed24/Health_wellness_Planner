from context import UserSessionContext
from hooks import RunHooks
import google.generativeai as genai

class MealPlannerTool:
    def generate_meal_plan(self, context: UserSessionContext) -> str:
        RunHooks.on_tool_start(context, "MealPlannerTool")
        prompt = f"Generate a 7-day meal plan for a user with diet preferences: {context.diet_preferences or 'none'} and goal: {context.goal or 'general health'}."
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            if response.text:
                meal_plan = response.text
                context.meal_plan = meal_plan.split("\n")
                RunHooks.on_tool_end(context, "MealPlannerTool")
                return f"\n7-Day Meal Plan:\n{meal_plan}"
            else:
                raise ValueError("Empty response from Gemini API")
        except Exception as e:
            error_message = f"Error generating meal plan: {str(e)}. Using fallback plan."
            print(error_message)
            fallback_plan = """
            Day 1: Breakfast - Oatmeal, Lunch - Salad, Dinner - Grilled vegetables
            Day 2: Breakfast - Smoothie, Lunch - Quinoa bowl, Dinner - Lentil soup
            Day 3: Breakfast - Yogurt, Lunch - Veggie wrap, Dinner - Stir-fry
            Day 4: Breakfast - Toast, Lunch - Chickpea salad, Dinner - Pasta
            Day 5: Breakfast - Pancakes, Lunch - Soup, Dinner - Tofu curry
            Day 6: Breakfast - Fruit bowl, Lunch - Hummus wrap, Dinner - Rice bowl
            Day 7: Breakfast - Cereal, Lunch - Veggie burger, Dinner - Salad
            """
            context.meal_plan = fallback_plan.split("\n")
            RunHooks.on_tool_end(context, "MealPlannerTool")
            return f"\n7-Day Meal Plan (Fallback):\n{fallback_plan}"