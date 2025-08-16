from pydantic import BaseModel, EmailStr
from typing import List, Literal, TypedDict

class SkillAnalysis(TypedDict):
    """
    Analysis of the skills required for the job.
    """
    matched: list[str]
    missing: list[str]
    additional: list[str]
    score: float
    

class SharedState(TypedDict):
    """
    Shared state for the agent.
    """
    name: str
    email: EmailStr
    phone: str
    years_of_experience: int
    skills: List[str]
    pre_screening_status: Literal['Pass', 'Fail']
    skills_analysis: SkillAnalysis
    final_decision: Literal['Interview', 'Phone Screen', 'Rejected']
    rejection_reason: str
    jd_text: str  # Store the job description text from user input
    
    