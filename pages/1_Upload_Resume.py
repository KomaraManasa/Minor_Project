import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from resume.parser import ResumeParser
from resume.cleaner import ResumeCleaner
from database.db_handler import DatabaseHandler

def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = os.path.join(project_root, "assets", "custom.css")
load_css(css_path)

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

if st.sidebar.button("🏠 Home", use_container_width=True):
    st.switch_page("app.py")

if st.sidebar.button("📄 1. Upload Resume", use_container_width=True, type="primary"):
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

st.markdown('<div class="gradient-header">Upload Resume</div>', unsafe_allow_html=True)
st.markdown('<div style="color:#A5B4FC; font-weight:700; font-size:1.15rem; letter-spacing:0.02em; margin-bottom: 25px;">MODULE 1: EXTRACT & CLEAN TEXT FROM PDF</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a PDF resume file", type=["pdf"])
db = DatabaseHandler()

if uploaded_file is not None:
    file_details = {
        "FileName": uploaded_file.name, 
        "FileType": uploaded_file.type, 
        "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
    }
    
    st.markdown(f"""
    <div class="tech-card">
        <div class="card-title">📄 File Selected</div>
        <div class="card-desc">
            <strong>File Name:</strong> {file_details['FileName']}<br>
            <strong>File Size:</strong> {file_details['FileSize']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Parse and Preprocess Resume", type="primary", use_container_width=True):
        with st.spinner("Extracting text from PDF..."):
            raw_text = ResumeParser.extract_text(uploaded_file)
            
        if raw_text:
            with st.spinner("Cleaning text corpus..."):
                cleaned_text = ResumeCleaner.clean_text(raw_text)
            
            with st.spinner("Saving resume to secure database..."):
                try:
                    resume_id = db.save_resume(uploaded_file.name, cleaned_text)
                    st.session_state["resume_id"] = resume_id
                    st.session_state["resume_filename"] = uploaded_file.name
                    st.session_state["resume_text"] = cleaned_text
                    
                    st.session_state["extracted_skills"] = []
                    st.session_state["recommended_jobs"] = []
                    st.session_state["selected_job"] = None
                    
                    st.success(f"🎉 Success! Resume parsed and cleaned. Stored in Database (ID: {resume_id}).")
                except Exception as e:
                    st.error(f"Failed to save resume: {e}")
        else:
            st.error("Failed to extract text. Make sure the PDF is not corrupted.")

if st.session_state["resume_id"]:
    st.markdown('<div class="gradient-subheader">Active Resume Session</div>', unsafe_allow_html=True)
    
    col_details, col_action = st.columns([2, 1])
    with col_details:
        st.markdown(f"""
        <div class="tech-card" style="height: 100%;">
            <div class="card-title" style="color: #10B981;">✅ Processed File Details</div>
            <div class="card-desc">
                <strong>Database ID:</strong> {st.session_state['resume_id']}<br>
                <strong>Filename:</strong> {st.session_state['resume_filename']}<br>
                <strong>Status:</strong> Preprocessed & Ready for Skill Extraction
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_action:
        st.write("")
        st.write("")
        if st.button("Proceed to Step 2: Extract Skills ➔", type="primary", use_container_width=True):
            st.switch_page("pages/2_Extract_Skills.py")
            