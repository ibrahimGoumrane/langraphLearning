from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum

class Decision(str, Enum):
    """Final hiring decision enum"""
    PASS = "PASS"
    REVIEW = "REVIEW"
    REJECT = "REJECT"

class SectionEvaluation(BaseModel):
    """Evaluation for a specific section comparison"""
    section_name: str = Field(description="Name of the section (e.g., 'Requirements', 'Responsibilities', 'Qualifications')")
    similarity_score: float = Field(description="Cosine similarity score between 0 and 1")
    explanation: str = Field(description="LLM-generated explanation of the match quality")
    key_matches: list[str] = Field(default_factory=list, description="Key matching points from CV")
    gaps: list[str] = Field(default_factory=list, description="Missing or weak areas")

class OverallScore(BaseModel):
    """Overall similarity scores"""
    raw: float = Field(description="Raw similarity score between entire CV and JD")
    mean: float = Field(description="Mean of all section similarity scores")

class EvaluationReport(BaseModel):
    """Complete evaluation report for a candidate"""
    decision: Decision = Field(description="Final hiring decision: PASS, REVIEW, or REJECT")
    overall_score: OverallScore = Field(description="Overall similarity scores")
    
    requirements_evaluation: SectionEvaluation = Field(description="Evaluation of requirements match")
    responsibilities_evaluation: SectionEvaluation = Field(description="Evaluation of responsibilities match")
    qualifications_evaluation: SectionEvaluation = Field(description="Evaluation of qualifications match")
    
    final_explanation: str = Field(description="Comprehensive explanation of the final decision")
    strengths: list[str] = Field(default_factory=list, description="Candidate's key strengths")
    weaknesses: list[str] = Field(default_factory=list, description="Candidate's key weaknesses or gaps")
    recommendation: str = Field(description="Final recommendation for hiring manager")
