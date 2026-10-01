import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from jobs.recommender import JobRecommender
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

if st.sidebar.button("📄 1. Upload Resume", use_container_width=True):
    st.switch_page("pages/1_Upload_Resume.py")

if st.sidebar.button("🧠 2. Extract Skills", use_container_width=True):
    st.switch_page("pages/2_Extract_Skills.py")

if st.sidebar.button("🔍 3. Live Match", use_container_width=True, type="primary"):
    st.switch_page("pages/3_Live_Jobs.py")

if st.sidebar.button("🛡️ 4. Verify Job", use_container_width=True):
    st.switch_page("pages/4_Verify_Job.py")

if st.sidebar.button("📊 5. Dashboard", use_container_width=True):
    st.switch_page("pages/5_Dashboard.py")
# ==========================================

st.markdown('<div class="gradient-header">Live Career Recommendations</div>', unsafe_allow_html=True)
st.markdown('<div style="color:#A5B4FC; font-weight:700; font-size:1.15rem; letter-spacing:0.02em; margin-bottom: 25px;">MODULE 3: LIVE JOB MATCHING VIA JSEARCH API</div>', unsafe_allow_html=True)

if not st.session_state.get("extracted_skills"):
    st.warning("⚠️ No extracted skills found in session. Please run skill extraction first.")
    if st.button("Go to Extract Skills Page", use_container_width=True):
        st.switch_page("pages/2_Extract_Skills.py")
else:
    st.markdown(f"""
    <div class="tech-card">
        <div class="card-title">🔍 Matching Criteria</div>
        <div class="card-desc">
            <strong>Target Skills:</strong> {', '.join(st.session_state['extracted_skills'])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    db = DatabaseHandler()
    recommender = JobRecommender()

    st.markdown('<div class="gradient-subheader">Search Parameters</div>', unsafe_allow_html=True)
    col_loc, col_num = st.columns([2, 1])
    with col_loc:
        location_input = st.text_input("Preferred Location", value="India")
    with col_num:
        num_jobs_input = st.slider("Number of jobs to retrieve", min_value=3, max_value=10, value=5)

    if st.button("Fetch Career Recommendations", type="primary", use_container_width=True):
        with st.spinner("Connecting to JSearch API and analyzing listings..."):
            jobs = recommender.fetch_jobs(
                skills=st.session_state["extracted_skills"],
                location=location_input,
                num_jobs=num_jobs_input
            )
            
            if jobs:
                try:
                    db.save_recommended_jobs(st.session_state["resume_id"], jobs)
                    st.session_state["recommended_jobs"] = jobs
                    st.success(f"Successfully retrieved and logged {len(jobs)} jobs in the database.")
                except Exception as e:
                    st.error(f"Failed to log recommended jobs in DB: {e}")
                    st.session_state["recommended_jobs"] = jobs
            else:
                st.error("No jobs could be matched or retrieved. Please verify network access.")

    if st.session_state.get("recommended_jobs"):
        st.markdown('<div class="gradient-subheader">Recommended Openings</div>', unsafe_allow_html=True)
        
        for idx, job in enumerate(st.session_state["recommended_jobs"]):
            st.markdown(f"""
            <div class="tech-card">
                <div class="card-title">💼 {job['title']}</div>
                <div class="card-subtitle">🏢 {job['company']} | 📍 {job['location']}</div>
                <div class="card-desc" style="margin-bottom: 15px;">{job['description'][:350]}...</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_apply, col_select = st.columns([1, 1])
            with col_apply:
                st.link_button("🔗 Apply Now", job["apply_link"], use_container_width=True)
            with col_select:
                if st.button(f"🛡️ Select to Verify Security", key=f"select_job_{idx}", use_container_width=True):
                    st.session_state["selected_job"] = job
                    st.success(f"Selected '{job['title']}' for authenticity check.")

    if st.session_state.get("selected_job"):
        st.markdown('<div class="gradient-subheader">Selected Job Ready for Verification</div>', unsafe_allow_html=True)
        col_sel_info, col_sel_act = st.columns([2, 1])
        with col_sel_info:
            st.markdown(f"""
            <div class="tech-card job-authentic" style="margin: 0; padding: 15px;">
                <div class="card-title" style="color: #10B981;">✅ Ready to Verify</div>
                <div class="card-desc" style="font-size: 0.95rem;">
                    <strong>Job:</strong> {st.session_state['selected_job']['title']}<br>
                    <strong>Company:</strong> {st.session_state['selected_job']['company']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_sel_act:
            st.write("")
            if st.button("Proceed to Step 4: Verify Job ➔", type="primary", use_container_width=True):
                st.switch_page("pages/4_Verify_Job.py")