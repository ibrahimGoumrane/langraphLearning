from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from dotenv import load_dotenv
from utils import LoggerSetup

class Retreival:
    """
    Main Exposed Function for  Retreival
    Is : run(self , path : str , type : str = "pdf") -> str 
    """
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("Retreival instance initialized")

    def __load_docx(self , path : str) -> str:
        """
        Private Function for Loading  
        Word File so the f.read() will not work
        Is : __load_docx(self , path : str) -> str 
        """
        try:
            self.logger.info(f"Loading DOCX file from: {path}")
            loader = Docx2txtLoader(path)
            content = ""
            for page in loader.lazy_load():
                content += page.page_content
            
            output_path = "../files/docx/cvpfe.txt"
            with open(output_path , "w") as f:
                f.write(content)
            
            self.logger.info(f"Successfully loaded DOCX file. Content length: {len(content)} characters")
            self.logger.debug(f"Content saved to: {output_path}")
            return content
        except Exception as e:
            self.logger.error(f"Error loading DOCX file from {path}: {str(e)}", exc_info=True)
            raise
    def __load_txt(self , path : str) -> str:
        """
        Private Function for Loading  
        Txt File so the f.read() will not work
        Is : __load_txt(self , path : str) -> str 
        """
        try:
            self.logger.info(f"Loading TXT file from: {path}")
            loader = TextLoader(path , encoding="utf-8")
            content = ""
            for page in loader.lazy_load():
                content += page.page_content
            
            output_path = "../files/txt/cvpfe.txt"
            with open(output_path , "w") as f:
                f.write(content)
            
            self.logger.info(f"Successfully loaded TXT file. Content length: {len(content)} characters")
            self.logger.debug(f"Content saved to: {output_path}")
            return content
        except Exception as e:
            self.logger.error(f"Error loading TXT file from {path}: {str(e)}", exc_info=True)
            raise
    def __load_pdf(self , path : str) -> str:
        """
        Private Function for Loading  
        Pdf File so the f.read() will not work
        Is : __load_pdf(self , path : str) -> str 
        """
        try:
            self.logger.info(f"Loading PDF file from: {path}")
            loader = PyPDFLoader(path , images_inner_format="markdown-img")
            # Write the extracted Content to a file
            content = ""
            for page in loader.lazy_load():
                content += page.page_content
            
            output_path = "../files/pdf/cvpfe.txt"
            with open(output_path , "w") as f:
                f.write(content)
            
            self.logger.info(f"Successfully loaded PDF file. Content length: {len(content)} characters")
            self.logger.debug(f"Content saved to: {output_path}")
            return content
        except Exception as e:
            self.logger.error(f"Error loading PDF file from {path}: {str(e)}", exc_info=True)
            raise


    def run(self , path : str , type : str = "pdf") -> str:
        """
        Main Exposed Function for  Retreival
        Is : run(self , path : str , type : str = "pdf") -> str 
        Args:
            path (str): Path to the File
            type (str): Type of the File (pdf , docx , txt)
        """
        self.logger.info(f"Starting file retrieval - Type: {type}, Path: {path}")
        
        try:
            if type == "pdf":
                result = self.__load_pdf(path)
            elif type == "docx":
                result = self.__load_docx(path)
            elif type == "txt":
                result = self.__load_txt(path)
            else:
                self.logger.error(f"Invalid file type specified: {type}")
                raise ValueError(f"Invalid File Type: {type}. Supported types: pdf, docx, txt")
            
            self.logger.info(f"File retrieval completed successfully for {type} file")
            return result
        except Exception as e:
            self.logger.error(f"File retrieval failed: {str(e)}", exc_info=True)
            raise


if __name__ == "__main__":
    retreival = Retreival()
    print("Loading PDF File...")
    retreival.run("../files/pdf/cvpfe.pdf")
    print("PDF File Loaded Successfully")
    print("Loading Docx File...")
    retreival.run("../files/docx/cvpfe.docx" , "docx")
    print("Docx File Loaded Successfully")
    print("Loading Txt File...")
    retreival.run("../files/txt/cvpfe.txt" , "txt")
    print("Txt File Loaded Successfully")