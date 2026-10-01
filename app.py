import streamlit as st
import os
import sys

# Ensure project root in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from resume.parser import ResumeParser
from resume.cleaner import ResumeCleaner
from database.db_handler import DatabaseHandler

# Set Streamlit page configurations
st.set_page_config(
    page_title="Smart Career Recommendation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to inject custom branding CSS
def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = os.path.join(current_dir, "assets", "custom.css")
load_css(css_path)

# Enhanced Premium Styling for the 5 Interactive Workflow Cards
st.markdown("""
<style>
/* Override Streamlit button styles completely for the workflow columns */
div[data-testid="stColumn"] div.stButton > button,
div[data-testid="stColumn"] button[kind="secondary"],
div[data-testid="stColumn"] button[data-testid="baseButton-secondary"],
div[data-testid="stColumn"] button[data-testid="stBaseButton-secondary"] {
    background: linear-gradient(145deg, #1E2338 0%, #121626 100%) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    border-radius: 14px !important;
    min-height: 215px !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    text-align: center !important;
    padding: 24px 14px !important;
    color: #FFFFFF !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35) !important;
    cursor: pointer !important;
}

div[data-testid="stColumn"] div.stButton > button:hover,
div[data-testid="stColumn"] button[kind="secondary"]:hover,
div[data-testid="stColumn"] button[data-testid="baseButton-secondary"]:hover,
div[data-testid="stColumn"] button[data-testid="stBaseButton-secondary"]:hover {
    border-color: #818CF8 !important;
    background: linear-gradient(145deg, #2D3558 0%, #1B213D 100%) !important;
    transform: translateY(-6px) scale(1.02) !important;
    box-shadow: 0 16px 35px -5px rgba(99, 102, 241, 0.55), 0 0 20px rgba(99, 102, 241, 0.3) !important;
}

div[data-testid="stColumn"] div.stButton > button p {
    font-family: "Outfit", sans-serif !important;
    color: #94A3B8 !important;
    font-size: 0.85rem !important;
    line-height: 1.5 !important;
    margin: 0 !important;
}

div[data-testid="stColumn"] div.stButton > button strong {
    color: #FFFFFF !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    display: block !important;
    margin-top: 6px !important;
    margin-bottom: 6px !important;
    letter-spacing: -0.01em !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State variables across pages
if "resume_id" not in st.session_state:
    st.session_state["resume_id"] = None
if "resume_filename" not in st.session_state:
    st.session_state["resume_filename"] = None
if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""
if "extracted_skills" not in st.session_state:
    st.session_state["extracted_skills"] = []
if "recommended_jobs" not in st.session_state:
    st.session_state["recommended_jobs"] = []
if "selected_job" not in st.session_state:
    st.session_state["selected_job"] = None

# ==========================================
# NATIVE SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 15px;'>
    <h2 style='color: #6366F1; margin-bottom: 5px; font-family: "Outfit", sans-serif; font-weight: 800; letter-spacing: -0.02em;'>SmartCareer</h2>
    <p style='color: #64748B; font-size: 0.85rem; font-family: "Outfit", sans-serif; font-weight: 500;'>Data-Driven Recommendation & Verification</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div style='color: #64748B; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px; font-family: \"Outfit\";'>MODULES LINK</div>", unsafe_allow_html=True)

if st.sidebar.button("🏠 Home", use_container_width=True, type="primary"):
    st.switch_page("app.py")

if st.sidebar.button("📄 1. Upload Resume", use_container_width=True):
    st.switch_page("pages/1_Upload_Resume.py")

if st.sidebar.button("🧠 2. Extract Skills", use_container_width=True):
    st.switch_page("pages/2_Extract_Skills.py")

if st.sidebar.button("🔍 3. Live Match", use_container_width=True):
    st.switch_page("pages/3_Live_Jobs.py")

if st.sidebar.button("🛡️ 4. Verify Job", use_container_width=True):
    st.switch_page("pages/4_Verify_Job.py")

if st.sidebar.button("📊 5. Dashboard", use_container_width=True):
    st.switch_page("pages/5_Dashboard.py")
# ==========================================

# Main Content
st.markdown('<div class="gradient-header">Smart Career Recommendation</div>', unsafe_allow_html=True)
st.markdown('<div style="color:#A5B4FC; font-weight:700; font-size:1.15rem; letter-spacing:0.02em; margin-bottom: 25px;">USING DATA-DRIVEN INTELLIGENCE & MACHINE LEARNING</div>', unsafe_allow_html=True)

st.markdown("""
Welcome to the **Smart Career Recommendation and Job Verification System**. This application is engineered to assist job seekers in finding matching careers based on their resume skills, and verifying the authenticity of job listings to protect candidates from recruitment scams.
""")

# Interactive Premium Clickable Workflow Cards
st.markdown('<div class="gradient-subheader">System Workflow Steps (Click any box to open)</div>', unsafe_allow_html=True)

w_col1, w_col2, w_col3, w_col4, w_col5 = st.columns(5)

with w_col1:
    if st.button("📄\n\n**1. Upload Resume**\n\nUpload CV in PDF format for automated text parsing.", key="card_step_1", use_container_width=True):
        st.switch_page("pages/1_Upload_Resume.py")

with w_col2:
    if st.button("🧠\n\n**2. Extract Skills**\n\nMine technical competencies using NLP pipelines.", key="card_step_2", use_container_width=True):
        st.switch_page("pages/2_Extract_Skills.py")

with w_col3:
    if st.button("🔍\n\n**3. Live Match**\n\nSearch real openings matching your skills.", key="card_step_3", use_container_width=True):
        st.switch_page("pages/3_Live_Jobs.py")

with w_col4:
    if st.button("🛡️\n\n**4. Verify Job**\n\nVerify postings using Machine Learning models.", key="card_step_4", use_container_width=True):
        st.switch_page("pages/4_Verify_Job.py")

with w_col5:
    if st.button("📊\n\n**5. Dashboard**\n\nMonitor predictions and historical audit logs.", key="card_step_5", use_container_width=True):
        st.switch_page("pages/5_Dashboard.py")

st.markdown('---')
st.markdown('<div class="gradient-subheader">Start Here: Step 1 (Upload Resume)</div>', unsafe_allow_html=True)

col_upload, col_upload_stats = st.columns([2, 1])
db = DatabaseHandler()

with col_upload:
    uploaded_file = st.file_uploader("Choose your PDF resume", type=["pdf"], key="home_resume_uploader")
    
    if uploaded_file is not None:
        file_details = {
            "FileName": uploaded_file.name,
            "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        st.markdown(f"""
        <div class="tech-card">
            <div class="card-title">📄 Selected File</div>
            <div class="card-desc">
                <strong>Name:</strong> {file_details['FileName']}<br>
                <strong>Size:</strong> {file_details['FileSize']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Parse and Preprocess Resume", type="primary", use_container_width=True):
            with st.spinner("Parsing PDF and extracting text..."):
                raw_text = ResumeParser.extract_text(uploaded_file)
                
            if raw_text:
                with st.spinner("Scrubbing text noise..."):
                    cleaned_text = ResumeCleaner.clean_text(raw_text)
                
                try:
                    resume_id = db.save_resume(uploaded_file.name, cleaned_text)
                    st.session_state["resume_id"] = resume_id
                    st.session_state["resume_filename"] = uploaded_file.name
                    st.session_state["resume_text"] = cleaned_text
                    
                    st.session_state["extracted_skills"] = []
                    st.session_state["recommended_jobs"] = []
                    st.session_state["selected_job"] = None
                    st.session_state["last_verification_result"] = None
                    
                    st.success(f"🎉 Success! Resume preprocessed & saved (ID: {resume_id}).")
                except Exception as e:
                    st.error(f"Failed to log resume details: {e}")
            else:
                st.error("Failed to parse text from PDF. Make sure the file is not corrupted.")

with col_upload_stats:
    if st.session_state["resume_id"]:
        st.markdown(f"""
        <div class="tech-card job-authentic">
            <div class="card-title" style="color: #10B981;">✅ Resume Processed</div>
            <div class="card-desc" style="font-size: 0.9rem;">
                <strong>ID:</strong> {st.session_state['resume_id']}<br>
                <strong>File:</strong> {st.session_state['resume_filename']}<br>
                <strong>Next:</strong> Proceed to Extract Skills!
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("Proceed to Step 2: Extract Skills ➔", type="primary", use_container_width=True):
            st.switch_page("pages/2_Extract_Skills.py")
    else:
        st.markdown("""
        <div class="tech-card" style="opacity: 0.5;">
            <div class="card-title">⏳ Waiting...</div>
            <div class="card-desc" style="font-size: 0.9rem;">
                Upload a resume PDF to activate the next guided step.
            </div>
        </div>
        """, unsafe_allow_html=True)