from main.utils.logger import LoggerSetup
from main.generationOutput import EvaluationReport, Decision, OverallScore
from main.cv.cvmodelOutput import CvmodelOutput
from main.jobDescription.descmodelOutput import DescmodelOutput
from langchain_ollama import ChatOllama
import time

class Generation:
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("Generation instance initialized")
        
        # Decision thresholds
        self.PASS_THRESHOLD = 0.75
        self.REVIEW_THRESHOLD = 0.60
        
    def _determine_decision(self, mean_score: float) -> Decision:
        """
        Determine hiring decision based on mean similarity score.
        
        Args:
            mean_score: Mean similarity score across all sections
            
        Returns:
            Decision enum (PASS, REVIEW, or REJECT)
        """
        if mean_score >= self.PASS_THRESHOLD:
            decision = Decision.PASS
        elif mean_score >= self.REVIEW_THRESHOLD:
            decision = Decision.REVIEW
        else:
            decision = Decision.REJECT
            
        self.logger.info(f"Decision determined: {decision.value} (score: {mean_score:.4f})")
        return decision
    
    def _format_cv_summary(self, cv: dict) -> str:
        """Format CV data into a readable summary for the LLM."""
        summary = "=== CANDIDATE CV ===\n\n"
        
        # Education
        if cv.get("education"):
            summary += "EDUCATION:\n"
            for edu in cv["education"]:
                summary += f"- {edu.degree} in {edu.field_of_study} from {edu.school} ({edu.start_date} - {edu.end_date})\n"
            summary += "\n"
        
        # Skills
        if cv.get("skills"):
            summary += "SKILLS:\n"
            skills = [skill.name for skill in cv["skills"]]
            summary += f"- {', '.join(skills)}\n\n"
        
        # Experience
        if cv.get("experience"):
            summary += "EXPERIENCE:\n"
            for exp in cv["experience"]:
                summary += f"- {exp.position} at {exp.company} ({exp.start_date} - {exp.end_date})\n"
                summary += f"  {exp.description}\n"
            summary += "\n"
        
        # Certifications
        if cv.get("certifications"):
            summary += "CERTIFICATIONS:\n"
            certs = [cert.name for cert in cv["certifications"]]
            summary += f"- {', '.join(certs)}\n\n"
        
        # Projects
        if cv.get("projects"):
            summary += "PROJECTS:\n"
            for proj in cv["projects"]:
                summary += f"- {proj.name}: {proj.description}\n"
            summary += "\n"
        
        return summary
    
    def _format_jd_summary(self, jd: dict) -> str:
        """Format job description data into a readable summary for the LLM."""
        summary = "=== JOB DESCRIPTION ===\n\n"
        
        # Requirements
        if jd.get("requirements"):
            summary += "REQUIREMENTS:\n"
            for req in jd["requirements"]:
                summary += f"- {req.name}\n"
            summary += "\n"
        
        # Responsibilities
        if jd.get("responsibilities"):
            summary += "RESPONSIBILITIES:\n"
            for resp in jd["responsibilities"]:
                summary += f"- {resp.name}\n"
            summary += "\n"
        
        # Qualifications
        if jd.get("qualifications"):
            summary += "QUALIFICATIONS:\n"
            for qual in jd["qualifications"]:
                summary += f"- {qual.name}\n"
            summary += "\n"
        
        return summary
    
    def run(
        self, 
        cv: dict, 
        jd: dict, 
        similarity_scores: dict[str, float | dict[str, float]]
    ) -> EvaluationReport:
        """
        Generate final evaluation report with LLM-powered analysis.
        
        Args:
            cv: Structured CV data (dict with education, skills, experience, certifications, projects)
            jd: Structured job description data (dict with requirements, responsibilities, qualifications)
            similarity_scores: Dictionary containing:
                - requirements: float
                - responsibilities: float
                - qualifications: float
                - overall: dict with 'raw' and 'mean' scores
                
        Returns:
            EvaluationReport: Complete evaluation with decision, explanations, and recommendations
        """
        self.logger.info("Starting evaluation report generation")
        start_time = time.time()
        
        try:
            # Extract scores
            req_score = similarity_scores["requirements"]
            resp_score = similarity_scores["responsibilities"]
            qual_score = similarity_scores["qualifications"]
            overall = similarity_scores["overall"]
            mean_score = overall["mean"]
            
            self.logger.debug(f"Scores - Requirements: {req_score:.4f}, Responsibilities: {resp_score:.4f}, "
                            f"Qualifications: {qual_score:.4f}, Mean: {mean_score:.4f}")
            
            # Determine decision
            decision = self._determine_decision(mean_score)
            
            # Format data for LLM
            cv_summary = self._format_cv_summary(cv)
            jd_summary = self._format_jd_summary(jd)
            
            # Construct LLM prompt
            system_prompt = """You are an expert technical recruiter analyzing candidate-job fit.
Your task is to provide detailed, evidence-based evaluation of how well a candidate matches a job description.

For each section (Requirements, Responsibilities, Qualifications), you must:
1. Explain what the similarity score means in practical terms
2. Identify specific matching points from the CV
3. Identify gaps or weaknesses
4. Be honest and balanced in your assessment

Finally, provide an overall recommendation that synthesizes all sections."""

            user_prompt = f"""{cv_summary}

{jd_summary}

=== SIMILARITY SCORES ===
Requirements Match: {req_score:.2%} (Education + Projects vs Requirements)
Responsibilities Match: {resp_score:.2%} (Experience + Projects vs Responsibilities)
Qualifications Match: {qual_score:.2%} (Skills + Certifications vs Qualifications)
Overall Mean Score: {mean_score:.2%}

=== YOUR TASK ===
Based on the above CV, job description, and similarity scores, provide a detailed evaluation:

1. **Requirements Evaluation** ({req_score:.2%} match):
   - Explanation: Why this score? What does it mean?
   - Key Matches: List 2-3 specific CV items that match requirements
   - Gaps: List any missing or weak areas

2. **Responsibilities Evaluation** ({resp_score:.2%} match):
   - Explanation: Why this score? What does it mean?
   - Key Matches: List 2-3 specific CV items that match responsibilities
   - Gaps: List any missing or weak areas

3. **Qualifications Evaluation** ({qual_score:.2%} match):
   - Explanation: Why this score? What does it mean?
   - Key Matches: List 2-3 specific CV items that match qualifications
   - Gaps: List any missing or weak areas

4. **Overall Assessment**:
   - Final Explanation: Synthesize all sections into a coherent assessment
   - Strengths: List 3-5 key strengths of this candidate
   - Weaknesses: List 3-5 key weaknesses or gaps
   - Recommendation: Final hiring recommendation for the hiring manager

Be specific, cite evidence from the CV, and be honest about both strengths and weaknesses."""

            # Call LLM
            self.logger.info("Calling LLM for evaluation analysis")
            llm = ChatOllama(
                model="deepseek-r1:latest",
                temperature=0.3,
                reasoning=False,
                format="json"
            ).with_structured_output(schema=EvaluationReport)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            llm_start = time.time()
            evaluation = llm.invoke(messages)
            llm_elapsed = time.time() - llm_start
            self.logger.info(f"LLM evaluation completed in {llm_elapsed:.2f}s")
            
            # Override decision with our threshold-based decision
            evaluation.decision = decision
            evaluation.overall_score = OverallScore(raw=overall["raw"], mean=mean_score)
            
            # Ensure section scores are set
            evaluation.requirements_evaluation.similarity_score = req_score
            evaluation.responsibilities_evaluation.similarity_score = resp_score
            evaluation.qualifications_evaluation.similarity_score = qual_score
            
            elapsed = time.time() - start_time
            self.logger.info(f"Evaluation report generated successfully in {elapsed:.2f}s")
            self.logger.info(f"Final decision: {decision.value}")
            
            return evaluation
            
        except Exception as e:
            self.logger.error(f"Error generating evaluation report: {str(e)}", exc_info=True)
            raise
