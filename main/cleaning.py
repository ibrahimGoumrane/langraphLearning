from utils import LoggerSetup

class Cleaning:
    """
    Main Exposed Function for Cleaning
    Is : run(self , cv_content : str) -> str 
    """
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("Cleaning instance initialized")

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


    def run(self , content : str) -> str:
        """
        Main Exposed Function for Cleaning
        Is : run(self , content : str) -> str 
        """
        self.logger.info(f"Starting Cleaning process. Content length: {len(content)} characters")
        
        try:
            content = self.__remove_special_characters(content)
            self.logger.debug("Special characters removed")
            
            content = self.__remove_extra_spaces(content)
            self.logger.debug("Extra spaces removed")
            
            content = self.__remove_extra_newlines(content)
            self.logger.debug("Extra newlines removed")
            
            self.logger.info(f"Cleaning completed. Final content length: {len(content)} characters")
            return content
        except Exception as e:
            self.logger.error(f"Error during Cleaning: {str(e)}", exc_info=True)
            raise