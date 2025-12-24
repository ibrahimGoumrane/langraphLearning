from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from main import LoggerSetup
import pypdfium2 as pdfium
import pytesseract

class Retreival:
    """
    Main Exposed Function for  Retreival
    Is : run(self , path : str , type : str = "pdf") -> str 
    """
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("Retreival instance initialized")
        self.save_path = "temp"
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
            
            self.logger.info(f"Successfully loaded DOCX file. Content length: {len(content)} characters")
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
            
            self.logger.info(f"Successfully loaded TXT file. Content length: {len(content)} characters")
            return content
        except Exception as e:
            self.logger.error(f"Error loading TXT file from {path}: {str(e)}", exc_info=True)
            raise
    

    def _convert_pdf_to_images(self, file_path: str, scale: float = 300/72):
        """
        Convert each page of the PDF to a PIL image.
        """
        pdf_file = pdfium.PdfDocument(file_path)
        images = []
        page_indices = list(range(len(pdf_file)))

        for i in page_indices:
            page = pdf_file[i]
            bitmap = page.render(scale=scale)           # render the page
            pil_image = bitmap.to_pil()                 # convert to PIL
            images.append(pil_image)
            bitmap.close()                              # free bitmap resources

        return images, page_indices

    def __load_pdf(self, path: str) -> str:
        """
        Load PDF file by converting it to images and extracting text using pytesseract OCR.
        """
        try:
            self.logger.info(f"Loading PDF file from: {path}")
            content = ""

            images, page_indices = self._convert_pdf_to_images(path)

            for i, image in zip(page_indices, images):
                self.logger.info(f"Processing page {i+1} with OCR")
                page_text = pytesseract.image_to_string(image)
                content += page_text + "\n"

            self.logger.info(f"Successfully loaded PDF file. Content length: {len(content)} characters")
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