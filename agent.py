import os
import google.generativeai as genai
from tools.goal_analyzer import GoalAnalyzerTool
from tools.meal_planner import MealPlannerTool
from tools.workout_recommender import WorkoutRecommenderTool
from agents.nutrition_expert_agent import NutritionExpertAgent
from agents.injury_support_agent import InjurySupportAgent
from agents.escalation_agent import EscalationAgent
from guardrails import validate_input, validate_output
from utils.streaming import stream_response
from context import UserSessionContext

class HealthWellnessAgent:
    def __init__(self, context: UserSessionContext):
        self.context = context
        self.goal_analyzer = GoalAnalyzerTool()
        self.meal_planner = MealPlannerTool()
        self.workout_recommender = WorkoutRecommenderTool()
        self.nutrition_expert = NutritionExpertAgent()
        self.injury_support = InjurySupportAgent()
        self.escalation_agent = EscalationAgent()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def process_query(self, user_input: str) -> str:
        # Input validation
        if not validate_input(user_input):
            return "Invalid input. Please provide a clear health-related question or goal."

        # Stream response for real-time interaction
        response = ""
        if "lose" in user_input.lower() or "gain" in user_input.lower():
            goal = self.goal_analyzer.analyze_goal(user_input, self.context)
            self.context.goal = goal
            response += f"Goal set: {goal['description']} (Target: {goal['quantity']} {goal['metric']} in {goal['duration']})"
            if self.context.diet_preferences:
                response += f"\nDiet Preference: {self.context.diet_preferences}"
            response += "\nGenerating a plan..."
            response += self.meal_planner.generate_meal_plan(self.context)
            response += self.workout_recommender.generate_workout_plan(self.context)
        elif "vegetarian" in user_input.lower() or "vegan" in user_input.lower():
            self.context.diet_preferences = user_input.lower()
            response += self.meal_planner.generate_meal_plan(self.context)
        elif "pain" in user_input.lower() or "injury" in user_input.lower():
            response += self.injury_support.handle_injury_query(user_input, self.context)
            self.context.handoff_logs.append(f"Handoff to InjurySupportAgent: {user_input}")
        elif "diabetic" in user_input.lower() or "nutrition" in user_input.lower():
            response += self.nutrition_expert.handle_nutrition_query(user_input, self.context)
            self.context.handoff_logs.append(f"Handoff to NutritionExpertAgent: {user_input}")
        elif "trainer" in user_input.lower():
            response += self.escalation_agent.handle_escalation(user_input, self.context)
            self.context.handoff_logs.append(f"Handoff to EscalationAgent: {user_input}")
        else:
            # General health question handled by Gemini API
            response += stream_response(self.model, user_input)

        # Output validation
        if not validate_output(response):
            return "Error processing response. Please try again."
        
        return response