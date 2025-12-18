class CvRetreival:
    """
    Main Exposed Function for CV Retreival
    Is : run(self , cv_path : str , type : str = "pdf") -> str 
    """
    def __init__(self):
        pass


    def __load_pdf(self , cv_path : str) -> str:
        """
        Private Function for Loading CV 
        Pdf File so the f.read() will not work
        Is : __load_pdf(self , cv_path : str) -> str 
        """
        pass


    def run(self , cv_path : str , type : str = "pdf") -> str:
        """
        Main Exposed Function for CV Retreival
        Is : run(self , cv_path : str , type : str = "pdf") -> str 
        """
        cv_content = self.__load_pdf(cv_path)
        return cv_content