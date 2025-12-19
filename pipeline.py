"""
AI Technical Recruiter - Main Pipeline
Orchestrates the complete evaluation pipeline from document loading to final decision.
"""

from main import (
    LoggerSetup,
    Saver,
    CvProcessing,
    DescProcessing,
    Embeddings,
    Generation,
    EvaluationReport
)
from main.retreival import Retreival
from main.cleaning import Cleaning
import time
from pathlib import Path


class RecruitmentPipeline:
    """
    Main pipeline orchestrator for CV-Job Description evaluation.
    
    Pipeline stages:
    1. Document Retrieval (load CV and JD files)
    2. Text Cleaning (remove noise and normalize)
    3. Structured Processing (LLM extraction)
    4. Semantic Similarity (embedding comparison)
    5. Final Evaluation (LLM-based decision)
    """
    
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("=" * 80)
        self.logger.info("Initializing Recruitment Pipeline")
        self.logger.info("=" * 80)
        
        # Initialize all pipeline components
        self.retrieval = Retreival()
        self.cleaning = Cleaning()
        self.cv_processing = CvProcessing()
        self.desc_processing = DescProcessing()
        self.embeddings = Embeddings()
        self.generation = Generation()
        
        self.logger.info("All pipeline components initialized successfully")
    
    def run(
        self,
        cv_path: str,
        jd_path: str,
        cv_type: str = "pdf",
        jd_type: str = "pdf",
        output_path: str = "results/evaluation_report.json"
    ) -> EvaluationReport:
        """
        Execute the complete recruitment pipeline.
        
        Args:
            cv_path: Path to CV file
            jd_path: Path to job description file
            cv_type: CV file type (pdf, docx, txt)
            jd_type: Job description file type (pdf, docx, txt)
            output_path: Path to save the final evaluation report
            
        Returns:
            EvaluationReport: Complete evaluation with decision and explanations
        """
        pipeline_start = time.time()
        self.logger.info("=" * 80)
        self.logger.info("STARTING RECRUITMENT PIPELINE")
        self.logger.info(f"CV: {cv_path} ({cv_type})")
        self.logger.info(f"JD: {jd_path} ({jd_type})")
        self.logger.info("=" * 80)
        
        try:
            # ========== STAGE 1: DOCUMENT RETRIEVAL ==========
            self.logger.info("\n" + "=" * 80)
            self.logger.info("STAGE 1: DOCUMENT RETRIEVAL")
            self.logger.info("=" * 80)
            
            stage_start = time.time()
            cv_raw = self.retrieval.run(cv_path, cv_type)
            jd_raw = self.retrieval.run(jd_path, jd_type)
            stage_elapsed = time.time() - stage_start
            
            self.logger.info(f"✓ Documents loaded successfully in {stage_elapsed:.2f}s")
            self.logger.info(f"  CV length: {len(cv_raw)} characters")
            self.logger.info(f"  JD length: {len(jd_raw)} characters")
            
            # ========== STAGE 2: TEXT CLEANING ==========
            self.logger.info("\n" + "=" * 80)
            self.logger.info("STAGE 2: TEXT CLEANING")
            self.logger.info("=" * 80)
            
            stage_start = time.time()
            cv_clean = self.cleaning.run(cv_raw)
            jd_clean = self.cleaning.run(jd_raw)
            stage_elapsed = time.time() - stage_start
            
            self.logger.info(f"✓ Text cleaned successfully in {stage_elapsed:.2f}s")
            self.logger.info(f"  CV cleaned length: {len(cv_clean)} characters")
            self.logger.info(f"  JD cleaned length: {len(jd_clean)} characters")
            
            
            # ========== STAGE 3: STRUCTURED PROCESSING ==========
            self.logger.info("\n" + "=" * 80)
            self.logger.info("STAGE 3: STRUCTURED PROCESSING (LLM Extraction)")
            self.logger.info("=" * 80)
            
            stage_start = time.time()
            
            self.logger.info("Processing CV...")
            cv_structured = self.cv_processing.run(cv_clean, output_format="json")
            cv_strings = self.cv_processing.flatten_objects_to_string(cv_structured)
            
            self.logger.info("Processing Job Description...")
            jd_structured = self.desc_processing.run(jd_clean, output_format="json")
            jd_strings = self.desc_processing.flatten_objects_to_string(jd_structured)
            
            stage_elapsed = time.time() - stage_start
            self.logger.info(f"✓ Structured extraction completed in {stage_elapsed:.2f}s")


            # ========== STAGE 4: SEMANTIC SIMILARITY SCORING ==========
            self.logger.info("\n" + "=" * 80)
            self.logger.info("STAGE 4: SEMANTIC SIMILARITY SCORING")
            self.logger.info("=" * 80)
            
            stage_start = time.time()
            similarity_scores = self.embeddings.run(cv_strings, jd_strings)
            stage_elapsed = time.time() - stage_start
            
            self.logger.info(f"✓ Similarity scoring completed in {stage_elapsed:.2f}s")
            self.logger.info(f"  Requirements match: {similarity_scores['requirements']:.2%}")
            self.logger.info(f"  Responsibilities match: {similarity_scores['responsibilities']:.2%}")
            self.logger.info(f"  Qualifications match: {similarity_scores['qualifications']:.2%}")
            self.logger.info(f"  Overall mean: {similarity_scores['overall']['mean']:.2%}")
            
            # ========== STAGE 5: FINAL EVALUATION & DECISION ==========
            self.logger.info("\n" + "=" * 80)
            self.logger.info("STAGE 5: FINAL EVALUATION & DECISION (LLM Analysis)")
            self.logger.info("=" * 80)
            
            stage_start = time.time()
            evaluation_report = self.generation.run(
                cv=cv_structured,
                jd=jd_structured,
                similarity_scores=similarity_scores
            )
            stage_elapsed = time.time() - stage_start
            
            self.logger.info(f"✓ Evaluation completed in {stage_elapsed:.2f}s")
            self.logger.info(f"  FINAL DECISION: {evaluation_report.decision.value}")
            
            # ========== SAVE RESULTS ==========
            self.logger.info("\n" + "=" * 80)
            self.logger.info("SAVING RESULTS")
            self.logger.info("=" * 80)
            
            # Create output directory if it doesn't exist
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the evaluation report
            Saver.saveJson(evaluation_report, output_path)
            self.logger.info(f"✓ Evaluation report saved to: {output_path}")
            
            # ========== PIPELINE COMPLETE ==========
            pipeline_elapsed = time.time() - pipeline_start
            self.logger.info("\n" + "=" * 80)
            self.logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            self.logger.info("=" * 80)
            self.logger.info(f"Total execution time: {pipeline_elapsed:.2f}s")
            self.logger.info(f"Final Decision: {evaluation_report.decision.value}")
            self.logger.info(f"Overall Score: {evaluation_report.overall_score.mean:.2%}")
            self.logger.info("=" * 80)
            
            return evaluation_report
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            raise


def main():
    """
    Main entry point for the recruitment pipeline.
    Processes CV and Job Description files from the files directory.
    """
    # Initialize pipeline
    pipeline = RecruitmentPipeline()
    
    # Define file paths (using PDF files as default)
    cv_path = "files/pdf/cvpfe.pdf"
    jd_path = "files/pdf/desc.pdf"
    
    # Run the pipeline
    evaluation = pipeline.run(
        cv_path=cv_path,
        jd_path=jd_path,
        cv_type="pdf",
        jd_type="pdf",
        output_path="results/evaluation_report.json"
    )
    
    # Print summary
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    print(f"Decision: {evaluation.decision.value}")
    print(f"Overall Score: {evaluation.overall_score.mean:.2%}")
    print(f"\nRequirements Match: {evaluation.requirements_evaluation.similarity_score:.2%}")
    print(f"Responsibilities Match: {evaluation.responsibilities_evaluation.similarity_score:.2%}")
    print(f"Qualifications Match: {evaluation.qualifications_evaluation.similarity_score:.2%}")
    print(f"\nFinal Recommendation:")
    print(evaluation.recommendation)
    print("=" * 80)
    print("\nFull report saved to: results/evaluation_report.json")


if __name__ == "__main__":
    main()
