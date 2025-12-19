from langchain_ollama import OllamaEmbeddings
from main import LoggerSetup,CvmodelOutput,DescmodelOutput
import numpy as np
import time

# This is the dimension of the embeddings
class Embeddings:
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info(f"{self.__class__.__name__} instance initialized")
        try:
            self.embeddings = OllamaEmbeddings(model="snowflake-arctic-embed2:latest")
            self.logger.info("OllamaEmbeddings model 'snowflake-arctic-embed2:latest' loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load OllamaEmbeddings model: {str(e)}", exc_info=True)
            raise
    
    def _get_embeddings(self, text: str) -> list[float]:
        """Generate embeddings for a single text."""
        if not text or not text.strip():
            self.logger.warning("Empty or whitespace-only text provided for embedding")
            # Return a zero vector for empty text
            return [0.0] * 1024  # Adjust dimension based on your model
        
        try:
            start_time = time.time()
            embeddings = self.embeddings.embed_query(text)
            elapsed = time.time() - start_time
            self.logger.debug(f"Generated embeddings for text (length: {len(text)} chars) in {elapsed:.3f}s")
            return embeddings
        except Exception as e:
            self.logger.error(f"Failed to generate embeddings for text: {str(e)}", exc_info=True)
            raise

    def _get_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        if not texts:
            self.logger.warning("Empty text list provided for batch embedding")
            return []
        
        try:
            start_time = time.time()
            embeddings = self.embeddings.embed_documents(texts)
            elapsed = time.time() - start_time
            self.logger.debug(f"Generated batch embeddings for {len(texts)} texts in {elapsed:.3f}s")
            return embeddings
        except Exception as e:
            self.logger.error(f"Failed to generate batch embeddings: {str(e)}", exc_info=True)
            raise

    def _cosine_similarity(self, embeddings1: list[float], embeddings2: list[float]) -> float:
        """Calculate cosine similarity between two embedding vectors."""
        try:
            # Fixed: removed "1 -" to get actual similarity (0-1) instead of distance
            similarity = np.dot(embeddings1, embeddings2) / (np.linalg.norm(embeddings1) * np.linalg.norm(embeddings2))
            self.logger.debug(f"Calculated cosine similarity: {similarity:.4f}")
            return float(similarity)
        except Exception as e:
            self.logger.error(f"Failed to calculate cosine similarity: {str(e)}", exc_info=True)
            raise

    def _get_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        self.logger.debug(f"Calculating similarity between texts (lengths: {len(text1)}, {len(text2)} chars)")
        return self._cosine_similarity(self._get_embeddings(text1), self._get_embeddings(text2)) + 0.2

    def run(self, cv: dict[str, str], desc: dict[str, str]) -> dict[str, float | dict[str, float]]:
        """
        Compare a CV with a job description using a holistic approach.
        
        Logic:
            1. Concatenate all CV sections into one full context.
            2. Compare EACH part of the JD (Requirements, Responsibilities, Quals) 
               against the FULL CV context.
        """
        self.logger.info("Starting CV and job description comparison")
        start_time = time.time()
        
        try:
            # Validate inputs
            if not cv or not desc:
                self.logger.error("CV or job description is None or empty")
                raise ValueError("Both CV and job description must be provided")
            
            # 1. PREPARE THE FULL CV CONTEXT
            # We join all values to ensure the model sees the complete picture of the candidate
            self.logger.debug("Constructing full CV context")
            cv_parts = [
                cv.get("education", ""),
                cv.get("experience", ""),
                cv.get("skills", ""),
                cv.get("certifications", ""),
                cv.get("projects", ""),
                cv.get("summary", "") # Added summary if available
            ]
            # Join with spaces/newlines to prevent word merging
            full_cv_text = " \n ".join([part for part in cv_parts if part])
            
            self.logger.debug(f"Full CV context length: {len(full_cv_text)} chars")
            
            # Extract JD components
            desc_requirements = desc.get("requirements", "")
            desc_responsibilities = desc.get("responsibilities", "")
            desc_qualifications = desc.get("qualifications", "")
            
            # 2. CALCULATE SIMILARITY (JD Component vs. FULL CV)
            
            # Requirements vs Full CV
            self.logger.info("Calculating requirements similarity")
            requirements_similarity = self._get_similarity(desc_requirements, full_cv_text)
            
            # Responsibilities vs Full CV
            self.logger.info("Calculating responsibilities similarity")
            responsibilities_similarity = self._get_similarity(desc_responsibilities, full_cv_text)
            
            # Qualifications vs Full CV
            self.logger.info("Calculating qualifications similarity")
            qualifications_similarity = self._get_similarity(desc_qualifications, full_cv_text)
            
            # Overall Similarity (Full JD vs Full CV)
            self.logger.info("Calculating overall similarity")
            full_desc_text = f"{desc_requirements} \n {desc_responsibilities} \n {desc_qualifications}"
            overall_similarity = self._get_similarity(full_desc_text, full_cv_text)
            
            # Calculate mean
            mean_similarity = (
                (requirements_similarity * 0.5) + 
                (responsibilities_similarity * 0.3) + 
                (qualifications_similarity * 0.2)
            )
            
            overall = {
                "raw": overall_similarity,
                "mean": mean_similarity
            }
            
            result = {
                "requirements": requirements_similarity,
                "responsibilities": responsibilities_similarity,
                "qualifications": qualifications_similarity,
                "overall": overall
            }
            
            elapsed = time.time() - start_time
            self.logger.info(f"CV comparison completed successfully in {elapsed:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error during embedding comparison: {str(e)}", exc_info=True)
            raise