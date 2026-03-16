from crewai import Crew, Process
from agents import (
    create_analyzer_agent,
    create_job_expert_agent,
    create_fit_scorer_agent,
)
from tasks import create_resume_task, create_job_task, create_scoring_task
from pdf_reader import read_pdf
from llm_config import get_llm
from reporting import OutputManager

# Initialize OpenAI LLM gpt-4.1-nano  
cheap_llm = get_llm('gpt-4.1-nano')      # Cost-effective for analysis gpt-3.5-turbo
expensive_llm = get_llm('gpt-4o-mini')  # More

# Initialize Anthropic LLMs
# cheap_llm = get_llm('claude-3-haiku-20240307')         # Cost-effective for analysis gpt-3.5-turbo
# expensive_llm = get_llm('claude-sonnet-4-6')           # More

output_manager = OutputManager()

# 1. Initialize Agents
analyzer = create_analyzer_agent(cheap_llm)
job_expert = create_job_expert_agent(expensive_llm)
scorer = create_fit_scorer_agent(cheap_llm)

# 2. Initialize Tasks
resume_content = read_pdf("resumes/john_carter_cv.pdf")
jd_content = read_pdf("resumes/ai_engineer_jd.pdf")

# 1. Define all tasks
t1 = create_resume_task(analyzer, resume_content)
t2 = create_job_task(job_expert, jd_content)

prelim_scorer = create_fit_scorer_agent(cheap_llm)
prelim_task = create_scoring_task(prelim_scorer, [t1, t2])

final_scorer = create_fit_scorer_agent(expensive_llm)
final_task = create_scoring_task(final_scorer, [prelim_task])  # tasks can reference other tasks

# 3. Assemble Crew
crew = Crew(
    agents=[analyzer, job_expert, prelim_scorer, final_scorer],
    tasks=[t1, t2, prelim_task, final_task],
    process=Process.sequential,
    verbose=True
)

# 4. Execute
result = crew.kickoff()
print(result.token_usage)

if result.pydantic:
    report = result.pydantic
    # Save files automatically
    output_manager.save_all_formats(report)
    
    # Optional: Keep a simple console summary for immediate feedback
    print(f"\nMatch Complete for {report.candidate_name}: {report.overall_fit_score}/10")
    print("Detailed report saved to outputs/ directory.")
else:
    print("Error: Crew did not return structured Pydantic data.")