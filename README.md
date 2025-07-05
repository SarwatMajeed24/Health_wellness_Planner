# Health & Wellness Planner Agent
This AI-powered health and wellness planner, built with Streamlit and the Gemini 2.0 Flash API, provides personalized or general fitness and dietary plans, schedules, and progress tracking. Users enter a query, choose between personalized (requires name, age, height, weight) or general responses, and receive tailored guidance through a web UI or CLI. Deployed at healthwellnessplanner-7yyouofdmebabqpclesnck.streamlit.app.
**Repository:** [github.com/your-username/health-wellness-planner]
## Setup

1- **Create Virtual Environment:**
```bash
python -m venv .venv

```bash
.\.venv\Scripts\activate
```

2- **Install Dependencies:**
```bash
pip install -r requirements.txt
```

3-**Create a .env File (for local testing):Create a .env file in the project root with your Gemini API key:**

```plaintext
GOOGLE_API_KEY=your_gemini_api_key_here

```

4- **Run the Application:**

**Streamlit**
```bash

 UI:streamlit run main.py

```

**CLI:**
```bash

python cli.py

```

## Features

- **Natural Language Interaction: Enter a query (e.g., "I want to lose 5kg in 2 months"), then choose personalized or general response.**
- **Personalization Option: Provide name, age, height, weight for tailored plans; skip for general advice.**
- **Goal Analysis: Personalized or general goal plans in a green box.**
- **Workout Planning: Tailored workout plans in a red box.**
- **Meal Planning: Customized meal plans in a blue box.**
- **Scheduling: Workout or meal schedules in a yellow box using scheduler.py.**
- **Progress Tracking: Activity logs and summaries in a purple box using tracker.py.**
- **Context Management: Stores user details and session context in UserSessionContext.**
- **Input/Output Guardrails: Validates inputs and ensures safe responses.**
- **Agent Handoff: Routes queries to specialized agents for nutrition (NutritionExpertAgent), injury support (InjurySupportAgent), or escalation (EscalationAgent).**
- **Real-Time Streaming: Displays responses in real-time.**
- **Streamlit UI:**
  - **Accessibility: Input fields include non-empty labels, with query input label hidden for visual consistency but accessible for screen readers.**
  - **Optional Theme Toggle: Switch between Light Mode (vibrant green-blue-purple gradient) and Dark Mode (dark gray-blue gradient) via a sidebar selectbox (if enabled).**
  - Developer credit "Developed by Sarwat Majeed" below the title in bold, colorful text.
  - Query-first input, followed by personalization choice (radio buttons).
  - Form for name, age, height, weight if personalized is chosen.
  - Separate boxes for Goal Plan, Workout Plan, Meal Plan, Schedule, and Progress Tracking.
  - Dedicated sidebar links (e.g., "View Goal Plan", "View Schedule") with single-click "Close ❌" buttons.
  - Blue PDF download button with Unicode support, including user details and all components.
  - Emojis for enhanced user experience (🥗🚀📋📥📜❌⚠️📭).


- **CLI Interface:**
  - Prompts for query, then personalization choice (1 for Personalized, 2 for General).
  - Colorful output using colorama with distinct headings for each component.
  - Commands: Enter queries, history to view categorized interactions, or exit to quit.


**Error Handling: Robust handling for API errors, invalid inputs, and PDF generation with Unicode support.**

## Deployment on Streamlit Cloud

1. Push the repository to GitHub, ensuring `.env` is not included (listed in `.gitignore`). 
2. In Streamlit Cloud:
    - Create a new app, selecting your repository (`health-wellness-planner`), branch (`main`), and main module (`main.py`). 
   - Add `GOOGLE_API_KEY` to secrets:
      ```toml
      GOOGLE_API_KEY = "your_gemini_api_key_here" >> README.md
      ``` 
    - Save and reboot the app. 
3. Deploy and access the app at [healthwellnessplanner-7yyouofdmebabqpclesnck.streamlit.app](https://healthwellnessplanner-7yyouofdmebabqpclesnck.streamlit.app)

## Folder Structure

 - `main.py`: Streamlit UI with accessibility fixes and optional theme toggle.
 - `cli.py`: CLI for text-based interactions.
 - `agent.py`: Main `HealthWellnessAgent` class for query processing.
 - `context.py`: Manages user session context (`UserSessionContext`).
 - `guardrails.py`: Input/output validation logic.
 - `hooks.py`: Lifecycle hooks for logging agent events.
 - `tools/`: 
   - `scheduler.py`: Generates schedules for workouts or meals.
   - `tracker.py`: Tracks user progress (e.g., workout completion, metrics). 
   - Other tools for goal analysis, meal planning, workout recommendations.
 - `agents/`: Specialized agents for nutrition, injury support, and escalation.
 - `utils/`: Streaming utility for real-time response display.
 - `requirements.txt`: Lists dependencies for deployment.
 - `.gitignore`: Excludes `.env`, `.venv/`, `__pycache__/`, `*.pyc`. 

 ## Testing >> README.md

- **Streamlit UI**: 
  - Run `streamlit run main.py` and open in browser (e.g., `http://localhost:8503`). 
  - Test query input (e.g., "I want to lose 5kg"), select Personalized (enter Name: Sarwat, Age: 25, Height: 165 cm, Weight: 70 kg) or General. 
     - If theme toggle is enabled, switch between Light and Dark modes.
   - Verify colorful boxes, sidebar links, single-click close buttons, PDF download, and no accessibility warnings.
 - **CLI**:
   - Run `python cli.py` and test queries, personalization, `history`, and `exit` commands.
   - Confirm colorful output with distinct headings.
 - **Streamlit Cloud**:
   - Deploy and test the app online, ensuring all features work. >>
   - **Robustness**: >>
  - Test with invalid API key (should handle gracefully). 
  - Test missing user details (General option should work).
   - Check for errors in terminal or browser console.

## Dependencies

- `streamlit==1.38.0`
- `google-generativeai==0.8.3` 
- `pydantic==2.9.2` 
- `python-dotenv==1.0.1` 
- `fpdf==1.7.2` 
- `colorama==0.4.6` 

## Notes

- Ensure a valid `GOOGLE_API_KEY` in `.env` locally or Streamlit Cloud secrets for deployment.
- `.env` must not be included in the GitHub repository (handled by `.gitignore`). 
- Fixed local `ModuleNotFoundError` for `streamlit` and `dotenv` by setting up virtual environment and `requirements.txt`. 
- Fixed deployment issues: Poetry errors, Google metadata timeout, and `GOOGLE_API_KEY` missing in Streamlit Cloud secrets.
- The project does not save PDF files locally; downloads are handled in memory.
- No handoff logs are displayed in the UI for a clean history view.

## Developer

Developed by **Sarwat Majeed**. >> README.md