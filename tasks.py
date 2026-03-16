from crewai import Task
from models import FinalEvaluation

def create_resume_task(agent, resume_text):
    return Task(
        description=f"Analyze this resume: {resume_text}",
        expected_output="A structured summary of the candidate profile.",
        agent=agent
    )

def create_job_task(agent, jd_text):
    return Task(
        description=f"Analyze this job description: {jd_text}",
        expected_output="A structured summary of job requirements.",
        agent=agent
    )

def create_scoring_task(agent, context_tasks):
    return Task(
        description=(
            "Review the candidate's resume and the job requirements from previous tasks.\n\n"
            "Your goal is to provide a 'Go/No-Go' recommendation for a recruiter.\n"
            "1. Be hyper-critical about 'Critical Gaps'.\n"
            "2. Identify 'Red Flags' (e.g., job hopping, lack of progression, or missing core certifications).\n"
            "3. Generate 3 high-impact interview questions tailored specifically to bridge the gaps found.\n"
            "4. Write an Executive Summary that a recruiter can copy-paste into an email to a Hiring Manager."
        ),
        expected_output="A comprehensive, recruiter-ready Pydantic evaluation object.",
        context=context_tasks,
        output_pydantic=FinalEvaluation,
        agent=agent
    )