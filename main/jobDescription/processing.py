class JobDescriptionProcessing:
    """
    Main Exposed Function for Job Description Processing
    Is : run (self , jd_content:str) -> dict[str , str] 
    """
    def __init__(self):
        pass
    
    def __extract_requirements(self , jd_content : str) -> str:
        pass

    def __extract_responsibilities(self , jd_content : str) -> str:
        pass

    def __extract_qualifications(self , jd_content : str) -> str:
        pass

    def run(self , jd_content : str) -> dict[str , str]:
        requirements = self.__extract_requirements(jd_content)
        responsibilities = self.__extract_responsibilities(jd_content)
        qualifications = self.__extract_qualifications(jd_content)
        return {"requirements": requirements, "responsibilities": responsibilities, "qualifications": qualifications}

