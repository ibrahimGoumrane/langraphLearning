from utils import LoggerSetup

class CvProcessing:
    """
    Main Exposed Function for CV Processing
    Is : run (self , cv_content:str) -> dict[str , str] 
    """
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("CvProcessing instance initialized")
    
    def __extract_education(self , cv_content : str) -> str:
        pass

    def __extract_skills(self , cv_content : str) -> str:
        pass

    def __extract_experience(self , cv_content : str) -> str:
        pass

    def run(self , cv_content : str) -> dict[str , str]:
        self.logger.info(f"Starting CV processing. Content length: {len(cv_content)} characters")
        
        try:
            education = self.__extract_education(cv_content)
            self.logger.debug("Education information extracted")
            
            skills = self.__extract_skills(cv_content)
            self.logger.debug("Skills information extracted")
            
            experience = self.__extract_experience(cv_content)
            self.logger.debug("Experience information extracted")
            
            result = {"education": education, "skills": skills, "experience": experience}
            self.logger.info("CV processing completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error during CV processing: {str(e)}", exc_info=True)
            raise


