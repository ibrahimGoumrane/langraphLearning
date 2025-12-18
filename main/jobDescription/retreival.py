class JobDescriptionRetreival:
    """
    Main Exposed Function for Job Description Retreival
    Is : run(self , jd_path : str , type : str = "pdf") -> str 
    """
    def __init__(self):
        pass


    def __load_pdf(self , jd_path : str) -> str:
        """
        Private Function for Loading Job Description 
        Pdf File so the f.read() will not work
        Is : __load_pdf(self , jd_path : str) -> str 
        """
        pass


    def run(self , jd_path : str , type : str = "pdf") -> str:
        """
        Main Exposed Function for Job Description Retreival
        Is : run(self , jd_path : str , type : str = "pdf") -> str 
        """
        jd_content = self.__load_pdf(jd_path)
        return jd_content