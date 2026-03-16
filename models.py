from pydantic import BaseModel, Field
from typing import List, Optional

class SkillMatch(BaseModel):
    score: int = Field(..., ge=0, le=10)
    matching_skills: List[str]
    missing_skills: List[str]
    critical_gaps: List[str] = Field(description="Skills missing that are deal-breakers")

class MatchDetail(BaseModel):
    score: int = Field(..., ge=0, le=10)
    analysis: str
    pros: List[str]
    cons: List[str]

class RecruiterInsights(BaseModel):
    potential_red_flags: List[str]
    suggested_interview_questions: List[str]
    culture_fit_estimation: str

class FinalEvaluation(BaseModel):
    candidate_name: str
    job_title: str
    overall_fit_score: int = Field(..., ge=0, le=10)
    
    # Detailed Breakdowns
    skills_match: SkillMatch
    experience_match: MatchDetail
    technical_alignment: MatchDetail
    role_readiness: MatchDetail
    
    # Recruiter-Specific Tools
    insights: RecruiterInsights
    executive_summary: str = Field(description="A 2-3 sentence pitch for or against the candidate")