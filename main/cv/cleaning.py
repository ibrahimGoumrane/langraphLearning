class CvCleaning:
    """
    Main Exposed Function for CV Cleaning
    Is : run(self , cv_content : str) -> str 
    """
    def __init__(self):
        pass

    def __remove_special_characters(self , cv_content : str) -> str:
        """
        Private Function for Removing Special Characters
        Is : __remove_special_characters(self , cv_content : str) -> str 
        """
        pass    

    def __remove_extra_spaces(self , cv_content : str) -> str:
        """
        Private Function for Removing Extra Spaces
        Is : __remove_extra_spaces(self , cv_content : str) -> str 
        """
        pass        

    def __remove_extra_newlines(self , cv_content : str) -> str:
        """
        Private Function for Removing Extra Newlines
        Is : __remove_extra_newlines(self , cv_content : str) -> str 
        """
        pass    


    def run(self , cv_content : str) -> str:
        """
        Main Exposed Function for CV Cleaning
        Is : run(self , cv_content : str) -> str 
        """
        cv_content = self.__remove_special_characters(cv_content)
        cv_content = self.__remove_extra_spaces(cv_content)
        cv_content = self.__remove_extra_newlines(cv_content)
        return cv_content