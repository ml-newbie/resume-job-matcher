import os

os.environ["CREWAI_TELEMETRY_ENABLED"] = "false"
os.environ["OTEL_SDK_DISABLED"] = "true"


import streamlit as st
import plotly.graph_objects as go

from pdf_reader import read_pdf
from run_workflow import run_resume_matching
from get_keys import get_secret

APP_PASSWORD = get_secret("APP_PASSWORD")

def check_password():

    import streamlit as st

    st.markdown("""
    <style>

    /* Hide sidebar */
    [data-testid="stSidebar"] {display: none;}

    /* Page background */
    .stApp {
        background: linear-gradient(135deg, #eef2ff, #f8fafc);
    }

    /* Login card */
    .login-card {
        padding: 45px;
        border-radius: 16px;
        background: white;
        box-shadow: 0 12px 35px rgba(0,0,0,0.08);
        text-align: center;
    }

    .login-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .login-subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 25px;
    }

    </style>
    """, unsafe_allow_html=True)

    def password_entered():
        if st.session_state["password"] == APP_PASSWORD:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    # vertical spacing
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    left, center, right = st.columns([3,2,3])

    with center:

        st.markdown("""
        <div class="login-card">
            <div class="login-title">🔒 AI Resume Matcher</div>
            <div class="login-subtitle">
                Evaluate candidate fit using AI-powered resume analysis
            </div>
        </div>
        """, unsafe_allow_html=True)

        password = st.text_input(
            "Password",
            type="password",
            label_visibility="collapsed",
            placeholder="Enter password",
            key="password"
        )

        login = st.button("Unlock Access", use_container_width=True)

        if login:
            password_entered()

        if "password_correct" in st.session_state:
            if not st.session_state["password_correct"]:
                st.error("Incorrect password")

    if "password_correct" not in st.session_state:
        return False
    elif not st.session_state["password_correct"]:
        return False
    else:
        return True
        
st.set_page_config(page_title="AI Resume Matcher", page_icon="📄", layout="wide")
if not check_password():
    st.stop()

    
st.title("AI Resume ↔ Job Description Matcher")

st.write(
    "Upload a candidate resume and a job description to evaluate candidate fit."
)

# File Upload
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

with col2:
    jd_file = st.file_uploader(
        "Upload Job Description (PDF)",
        type=["pdf"]
    )


# Run Button
if st.button("Run Matching"):

    if resume_file and jd_file:

        with st.spinner("Analyzing resume and job description..."):

            resume_text = read_pdf(resume_file)
            jd_text = read_pdf(jd_file)

            report, tokens = run_resume_matching(
                resume_text,
                jd_text
            )

        if report:

            # ==============================
            # Candidate Overview
            # ==============================

            st.header("Candidate Evaluation")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Candidate", report.candidate_name)

            with col2:
                st.metric("Role", report.job_title)

            with col3:
                st.metric(
                    "Overall Fit",
                    f"{report.overall_fit_score}/10"
                )

            # ==============================
            # Radar Chart
            # ==============================

            categories = [
                "Skills",
                "Experience",
                "Technical Alignment",
                "Role Readiness"
            ]

            scores = [
                report.skills_match.score,
                report.experience_match.score,
                report.technical_alignment.score,
                report.role_readiness.score
            ]

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill="toself",
                name="Candidate"
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )
                ),
                showlegend=False,
                height=400
            )

            st.subheader("Evaluation Breakdown")
            st.plotly_chart(fig, use_container_width=True)

            # ==============================
            # Skills Analysis
            # ==============================

            st.subheader("Skills Analysis")

            skills = report.skills_match

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("### Matching Skills")
                for skill in skills.matching_skills:
                    st.success(skill)

            with col2:
                st.markdown("### Missing Skills")
                for skill in skills.missing_skills:
                    st.warning(skill)

            with col3:
                st.markdown("### Critical Gaps")
                for skill in skills.critical_gaps:
                    st.error(skill)

            # ==============================
            # Detailed Evaluation
            # ==============================

            st.subheader("Detailed Evaluation")

            tabs = st.tabs([
                "Experience",
                "Technical Alignment",
                "Role Readiness"
            ])

            # Experience
            with tabs[0]:

                exp = report.experience_match

                st.metric("Score", f"{exp.score}/10")

                st.write(exp.analysis)

                st.markdown("### Pros")
                for p in exp.pros:
                    st.success(p)

                st.markdown("### Cons")
                for c in exp.cons:
                    st.warning(c)

            # Technical Alignment
            with tabs[1]:

                tech = report.technical_alignment

                st.metric("Score", f"{tech.score}/10")

                st.write(tech.analysis)

                st.markdown("### Pros")
                for p in tech.pros:
                    st.success(p)

                st.markdown("### Cons")
                for c in tech.cons:
                    st.warning(c)

            # Role Readiness
            with tabs[2]:

                role = report.role_readiness

                st.metric("Score", f"{role.score}/10")

                st.write(role.analysis)

                st.markdown("### Pros")
                for p in role.pros:
                    st.success(p)

                st.markdown("### Cons")
                for c in role.cons:
                    st.warning(c)

            # ==============================
            # Recruiter Insights
            # ==============================

            st.subheader("Recruiter Insights")

            insights = report.insights

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### Potential Red Flags")

                for flag in insights.potential_red_flags:
                    st.error(flag)

            with col2:

                st.markdown("### Suggested Interview Questions")

                for q in insights.suggested_interview_questions:
                    st.info(q)

            st.markdown("### Culture Fit Estimation")

            st.write(insights.culture_fit_estimation)

            # ==============================
            # Executive Summary
            # ==============================

            st.subheader("Executive Summary")

            st.info(report.executive_summary)

            # ==============================
            # Token Usage
            # ==============================

            if tokens:
                st.subheader("LLM Token Usage")
                st.json(tokens)

        else:
            st.error("Crew execution failed.")

    else:
        st.warning("Please upload both Resume and Job Description.")
