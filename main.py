import streamlit as st
from agent import HealthWellnessAgent
from context import UserSessionContext
from dotenv import load_dotenv
from fpdf import FPDF
import io

# Initialize session state at the top
if "user_context" not in st.session_state:
    st.session_state.user_context = UserSessionContext(
        name="User", uid=1, age=None, height=None, weight=None, handoff_logs=[], progress_logs=[]
    )
if "query_submitted" not in st.session_state:
    st.session_state.query_submitted = False
if "current_query" not in st.session_state:
    st.session_state.current_query = ""
if "personalization_choice" not in st.session_state:
    st.session_state.personalization_choice = None
if "selected_history_index" not in st.session_state:
    st.session_state.selected_history_index = None
if "selected_history_type" not in st.session_state:
    st.session_state.selected_history_type = None

def clean_text(text):
    """Replace problematic Unicode characters with safe alternatives."""
    replacements = {
        '\u2013': '-',  # En dash to hyphen
        '\u2014': '--', # Em dash to double hyphen
        '\u2018': "'",  # Left single quote
        '\u2019': "'",  # Right single quote
        '\u2026': '...', # Ellipsis
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

def process_query(query, personalized):
    """Process and display response with categorization."""
    agent = HealthWellnessAgent(st.session_state.user_context)
    with st.spinner("Processing your request... ⏳"):
        if personalized:
            user_details = f"User: {st.session_state.user_context.name}, Age: {st.session_state.user_context.age or 'unknown'}, Height: {st.session_state.user_context.height or 'unknown'} cm, Weight: {st.session_state.user_context.weight or 'unknown'} kg. "
            full_query = user_details + query
        else:
            full_query = query
        response = agent.process_query(full_query)
        responses = []
        query_lower = query.lower()
        if "goal" in query_lower:
            responses.append({"type": "goal_plan", "content": response})
        if "workout" in query_lower or "exercise" in query_lower:
            responses.append({"type": "workout_plan", "content": response})
        if "meal" in query_lower or "diet" in query_lower:
            responses.append({"type": "meal_plan", "content": response})
        if "schedule" in query_lower or "plan" in query_lower:
            responses.append({"type": "schedule", "content": response})
        if "track" in query_lower or "progress" in query_lower:
            responses.append({"type": "track", "content": response})
        if not responses:
            responses.append({"type": "general", "content": response})

        for resp in responses:
            if resp["type"] == "goal_plan":
                st.markdown("### Goal Plan")
                st.markdown(f"<div class='goal-box'>{resp['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
            elif resp["type"] == "workout_plan":
                st.markdown("### Workout Plan")
                st.markdown(f"<div class='workout-box'>{resp['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
            elif resp["type"] == "meal_plan":
                st.markdown("### Meal Plan")
                st.markdown(f"<div class='meal-box'>{resp['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
            elif resp["type"] == "schedule":
                st.markdown("### Schedule")
                st.markdown(f"<div class='schedule-box'>{resp['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
            elif resp["type"] == "track":
                st.markdown("### Progress Tracking")
                st.markdown(f"<div class='track-box'>{resp['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
            else:
                st.markdown("### Response")
                st.markdown(f"<div class='response-box'>{resp['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
            st.session_state.user_context.progress_logs.append({
                "query": query,
                "type": resp["type"],
                "content": resp["content"]
            })

def main():
    # Load environment variables
    load_dotenv()
    
    st.set_page_config(page_title="Health & Wellness Planner", layout="wide")
    
    # Add custom CSS for vibrant styling
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            border-radius: 10px;
            padding: 10px;
            border: 2px solid #28a745;
            background-color: #d4edda;
        }
        .stNumberInput > div > div > input {
            border-radius: 10px;
            padding: 10px;
            border: 2px solid #28a745;
            background-color: #d4edda;
        }
        .stRadio > div {
            background-color: #f0f5ff;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #007bff;
        }
        .stButton > button {
            background-color: #28a745;
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #218838;
        }
        .stSpinner > div {
            color: #28a745;
        }
        .response-box {
            background-color: #e6f3ff;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #007bff;
            margin-top: 10px;
        }
        .goal-box {
            background-color: #f0fff4;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #28a745;
            margin-top: 10px;
        }
        .workout-box {
            background-color: #fff5f5;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #dc3545;
            margin-top: 10px;
        }
        .meal-box {
            background-color: #f0f5ff;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #007bff;
            margin-top: 10px;
        }
        .schedule-box {
            background-color: #fffbe6;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ffc107;
            margin-top: 10px;
        }
        .track-box {
            background-color: #f3e8ff;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #6f42c1;
            margin-top: 10px;
        }
        .history-button {
            background-color: #ffe5b4;
            color: #856404;
            border-radius: 5px;
            padding: 8px;
            margin: 5px 0;
            display: block;
            font-size: 14px;
        }
        .history-button:hover {
            background-color: #ffd700;
        }
        .close-button {
            background-color: #dc3545;
            color: white;
            border-radius: 5px;
            padding: 3px;
            margin: 3px 0;
            font-size: 12px;
            width: 80px;
        }
        .close-button:hover {
            background-color: #c82333;
        }
        .download-button {
            background-color: #007bff;
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }
        .download-button:hover {
            background-color: #0056b3;
        }
        .developer {
            text-align: center;
            margin: 10px 0;
            font-size: 18px;
            font-weight: bold;
            color: #6a1b9a;
        }
        .main {
            background: linear-gradient(to bottom, #c8e6c9, #bbdefb, #f3e5f5);
            padding: 20px;
            border-radius: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    st.title("🥗 Health & Wellness Planner")
    st.markdown('<div class="developer">Developed by Sarwat Majeed 🌟</div>', unsafe_allow_html=True)
    st.markdown("Enter your health-related question or goal, then choose personalization! 🌈")

    # Query input form
    with st.form(key="query_form"):
        st.markdown("📝 **Enter your query or goal:**")
        user_input = st.text_input("Enter your health query or goal", placeholder="e.g., I want to lose 5kg in 2 months", key="query_input", label_visibility="collapsed")
        submit_query = st.form_submit_button("Submit Query 🚀")
        if submit_query:
            if user_input:
                st.session_state.current_query = user_input
                st.session_state.query_submitted = True
                st.session_state.personalization_choice = None
            else:
                st.error("Please enter a valid question or goal. ⚠️")
                st.session_state.query_submitted = False

    # Personalization options
    if st.session_state.query_submitted and st.session_state.current_query:
        st.markdown("🎯 **Choose Response Type:**")
        st.session_state.personalization_choice = st.radio(
            "Do you want a personalized response or a general one?",
            ["Personalized Information", "General Information"],
            key="personalization_radio",
            label_visibility="visible"
        )

        if st.session_state.personalization_choice == "Personalized Information":
            with st.form(key="user_details_form"):
                st.markdown("📋 **Enter Your Details**")
                name = st.text_input("Name", value=st.session_state.user_context.name, placeholder="e.g., Sarwat", label_visibility="visible")
                age = st.number_input("Age (years)", min_value=1, max_value=120, value=st.session_state.user_context.age or 30, step=1, label_visibility="visible")
                height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=st.session_state.user_context.height or 165.0, step=0.1, label_visibility="visible")
                weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=st.session_state.user_context.weight or 70.0, step=0.1, label_visibility="visible")
                submit_details = st.form_submit_button("Generate Personalized Response")
                if submit_details:
                    st.session_state.user_context.update_user_details(name=name, age=age, height=height, weight=weight)
                    process_query(st.session_state.current_query, personalized=True)
                    st.session_state.query_submitted = False
        elif st.session_state.personalization_choice == "General Information":
            with st.form(key="general_form"):
                submit_general = st.form_submit_button("Generate General Response")
                if submit_general:
                    process_query(st.session_state.current_query, personalized=False)
                    st.session_state.query_submitted = False

    # Sidebar for conversation history links
    with st.sidebar:
        st.subheader("📜 Conversation History")
        if st.session_state.user_context.progress_logs:
            for i, log in enumerate(st.session_state.user_context.progress_logs):
                label = f"View {log['type'].replace('_', ' ').title()}: {log['query'][:30]}... 📋"
                if st.button(label, key=f"history_{i}", help="Click to view this entry"):
                    st.session_state.selected_history_index = i
                    st.session_state.selected_history_type = log["type"]
                if st.session_state.get("selected_history_index", None) == i:
                    if st.button("Close ❌", key=f"close_{i}", help="Close this history entry"):
                        st.session_state.selected_history_index = None
                        st.session_state.selected_history_type = None
                    st.markdown(f"**You**: {log['query']}")
                    if log["type"] == "goal_plan":
                        st.markdown("### Goal Plan")
                        st.markdown(f"<div class='goal-box'>{log['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
                    elif log["type"] == "workout_plan":
                        st.markdown("### Workout Plan")
                        st.markdown(f"<div class='workout-box'>{log['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
                    elif log["type"] == "meal_plan":
                        st.markdown("### Meal Plan")
                        st.markdown(f"<div class='meal-box'>{log['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
                    elif log["type"] == "schedule":
                        st.markdown("### Schedule")
                        st.markdown(f"<div class='schedule-box'>{log['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
                    elif log["type"] == "track":
                        st.markdown("### Progress Tracking")
                        st.markdown(f"<div class='track-box'>{log['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("### Response")
                        st.markdown(f"<div class='response-box'>{log['content'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
        else:
            st.write("No conversation history yet. 📭")

    # PDF report download link
    if st.session_state.user_context.progress_logs:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Health & Wellness Progress Report", ln=True, align="C")
            pdf.cell(200, 10, txt=f"User: {st.session_state.user_context.name}", ln=True)
            pdf.cell(200, 10, txt=f"Age: {st.session_state.user_context.age or 'unknown'}", ln=True)
            pdf.cell(200, 10, txt=f"Height: {st.session_state.user_context.height or 'unknown'} cm", ln=True)
            pdf.cell(200, 10, txt=f"Weight: {st.session_state.user_context.weight or 'unknown'} kg", ln=True)
            current_type = None
            for log in st.session_state.user_context.progress_logs:
                if log["type"] != current_type:
                    pdf.cell(200, 10, txt=log["type"].replace("_", " ").title(), ln=True, align="L")
                    current_type = log["type"]
                pdf.cell(200, 10, txt=f"Query: {clean_text(log['query'])}", ln=True)
                pdf.multi_cell(200, 10, txt=clean_text(log['content']))
            pdf_output = io.BytesIO()
            pdf_output.write(pdf.output(dest="S").encode("latin-1", errors="replace"))
            pdf_output.seek(0)
            st.download_button(
                label="📥 Download Progress Report",
                data=pdf_output,
                file_name="progress_report.pdf",
                mime="application/pdf",
                key="download_pdf",
                help="Click to download your progress report as a PDF",
                use_container_width=True,
                type="primary"
            )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)} ⚠️")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()