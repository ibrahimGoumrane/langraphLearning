class CvProcessing:
    """
    Main Exposed Function for CV Processing
    Is : run (self , cv_content:str) -> dict[str , str] 
    """
    def __init__(self):
        pass
    
    def __extract_education(self , cv_content : str) -> str:
        pass

    def __extract_skills(self , cv_content : str) -> str:
        pass

    def __extract_experience(self , cv_content : str) -> str:
        pass

    def run(self , cv_content : str) -> dict[str , str]:
        education = self.__extract_education(cv_content)
        skills = self.__extract_skills(cv_content)
        experience = self.__extract_experience(cv_content)
        return {"education": education, "skills": skills, "experience": experience}

