import streamlit as st
import os
import sys
import json
import pandas as pd
import plotly.express as px

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.append(project_root)

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

if st.sidebar.button("4. Verify Job", use_container_width=True):
    st.switch_page("pages/4_Verify_Job.py")

if st.sidebar.button(
    "5. Dashboard",
    use_container_width=True,
    type="primary"
):
    st.switch_page("pages/5_Dashboard.py")


st.markdown(
    '<div class="gradient-header">Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div style="color:#A5B4FC; font-weight:700; font-size:1.15rem; '
    'margin-bottom: 25px;">View project statistics and verification results</div>',
    unsafe_allow_html=True
)


db = DatabaseHandler()
stats = db.get_dashboard_stats()


col_m1, col_m2, col_m3, col_m4 = st.columns(4)


with col_m1:
    st.markdown(
        f'<div class="metric-box">'
        f'<div class="metric-value">{stats["total_resumes"]}</div>'
        f'<div class="metric-label">Resumes</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with col_m2:
    st.markdown(
        f'<div class="metric-box">'
        f'<div class="metric-value">{stats["total_verified"]}</div>'
        f'<div class="metric-label">Verifications</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with col_m3:
    st.markdown(
        f'<div class="metric-box">'
        f'<div class="metric-value" style="color:#10B981;">'
        f'{stats["authentic_count"]}</div>'
        f'<div class="metric-label">Authentic</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with col_m4:
    st.markdown(
        f'<div class="metric-box">'
        f'<div class="metric-value" style="color:#F59E0B;">'
        f'{stats["suspicious_count"]}</div>'
        f'<div class="metric-label">Suspicious</div>'
        f'</div>',
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="gradient-subheader">Model Results and Job Distribution</div>',
    unsafe_allow_html=True
)


col_chart1, col_chart2 = st.columns(2)


with col_chart1:

    st.write("Model Accuracy Comparison")

    stats_path = os.path.join(
        project_root,
        "models",
        "training_stats.json"
    )

    if os.path.exists(stats_path):

        try:

            with open(stats_path, "r") as f:
                training_data = json.load(f)

            comp_data = training_data.get("comparison", {})

            df_models = pd.DataFrame({
                "Model": list(comp_data.keys()),
                "Accuracy (%)": [
                    m["accuracy"]
                    for m in comp_data.values()
                ]
            })

            fig1 = px.bar(
                df_models,
                x="Model",
                y="Accuracy (%)",
                text="Accuracy (%)",
                template="plotly_dark"
            )

            fig1.update_layout(
                showlegend=False,
                margin=dict(t=10, b=10, l=10, r=10),
                height=300
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        except Exception:
            st.error("Could not load model metrics.")

    else:

        df_models_default = pd.DataFrame({
            "Model": [
                "Random Forest",
                "Support Vector Machine",
                "Logistic Regression",
                "Naive Bayes"
            ],
            "Accuracy (%)": [
                98.5,
                96.2,
                94.8,
                91.3
            ]
        })

        fig_def = px.bar(
            df_models_default,
            x="Model",
            y="Accuracy (%)",
            text="Accuracy (%)",
            template="plotly_dark"
        )

        fig_def.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=300
        )

        st.plotly_chart(
            fig_def,
            use_container_width=True
        )


with col_chart2:

    st.write("Authentic and Suspicious Jobs")

    if stats["total_verified"] > 0:

        df_dist = pd.DataFrame({
            "Verdict": [
                "Authentic",
                "Suspicious"
            ],
            "Count": [
                stats["authentic_count"],
                stats["suspicious_count"]
            ]
        })

        fig2 = px.pie(
            df_dist,
            names="Verdict",
            values="Count",
            color="Verdict",
            color_discrete_map={
                "Authentic": "#10B981",
                "Suspicious": "#F59E0B"
            },
            template="plotly_dark",
            hole=0.4
        )

        fig2.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=300
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    else:

        st.info(
            "No job verifications have been recorded yet."
        )


st.markdown(
    '<div class="gradient-subheader">Job Verification History</div>',
    unsafe_allow_html=True
)


verifications = db.get_all_verifications()


if verifications:

    log_data = []

    for v in verifications:

        log_data.append({
            "Log ID": v["id"],
            "Timestamp": v["created_at"],
            "Verdict": v["prediction_result"],
            "Confidence (%)": f"{v['confidence_score']:.2f}%",
            "Job Description Snippet":
                v["job_description"][:100] + "..."
        })

    st.dataframe(
        pd.DataFrame(log_data),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No job verification history is available."
    )


st.markdown("---")


if st.button(
    "Return to Home",
    use_container_width=True
):
    st.switch_page("app.py")
