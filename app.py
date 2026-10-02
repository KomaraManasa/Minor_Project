import streamlit as st
import os
import sys

# Add project folder to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from resume.parser import ResumeParser
from resume.cleaner import ResumeCleaner
from database.db_handler import DatabaseHandler


# Streamlit page settings
st.set_page_config(
    page_title="Smart Career Recommendation",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load custom CSS
def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


css_path = os.path.join(current_dir, "assets", "custom.css")
load_css(css_path)


# Style for workflow buttons
st.markdown("""
<style>
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
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35) !important;
    cursor: pointer !important;
}

div[data-testid="stColumn"] div.stButton > button:hover,
div[data-testid="stColumn"] button[kind="secondary"]:hover,
div[data-testid="stColumn"] button[data-testid="baseButton-secondary"]:hover,
div[data-testid="stColumn"] button[data-testid="stBaseButton-secondary"]:hover {
    border-color: #818CF8 !important;
    background: linear-gradient(145deg, #2D3558 0%, #1B213D 100%) !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 12px 25px rgba(99, 102, 241, 0.35) !important;
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
}
</style>
""", unsafe_allow_html=True)


# Values shared between pages
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


# Sidebar navigation
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 15px;'>
    <h2 style='color: #6366F1; margin-bottom: 5px; font-family: "Outfit", sans-serif; font-weight: 800;'>
        SmartCareer
    </h2>
    <p style='color: #64748B; font-size: 0.85rem; font-family: "Outfit", sans-serif;'>
        Job Recommendation and Verification
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    "<div style='color: #64748B; font-size: 0.75rem; font-weight: 700; "
    "margin-bottom: 10px; font-family: \"Outfit\";'>MENU</div>",
    unsafe_allow_html=True
)


if st.sidebar.button("Home", use_container_width=True, type="primary"):
    st.switch_page("app.py")

if st.sidebar.button("1. Upload Resume", use_container_width=True):
    st.switch_page("pages/1_Upload_Resume.py")

if st.sidebar.button("2. Extract Skills", use_container_width=True):
    st.switch_page("pages/2_Extract_Skills.py")

if st.sidebar.button("3. Live Match", use_container_width=True):
    st.switch_page("pages/3_Live_Jobs.py")

if st.sidebar.button("4. Verify Job", use_container_width=True):
    st.switch_page("pages/4_Verify_Job.py")

if st.sidebar.button("5. Dashboard", use_container_width=True):
    st.switch_page("pages/5_Dashboard.py")


# Main page
st.markdown(
    '<div class="gradient-header">Smart Career Recommendation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="color:#A5B4FC; font-weight:700; font-size:1.15rem; '
    'margin-bottom: 25px;">Resume-based job recommendation and verification</div>',
    unsafe_allow_html=True
)

st.markdown("""
This project helps users find jobs based on the skills in their resume
and check whether a job posting looks suspicious.
""")


# Workflow
st.markdown(
    '<div class="gradient-subheader">Project Workflow</div>',
    unsafe_allow_html=True
)

w_col1, w_col2, w_col3, w_col4, w_col5 = st.columns(5)


with w_col1:
    if st.button(
        "**1. Upload Resume**\n\nUpload your resume in PDF format.",
        key="card_step_1",
        use_container_width=True
    ):
        st.switch_page("pages/1_Upload_Resume.py")


with w_col2:
    if st.button(
        "**2. Extract Skills**\n\nExtract skills from the resume.",
        key="card_step_2",
        use_container_width=True
    ):
        st.switch_page("pages/2_Extract_Skills.py")


with w_col3:
    if st.button(
        "**3. Live Match**\n\nFind jobs based on your skills.",
        key="card_step_3",
        use_container_width=True
    ):
        st.switch_page("pages/3_Live_Jobs.py")


with w_col4:
    if st.button(
        "**4. Verify Job**\n\nCheck a job posting using the ML model.",
        key="card_step_4",
        use_container_width=True
    ):
        st.switch_page("pages/4_Verify_Job.py")


with w_col5:
    if st.button(
        "**5. Dashboard**\n\nView previous results.",
        key="card_step_5",
        use_container_width=True
    ):
        st.switch_page("pages/5_Dashboard.py")


st.markdown("---")

st.markdown(
    '<div class="gradient-subheader">Step 1: Upload Resume</div>',
    unsafe_allow_html=True
)


col_upload, col_upload_stats = st.columns([2, 1])

db = DatabaseHandler()


with col_upload:

    uploaded_file = st.file_uploader(
        "Choose your PDF resume",
        type=["pdf"],
        key="home_resume_uploader"
    )

    if uploaded_file is not None:

        file_details = {
            "FileName": uploaded_file.name,
            "FileSize": f"{uploaded_file.size / 1024:.2f} KB"
        }

        st.markdown(f"""
        <div class="tech-card">
            <div class="card-title">Selected File</div>
            <div class="card-desc">
                <strong>Name:</strong> {file_details['FileName']}<br>
                <strong>Size:</strong> {file_details['FileSize']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Parse and Preprocess Resume",
            type="primary",
            use_container_width=True
        ):

            with st.spinner("Reading resume..."):
                raw_text = ResumeParser.extract_text(uploaded_file)

            if raw_text:

                with st.spinner("Cleaning resume text..."):
                    cleaned_text = ResumeCleaner.clean_text(raw_text)

                try:

                    resume_id = db.save_resume(
                        uploaded_file.name,
                        cleaned_text
                    )

                    st.session_state["resume_id"] = resume_id
                    st.session_state["resume_filename"] = uploaded_file.name
                    st.session_state["resume_text"] = cleaned_text

                    st.session_state["extracted_skills"] = []
                    st.session_state["recommended_jobs"] = []
                    st.session_state["selected_job"] = None
                    st.session_state["last_verification_result"] = None

                    st.success(
                        f"Resume processed and saved. Resume ID: {resume_id}"
                    )

                except Exception as e:
                    st.error(f"Could not save resume details: {e}")

            else:
                st.error(
                    "Could not extract text from the PDF. "
                    "Please check the file and try again."
                )


with col_upload_stats:

    if st.session_state["resume_id"]:

        st.markdown(f"""
        <div class="tech-card job-authentic">
            <div class="card-title" style="color: #10B981;">
                Resume Processed
            </div>
            <div class="card-desc" style="font-size: 0.9rem;">
                <strong>ID:</strong> {st.session_state['resume_id']}<br>
                <strong>File:</strong> {st.session_state['resume_filename']}<br>
                <strong>Next:</strong> Extract skills from the resume.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button(
            "Go to Step 2: Extract Skills",
            type="primary",
            use_container_width=True
        ):
            st.switch_page("pages/2_Extract_Skills.py")

    else:

        st.markdown("""
        <div class="tech-card" style="opacity: 0.5;">
            <div class="card-title">Waiting</div>
            <div class="card-desc" style="font-size: 0.9rem;">
                Upload a resume to continue.
            </div>
        </div>
        """, unsafe_allow_html=True)
