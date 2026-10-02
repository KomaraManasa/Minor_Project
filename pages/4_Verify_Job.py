import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.append(project_root)

from verification.model import JobVerifier
from database.db_handler import DatabaseHandler


def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


css_path = os.path.join(project_root, "assets", "custom.css")
load_css(css_path)


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


if st.sidebar.button("Home", use_container_width=True):
    st.switch_page("app.py")

if st.sidebar.button("1. Upload Resume", use_container_width=True):
    st.switch_page("pages/1_Upload_Resume.py")

if st.sidebar.button("2. Extract Skills", use_container_width=True):
    st.switch_page("pages/2_Extract_Skills.py")

if st.sidebar.button("3. Live Match", use_container_width=True):
    st.switch_page("pages/3_Live_Jobs.py")

if st.sidebar.button(
    "4. Verify Job",
    use_container_width=True,
    type="primary"
):
    st.switch_page("pages/4_Verify_Job.py")

if st.sidebar.button("5. Dashboard", use_container_width=True):
    st.switch_page("pages/5_Dashboard.py")


st.markdown(
    '<div class="gradient-header">Verify Job Posting</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="color:#A5B4FC; font-weight:700; font-size:1.15rem; '
    'margin-bottom: 25px;">Check a job posting using the trained model</div>',
    unsafe_allow_html=True
)


db = DatabaseHandler()

selected_job = st.session_state.get("selected_job")

default_text = ""

if selected_job:

    st.info(
        f"Using the selected job: {selected_job['title']} "
        f"at {selected_job['company']}."
    )

    default_text = (
        f"Job Title: {selected_job['title']}\n"
        f"Company: {selected_job['company']}\n\n"
        f"Job Description:\n{selected_job['description']}"
    )


job_desc_input = st.text_area(
    "Paste Job Description",
    value=default_text,
    height=250,
    placeholder="Paste the job description here..."
)


if "last_verification_result" not in st.session_state:
    st.session_state["last_verification_result"] = None


if st.button(
    "Run Verification",
    type="primary",
    use_container_width=True
):

    if not job_desc_input.strip():

        st.warning(
            "Please paste a job description to verify."
        )

    else:

        with st.spinner("Analyzing job description..."):

            try:

                verifier = JobVerifier()

                result = verifier.verify(job_desc_input)

                db.save_verification(
                    job_description=job_desc_input,
                    prediction_result=result["label"],
                    confidence_score=result["confidence"],
                    reasons=result["reasons"]
                )

                st.session_state["last_verification_result"] = result

                st.success(
                    "Verification complete."
                )

            except Exception as e:

                st.error(
                    f"Verification failed: {e}"
                )


result = st.session_state["last_verification_result"]


if result:

    st.markdown(
        '<div class="gradient-subheader">Verification Results</div>',
        unsafe_allow_html=True
    )

    col_verdict, col_details = st.columns([1, 1])


    with col_verdict:

        card_class = (
            "job-authentic"
            if result["label"] == "Authentic"
            else "job-suspicious"
        )

        st.markdown(f"""
        <div class="tech-card {card_class}">
            <div class="card-title" style="font-size: 1.5rem; font-family: 'Outfit', sans-serif;">
                {result['label'].upper()}
            </div>

            <div class="card-subtitle" style="margin-top: 5px;">
                Classification Result
            </div>

            <div class="card-desc" style="color: #FFFFFF; font-size: 1.1rem; margin-top: 15px;">
                Model confidence:
                <strong>{result['confidence']}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(
            result["confidence"] / 100.0
        )


    with col_details:

        reasons_list_html = "".join(
            [
                f'<li class="reason-item">{reason}</li>'
                for reason in result["reasons"]
            ]
        )

        st.markdown(f"""
        <div class="tech-card" style="height: 100%;">
            <div class="card-title">Verification Details</div>

            <div class="card-subtitle">
                Supporting information
            </div>

            <div class="card-desc">
                <ul style="padding-left: 15px; margin: 0;">
                    {reasons_list_html}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("---")

    col_action1, col_action2 = st.columns([2, 1])


    with col_action1:

        if selected_job and st.button(
            "Clear Selected Job",
            use_container_width=True
        ):

            st.session_state["selected_job"] = None
            st.session_state["last_verification_result"] = None

            st.rerun()


    with col_action2:

        if st.button(
            "Proceed to Step 5: Dashboard",
            type="primary",
            use_container_width=True
        ):
            st.switch_page("pages/5_Dashboard.py")
