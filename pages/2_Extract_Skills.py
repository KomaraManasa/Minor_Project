import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.append(project_root)

from utils.nlp_skills import SkillExtractor
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

if st.sidebar.button(
    "2. Extract Skills",
    use_container_width=True,
    type="primary"
):
    st.switch_page("pages/2_Extract_Skills.py")

if st.sidebar.button("3. Live Match", use_container_width=True):
    st.switch_page("pages/3_Live_Jobs.py")

if st.sidebar.button("4. Verify Job", use_container_width=True):
    st.switch_page("pages/4_Verify_Job.py")

if st.sidebar.button("5. Dashboard", use_container_width=True):
    st.switch_page("pages/5_Dashboard.py")


st.markdown(
    '<div class="gradient-header">Extract Skills</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="color:#A5B4FC; font-weight:700; font-size:1.15rem; '
    'margin-bottom: 25px;">Extract skills from the resume</div>',
    unsafe_allow_html=True
)


if not st.session_state.get("resume_id") or not st.session_state.get("resume_text"):

    st.warning(
        "No active resume found. Please upload and parse your resume first."
    )

    if st.button(
        "Go to Upload Resume Page",
        use_container_width=True
    ):
        st.switch_page("pages/1_Upload_Resume.py")

else:

    st.markdown(f"""
    <div class="tech-card">
        <div class="card-title">Active Resume</div>
        <div class="card-desc">
            <strong>Filename:</strong> {st.session_state['resume_filename']}<br>
            <strong>Database ID:</strong> {st.session_state['resume_id']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    db = DatabaseHandler()

    if st.button(
        "Extract Skills",
        type="primary",
        use_container_width=True
    ):

        with st.spinner("Extracting skills from resume..."):

            try:

                extractor = SkillExtractor()

                skills = extractor.extract_skills(
                    st.session_state["resume_text"]
                )

                if skills:

                    db.save_skills(
                        st.session_state["resume_id"],
                        skills
                    )

                    st.session_state["extracted_skills"] = skills

                    st.success(
                        f"Extracted {len(skills)} skills from the resume."
                    )

                else:

                    st.warning(
                        "No matching skills were found in the resume."
                    )

            except Exception as e:

                st.error(
                    f"Could not extract skills: {e}"
                )


    if st.session_state.get("extracted_skills"):

        st.markdown(
            '<div class="gradient-subheader">Extracted Skills</div>',
            unsafe_allow_html=True
        )

        col_b, col_nxt = st.columns([3, 1])

        with col_b:

            badges_html = (
                "<div style='display: flex; flex-wrap: wrap; "
                "margin-bottom: 20px;'>"
            )

            for skill in st.session_state["extracted_skills"]:
                badges_html += (
                    f'<span class="skill-badge">{skill}</span>'
                )

            badges_html += "</div>"

            st.markdown(
                badges_html,
                unsafe_allow_html=True
            )

        with col_nxt:

            st.write("")

            if st.button(
                "Proceed to Step 3: Live Match",
                type="primary",
                use_container_width=True
            ):
                st.switch_page("pages/3_Live_Jobs.py")
