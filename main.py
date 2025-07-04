import streamlit as st
from agent import HealthWellnessAgent
from context import UserSessionContext
from dotenv import load_dotenv
from fpdf import FPDF
import os
import io

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
    st.markdown("Ask any health-related question or set fitness/dietary goals! 🌈")

    # Initialize session state for context
    if "user_context" not in st.session_state:
        st.session_state.user_context = UserSessionContext(
            name="User", uid=1, handoff_logs=[], progress_logs=[]
        )
    if "selected_history_index" not in st.session_state:
        st.session_state.selected_history_index = None

    # Input form
    st.markdown("📝 **Enter your query or goal:**")
    user_input = st.text_input("", placeholder="e.g., I want to lose 5kg in 2 months")
    if st.button("Submit 🚀"):
        if user_input:
            agent = HealthWellnessAgent(st.session_state.user_context)
            with st.spinner("Processing your request... ⏳"):
                response = agent.process_query(user_input)
                # Format response with markdown
                st.markdown(f"<div class='response-box'>{response.replace('\n', '<br>')}</div>", unsafe_allow_html=True)
                # Update context with progress
                st.session_state.user_context.progress_logs.append({"query": user_input, "response": response})
                # Reset selected history to avoid confusion
                st.session_state.selected_history_index = None
        else:
            st.error("Please enter a valid question or goal. ⚠️")

    # PDF report download link
    if st.session_state.user_context.progress_logs:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Health & Wellness Progress Report", ln=True, align="C")
            for log in st.session_state.user_context.progress_logs:
                pdf.cell(200, 10, txt=f"Query: {clean_text(log['query'])}", ln=True)
                pdf.multi_cell(200, 10, txt=clean_text(log['response']))
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

    # Sidebar for conversation history links
    with st.sidebar:
        st.subheader("📜 Conversation History")
        if st.session_state.user_context.progress_logs:
            for i, log in enumerate(st.session_state.user_context.progress_logs):
                if st.button(f"View: {log['query'][:30]}... 📋", key=f"history_{i}", help="Click to view this query and response"):
                    st.session_state.selected_history_index = i
                # Display selected history entry with close button on top
                if st.session_state.selected_history_index == i:
                    if st.button("Close ❌", key=f"close_{i}", help="Close this history entry"):
                        st.session_state.selected_history_index = None
                    st.markdown(f"**You**: {log['query']}")
                    st.markdown(f"<div class='response-box'>{log['response'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
        else:
            st.write("No conversation history yet. 📭")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()


