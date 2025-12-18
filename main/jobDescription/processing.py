from utils import LoggerSetup

class JobDescriptionProcessing:
    """
    Main Exposed Function for Job Description Processing
    Is : run (self , jd_content:str) -> dict[str , str] 
    """
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("JobDescriptionProcessing instance initialized")
    
    def __extract_requirements(self , jd_content : str) -> str:
        pass

    def __extract_responsibilities(self , jd_content : str) -> str:
        pass

    def __extract_qualifications(self , jd_content : str) -> str:
        pass

    def run(self , jd_content : str) -> dict[str , str]:
        self.logger.info(f"Starting job description processing. Content length: {len(jd_content)} characters")
        
        try:
            requirements = self.__extract_requirements(jd_content)
            self.logger.debug("Requirements extracted")
            
            responsibilities = self.__extract_responsibilities(jd_content)
            self.logger.debug("Responsibilities extracted")
            
            qualifications = self.__extract_qualifications(jd_content)
            self.logger.debug("Qualifications extracted")
            
            result = {"requirements": requirements, "responsibilities": responsibilities, "qualifications": qualifications}
            self.logger.info("Job description processing completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error during job description processing: {str(e)}", exc_info=True)
            raise


