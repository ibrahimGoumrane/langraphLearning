class JobDescriptionCleaning:
    """
    Main Exposed Function for Job Description Cleaning
    Is : run(self , jd_content : str) -> str 
    """
    def __init__(self):
        pass

    def __remove_special_characters(self , jd_content : str) -> str:
        """
        Private Function for Removing Special Characters
        Is : __remove_special_characters(self , jd_content : str) -> str 
        """
        pass    

    def __remove_extra_spaces(self , jd_content : str) -> str:
        """
        Private Function for Removing Extra Spaces
        Is : __remove_extra_spaces(self , jd_content : str) -> str 
        """
        pass        

    def __remove_extra_newlines(self , jd_content : str) -> str:
        """
        Private Function for Removing Extra Newlines
        Is : __remove_extra_newlines(self , jd_content : str) -> str 
        """
        pass    


    def run(self , jd_content : str) -> str:
        """
        Main Exposed Function for Job Description Cleaning
        Is : run(self , jd_content : str) -> str 
        """
        jd_content = self.__remove_special_characters(jd_content)
        jd_content = self.__remove_extra_spaces(jd_content)
        jd_content = self.__remove_extra_newlines(jd_content)
        return jd_content