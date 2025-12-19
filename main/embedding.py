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
        return self._cosine_similarity(self._get_embeddings(text1), self._get_embeddings(text2))

    def run(self, cv: dict[str, str], desc: dict[str, str]) -> dict[str, float | dict[str, float]]:
        """
        Compare a CV with a job description.
        
        Args:
            cv: The CV to compare
            desc: The job description to compare
        Logic:
            1. requirements will be compared to education and projects
            2. responsibilities will be compared to experience and projects
            3. qualifications will be compared to skills and certifications
            4. overall {
                raw : will be the actual similarity score between the entire cv and job description 
                mean: will be the mean of the other parts
            }
        Returns:
            Object with the similarity score for each part of the job description
            {
                    requirements: float
                    responsibilities: float
                    qualifications: float
                    overall: {
                        raw: float
                        mean: float
                    }
            }
        """
        self.logger.info("Starting CV and job description comparison")
        start_time = time.time()
        
        try:
            # Validate inputs
            if not cv or not desc:
                self.logger.error("CV or job description is None or empty")
                raise ValueError("Both CV and job description must be provided")
            
            # Extract the desired parts from the cv and job description
            self.logger.debug("Extracting CV components")
            cv_education = cv.get("education", "")
            cv_experience = cv.get("experience", "")
            cv_skills = cv.get("skills", "")
            cv_certifications = cv.get("certifications", "")
            cv_projects = cv.get("projects", "")
            
            self.logger.debug(f"CV components - education: {len(cv_education)} chars, experience: {len(cv_experience)} chars, "
                            f"skills: {len(cv_skills)} chars, certifications: {len(cv_certifications)} chars, "
                            f"projects: {len(cv_projects)} chars")
            
            self.logger.debug("Extracting job description components")
            desc_requirements = desc.get("requirements", "")
            desc_responsibilities = desc.get("responsibilities", "")
            desc_qualifications = desc.get("qualifications", "")
            
            self.logger.debug(f"Job description components - requirements: {len(desc_requirements)} chars, "
                            f"responsibilities: {len(desc_responsibilities)} chars, "
                            f"qualifications: {len(desc_qualifications)} chars")
            
            # Calculate the similarity for each part
            self.logger.info("Calculating requirements similarity (requirements vs education + projects)")
            requirements_similarity = self._get_similarity(desc_requirements, cv_education + cv_projects)
            self.logger.info(f"Requirements similarity: {requirements_similarity:.4f}")
            
            self.logger.info("Calculating responsibilities similarity (responsibilities vs experience + projects)")
            responsibilities_similarity = self._get_similarity(desc_responsibilities, cv_experience + cv_projects)
            self.logger.info(f"Responsibilities similarity: {responsibilities_similarity:.4f}")
            
            self.logger.info("Calculating qualifications similarity (qualifications vs skills + certifications)")
            qualifications_similarity = self._get_similarity(desc_qualifications, cv_skills + cv_certifications)
            self.logger.info(f"Qualifications similarity: {qualifications_similarity:.4f}")
            
            # Calculate the overall similarity
            self.logger.info("Calculating overall similarity (all job desc vs all CV)")
            overall_similarity = self._get_similarity(desc_requirements + desc_responsibilities + desc_qualifications,
                                                      cv_education + cv_experience + cv_skills + cv_certifications + cv_projects)
            self.logger.info(f"Overall raw similarity: {overall_similarity:.4f}")
            
            mean_similarity = (requirements_similarity + responsibilities_similarity + qualifications_similarity) / 3
            self.logger.info(f"Overall mean similarity: {mean_similarity:.4f}")
            
            overall = {
                "raw": overall_similarity,
                "mean": mean_similarity
            }
            
            # Return the results
            result = {
                "requirements": requirements_similarity,
                "responsibilities": responsibilities_similarity,
                "qualifications": qualifications_similarity,
                "overall": overall
            }
            
            elapsed = time.time() - start_time
            self.logger.info(f"CV comparison completed successfully in {elapsed:.2f}s")
            self.logger.info(f"Final results: {result}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error during embedding comparison: {str(e)}", exc_info=True)
            raise

