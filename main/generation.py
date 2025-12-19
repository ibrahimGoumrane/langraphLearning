from main.utils.logger import LoggerSetup
from main.generationOutput import EvaluationReport, Decision, OverallScore
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import time
import json
class Generation:
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("Generation instance initialized")
        
        # Decision thresholds (Adjust these based on your embedding model's typical output)
        self.PASS_THRESHOLD = 0.50  # Lowered because raw cosine similarity is often lower
        self.REVIEW_THRESHOLD = 0.35
        
    def _determine_decision(self, mean_score: float) -> Decision:
        if mean_score >= self.PASS_THRESHOLD:
            return Decision.PASS
        elif mean_score >= self.REVIEW_THRESHOLD:
            return Decision.REVIEW
        else:
            return Decision.REJECT

    def _format_cv_summary(self, cv: dict) -> str:
        # (Your existing formatting logic is good, keeping it brief for this snippet)
        summary = "=== CANDIDATE CV ===\n"
        # Flatten skills
        if cv.get("skills"):
            skills = [s.name for s in cv["skills"]]
            summary += f"SKILLS: {', '.join(skills)}\n"
        # Flatten experience
        if cv.get("experience"):
            summary += "EXPERIENCE:\n"
            for exp in cv["experience"]:
                summary += f"- {exp.position} at {exp.company}: {exp.description}\n"
        # Flatten projects
        if cv.get("projects"):
            summary += "PROJECTS:\n"
            for proj in cv["projects"]:
                summary += f"- {proj.name}: {proj.description}\n"
        # Flatten education
        if cv.get("education"):
             for edu in cv["education"]:
                summary += f"EDUCATION: {edu.degree} ({edu.start_date}-{edu.end_date})\n"
        return summary

    def _format_jd_summary(self, jd: dict) -> str:
        summary = "=== JOB DESCRIPTION ===\n"
        if jd.get("requirements"):
            summary += "REQUIREMENTS:\n" + "\n".join([f"- {r.name}" for r in jd["requirements"]]) + "\n"
        if jd.get("responsibilities"):
            summary += "RESPONSIBILITIES:\n" + "\n".join([f"- {r.name}" for r in jd["responsibilities"]]) + "\n"
        return summary

    def _resolve_final_decision(self, llm_decision_str: str, mean_score: float) -> Decision:
        """
        Combine LLM decision with Embedding Score based on user rules:
        1. LLM REJECT -> REJECT
        2. LLM PASS + Low Score -> REVIEW
        3. LLM REVIEW + Very Low Score (Score says No) -> REJECT
        """
        try:
            llm_decision = llm_decision_str.upper()
        except AttributeError:
            self.logger.warning(f"Invalid LLM decision received: {llm_decision_str}. Defaulting to REVIEW check.")
            llm_decision = "REVIEW"

        # Rule: If LLM rejects, we reject (Veto power)
        if llm_decision == "REJECT":
            self.logger.info(f"LLM Decision: REJECT. Final: REJECT.")
            return Decision.REJECT
            
        # Rule: If LLM PASS
        if llm_decision == "PASS":
            # If score supports it (>= PASS_THRESHOLD) -> PASS
            if mean_score >= self.PASS_THRESHOLD:
                self.logger.info(f"LLM Decision: PASS, Score: {mean_score:.2f} (High). Final: PASS.")
                return Decision.PASS
            else:
                # Score says no (Low) -> REVIEW
                self.logger.info(f"LLM Decision: PASS, but Score: {mean_score:.2f} (Low). Downgrading to REVIEW.")
                return Decision.REVIEW
        
        # Rule: If LLM REVIEW
        if llm_decision == "REVIEW":
            # If score supports at least Review (>= REVIEW_THRESHOLD) -> REVIEW
            if mean_score >= self.REVIEW_THRESHOLD:
                self.logger.info(f"LLM Decision: REVIEW, Score: {mean_score:.2f} (Ok). Final: REVIEW.")
                return Decision.REVIEW
            else:
                # Score says no (Very Low) -> REJECT
                self.logger.info(f"LLM Decision: REVIEW, but Score: {mean_score:.2f} (Too Low). Downgrading to REJECT.")
                return Decision.REJECT

        # Fallback
        self.logger.warning(f"Unhandled decision case: {llm_decision}. Defaulting to REVIEW.")
        return Decision.REVIEW

    def run(self, cv: dict, jd: dict, similarity_scores: dict) -> EvaluationReport:
        """
        Generates the report by:
        1. Asking LLM for BLIND analysis (Text only) AND a decision.
        2. Merging LLM decision with Embedding scores using logic.
        """
        self.logger.info("Starting evaluation report generation")
        start_time = time.time()
        
        try:
            # 1. Prepare Data
            cv_text = self._format_cv_summary(cv)
            jd_text = self._format_jd_summary(jd)
            
            # 2. Get Embedding Score
            mean_score = similarity_scores["overall"]["mean"]
            
            # 3. Define the "Blind" Prompt
            system_prompt = """You are an expert technical recruiter. 
            Analyze the Candidate's CV against the Job Description based ONLY on the text provided.
            
            Your Goal: Find the truth.
            - If the CV mentions a skill (e.g., 'Java'), it is a MATCH, even if it's just listed in skills.
            - If a skill is explicitly missing, it is a GAP.
            - Do not be biased by the length of the CV. Look for keywords and semantic meaning.
            """
            
            user_prompt = f"""
            {jd_text}
            
            {cv_text}
            
            Based on the text above, generate a JSON evaluation in this format:
            {{
                "decision": "PASS" | "REVIEW" | "REJECT", 
                "requirements_evaluation": {{
                    "explanation": "Brief assessment of technical requirements fit.",
                    "key_matches": ["list of matching skills/experience found"],
                    "gaps": ["list of missing requirements"]
                }},
                "responsibilities_evaluation": {{
                    "explanation": "Assessment of ability to perform daily tasks.",
                    "key_matches": ["relevant experience points"],
                    "gaps": ["missing experience areas"]
                }},
                "qualifications_evaluation": {{
                    "explanation": "Assessment of certifications and soft skills.",
                    "key_matches": ["relevant qualifications found"],
                    "gaps": ["missing qualifications"]
                }},
                "final_explanation": "A summary of the candidate's overall fit.",
                "recommendation": "A professional hiring recommendation sentence."
            }}
            """

            # 4. Call LLM (Blindly)
            self.logger.info("Calling LLM for blind qualitative analysis...")
            llm = ChatOllama(model="llama3:latest", temperature=0.1, format="json")
            
            response = llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ])
            
            llm_data = json.loads(response.content)
            
            # 5. THE MERGE: Combine LLM Decision + Embedding Scores
            self.logger.info("Merging Embedding Scores with LLM Analysis")
            
            llm_raw_decision = llm_data.get("decision", "REVIEW")
            final_decision = self._resolve_final_decision(llm_raw_decision, mean_score)
            
            # Construct the final object
            report = EvaluationReport(
                decision=final_decision,
                overall_score=OverallScore(
                    raw=similarity_scores["overall"]["raw"], 
                    mean=mean_score
                ),
                requirements_evaluation={
                    "section_name": "Requirements",
                    "similarity_score": similarity_scores["requirements"],
                    "explanation": llm_data["requirements_evaluation"]["explanation"],
                    "key_matches": llm_data["requirements_evaluation"]["key_matches"],
                    "gaps": llm_data["requirements_evaluation"]["gaps"]
                },
                responsibilities_evaluation={
                    "section_name": "Responsibilities",
                    "similarity_score": similarity_scores["responsibilities"],
                    "explanation": llm_data["responsibilities_evaluation"]["explanation"],
                    "key_matches": llm_data["responsibilities_evaluation"]["key_matches"],
                    "gaps": llm_data["responsibilities_evaluation"]["gaps"]
                },
                qualifications_evaluation={
                    "section_name": "Qualifications",
                    "similarity_score": similarity_scores["qualifications"],
                    "explanation": llm_data["qualifications_evaluation"]["explanation"],
                    "key_matches": llm_data["qualifications_evaluation"]["key_matches"],
                    "gaps": llm_data["qualifications_evaluation"]["gaps"]
                },
                final_explanation=llm_data["final_explanation"],
                strengths=llm_data["requirements_evaluation"]["key_matches"],
                weaknesses=llm_data["requirements_evaluation"]["gaps"],
                recommendation=llm_data["recommendation"]
            )
            
            elapsed = time.time() - start_time
            self.logger.info(f"Report generated in {elapsed:.2f}s. Final Decision: {final_decision.value} (LLM said {llm_raw_decision})")
            return report

        except Exception as e:
            self.logger.error(f"Error in generation: {str(e)}", exc_info=True)
            raise