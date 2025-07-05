Health & Wellness Planner Agent
This Streamlit-based and CLI-based AI-powered health and wellness planner uses the Gemini 2.0 Flash API to provide personalized or general health guidance. Users first enter a query, then choose between personalized (requires name, age, height, weight) or general responses to receive tailored fitness and dietary plans, schedule tasks, track progress, and access specialized advice for nutrition or injury concerns.
Repository: github.com/your-username/health-wellness-planner
Setup

Install uv:
pip install uv


Install Dependencies:
uv pip install google-generativeai streamlit pydantic python-dotenv fpdf colorama


Create a .env File:Create a .env file in the project root with your Gemini API key:
GOOGLE_API_KEY=your_gemini_api_key_here


Run the Application:

Streamlit UI:streamlit run main.py


CLI:python cli.py





Features

Natural Language Interaction: Enter a query (e.g., "I want to lose 5kg in 2 months"), then choose personalized or general response.
Personalization Option: Provide name, age, height, weight for tailored plans; skip for general advice.
Goal Analysis: Personalized or general goal plans in a green box.
Workout Planning: Tailored workout plans in a red box.
Meal Planning: Customized meal plans in a blue box.
Scheduling: Workout or meal schedules in a yellow box using scheduler.py.
Progress Tracking: Activity logs and summaries in a purple box using tracker.py.
Context Management: Stores user details and session context in UserSessionContext.
Input/Output Guardrails: Validates inputs and ensures safe responses.
Agent Handoff: Routes queries to specialized agents for nutrition, injury support, or escalation.
Real-Time Streaming: Displays responses in real-time.
Streamlit UI:
Vibrant multi-color gradient background (green, blue, purple).
Developer credit "Developed by Sarwat Majeed" below the title in bold, colorful text.
Query-first input, followed by personalization choice (radio buttons).
Form for name, age, height, weight if personalized is chosen.
Separate boxes for Goal Plan, Workout Plan, Meal Plan, Schedule, and Progress Tracking.
Dedicated sidebar links (e.g., "View Goal Plan", "View Schedule").
Smaller "Close" button above each history entry, hiding in one click.
Blue PDF download button with Unicode support, including user details and all components.
Emojis for enhanced user experience (e.g., 🥗, 📝, 🚀, 📥, 📜, 📋, ❌, ⚠️, 📭).


CLI Interface:
Prompts for query, then personalization choice (1 for Personalized, 2 for General).
Colorful output using colorama with distinct headings for each component.
Commands: Enter queries, history to view categorized interactions, or exit to quit.


Error Handling: Robust handling for API errors, invalid inputs, and PDF generation with Unicode support.

Folder Structure

main.py: Streamlit UI for web-based interactions.
cli.py: CLI for text-based interactions.
agent.py: Main HealthWellnessAgent class for query processing.
context.py: Manages user session context (UserSessionContext).
guardrails.py: Input/output validation logic.
hooks.py: Lifecycle hooks for logging agent events.
tools/:
scheduler.py: Generates schedules for workouts or meals.
tracker.py: Tracks user progress (e.g., workout completion, metrics).
Other tools for goal analysis, meal planning, workout recommendations.


agents/: Specialized agents for nutrition (NutritionExpertAgent), injury support (InjurySupportAgent), and escalation (EscalationAgent).
utils/: Streaming utility for real-time response display.

Usage
Streamlit UI

Run streamlit run main.py and open the app in your browser (e.g., http://localhost:8501).
View the "Health & Wellness Planner" title, followed by the developer credit "Developed by Sarwat Majeed" in bold, colorful text.
Enter a query (e.g., "I want to lose 5kg in 2 months").
Choose "Personalized Information" (enter name, age, height, weight) or "General Information".
View responses in separate boxes with headings (e.g., Goal Plan, Workout Plan, Schedule).
Access conversation history in the sidebar:
Click links like "View Goal Plan: Lose 5kg..." or "View Schedule: Weekly plan...".
Use the smaller "Close" button above each entry to hide it in one click.


Download a PDF progress report with user details and all components under respective headings.
Observe the vibrant multi-color gradient background and emojis.

CLI

Run python cli.py.
Enter a query at the colorful prompt (e.g., "Schedule my meals").
Choose 1 for Personalized (enter name, age, height, weight) or 2 for General.
View responses with headings (e.g., "Goal Plan", "Schedule").
Type history to view categorized history or exit to quit.
Colors:
Welcome and responses: Green (🌟, 📋).
Instructions and queries: Cyan and yellow.
History header: Magenta (📜).
Errors and exit: Red (⚠️, 📭, 👋).



Testing

Streamlit UI:
Test query input (e.g., "I want to lose 5kg"), then select Personalized (enter Name: Sarwat, Age: 25, Height: 165 cm, Weight: 70 kg) or General.
Test queries:
"I want to lose 5kg in 2 months" (Goal Plan, Workout Plan, Meal Plan).
"Schedule my workouts for the week" (Schedule).
"Track my cardio workout" (Progress Tracking).
"I have knee pain" (injury).
"I’m diabetic" (nutrition).


Verify separate boxes, sidebar links, single-click close button, and PDF with user details.


CLI:
Test query and personalization choice (1 or 2).
Test similar queries and commands (history, exit).
Confirm colorful output with distinct headings.


Robustness:
Test with an invalid API key to ensure fallback plans.
Test with missing user details (General option should work).
Check for errors in terminal or browser console.



Dependencies

google-generativeai: For Gemini API integration.
streamlit: For the web-based UI.
pydantic: For data validation.
python-dotenv: For environment variable management.
fpdf: For PDF report generation.
colorama: For colorful CLI output.

Notes

Ensure a valid GOOGLE_API_KEY in the .env file.
The project does not save PDF files locally; downloads are handled in memory.
No handoff logs are displayed in the UI to maintain a clean history view.
Scheduling (scheduler.py) and tracking (tracker.py) benefit from user details for personalized responses.

Developer
Developed by Sarwat Majeed.