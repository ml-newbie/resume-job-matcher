from crewai import Agent

def create_analyzer_agent(llm):
    return Agent(
        role='Resume Data Extractor',
        goal='Extract high-fidelity structured data from CVs.',
        backstory='You are a specialist in parsing technical resumes into clean data.',
        llm=llm,
        verbose=True
    )

def create_job_expert_agent(llm):
    return Agent(
        role='Job Requirement Analyst',
        goal='Identify core requirements and stack needs from a JD.',
        backstory='You distill complex job descriptions into actionable criteria.',
        llm=llm,
        verbose=True
    )

def create_fit_scorer_agent(llm):
    return Agent(
        role='Senior Technical Recruiter',
        goal='Evaluate candidate-to-job fit with high precision.',
        backstory='Expert in gap analysis and talent assessment.',
        llm=llm,
        verbose=True
    )