from crewai import Crew, Process
from agents import (
    create_analyzer_agent,
    create_job_expert_agent,
    create_fit_scorer_agent,
)
from tasks import create_resume_task, create_job_task, create_scoring_task
from llm_config import get_llm
from reporting import OutputManager


def run_resume_matching(resume_content, jd_content):

    cheap_llm = get_llm("gpt-4.1-nano")
    expensive_llm = get_llm("gpt-4o-mini")

    output_manager = OutputManager()

    # Agents
    analyzer = create_analyzer_agent(cheap_llm)
    job_expert = create_job_expert_agent(expensive_llm)

    # Tasks
    t1 = create_resume_task(analyzer, resume_content)
    t2 = create_job_task(job_expert, jd_content)

    prelim_scorer = create_fit_scorer_agent(cheap_llm)
    prelim_task = create_scoring_task(prelim_scorer, [t1, t2])

    final_scorer = create_fit_scorer_agent(expensive_llm)
    final_task = create_scoring_task(final_scorer, [prelim_task])

    crew = Crew(
        agents=[analyzer, job_expert, prelim_scorer, final_scorer],
        tasks=[t1, t2, prelim_task, final_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    if result.pydantic:
        report = result.pydantic
        output_manager.save_all_formats(report)
        return report, result.token_usage

    return None, None