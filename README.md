Health & Wellness Planner Agent
This Streamlit-based and CLI-based AI-powered health and wellness planner uses the Gemini 2.0 Flash API to provide personalized health guidance. Users can set fitness and dietary goals, receive tailored meal and workout plans, and access specialized advice for nutrition or injury concerns.
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

Natural Language Interaction: Ask health-related questions or set fitness/dietary goals (e.g., "I want to lose 5kg in 2 months").
Goal Analysis: Personalized meal and workout plans generated based on user goals.
Context Management: Maintains user session context for multi-turn interactions.
Input/Output Guardrails: Validates user inputs and ensures safe responses.
Agent Handoff: Routes queries to specialized agents for nutrition, injury support, or escalation to a human trainer.
Real-Time Streaming: Displays responses in real-time using streaming utilities.
Streamlit UI:
Vibrant multi-color gradient background (green, blue, purple).
Developer credit "Developed by Sarwat Majeed" below the title in bold, colorful text.
Individual conversation history links in the sidebar with a smaller "Close" button above each entry, hiding entries in one click.
Blue PDF download button with Unicode support for progress reports.
Emojis for enhanced user experience (e.g., 🥗, 📝, 🚀, 📥, 📜, 📋, ❌, ⚠️, 📭).


CLI Interface:
Colorful output using colorama for prompts, responses, and history (green, cyan, yellow, magenta, red).
Commands: Enter queries, type history to view past interactions, or exit to quit.


Error Handling: Robust handling for API errors and PDF generation with Unicode character support.

Folder Structure

main.py: Streamlit UI for web-based interactions.
cli.py: CLI for text-based interactions.
agent.py: Main HealthWellnessAgent class for query processing.
context.py: Manages user session context (UserSessionContext).
guardrails.py: Input/output validation logic.
hooks.py: Lifecycle hooks for logging agent events.
tools/: Tools for goal analysis, meal planning, workout recommendations, scheduling, and progress tracking.
agents/: Specialized agents for nutrition (NutritionExpertAgent), injury support (InjurySupportAgent), and escalation (EscalationAgent).
utils/: Streaming utility for real-time response display.

Usage
Streamlit UI

Run streamlit run main.py and open the app in your browser (e.g., http://localhost:8501).
View the "Health & Wellness Planner" title at the top, followed by the developer credit "Developed by Sarwat Majeed" in bold, colorful text.
Enter health-related questions or goals in the input field (e.g., "I want to lose 5kg in 2 months").
View conversation history in the sidebar:
Click individual query links to display entries.
Use the smaller "Close" button above each entry to hide it in one click.


Download a PDF progress report using the blue "Download Progress Report" button (Unicode-compatible).
Observe the vibrant multi-color gradient background and emojis for a user-friendly experience.

CLI

Run python cli.py.
Enter queries at the colorful prompt (e.g., "I want to lose 5kg in 2 months").
Type history to view conversation history in color or exit to quit.
Colors:
Welcome and responses: Green (🌟, 📋).
Instructions and queries: Cyan and yellow.
History header: Magenta (📜).
Errors and exit: Red (⚠️, 📭, 👋).



Testing

Streamlit UI:
Test queries like "I want to lose 5kg in 2 months" (goal plan), "I want to talk to a real trainer" (escalation), "tell me 7 days diet plan" (meal plan), "I have knee pain" (injury), "I’m diabetic" (nutrition).
Verify single-click close button, PDF download, and no handoff logs in the sidebar.


CLI:
Test similar queries and commands (history, exit).
Confirm colorful output.


Robustness:
Test with an invalid API key to ensure fallback plans.
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

Developer
Developed by Sarwat Majeed.