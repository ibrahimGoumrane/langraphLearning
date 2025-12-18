from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from dotenv import load_dotenv

class Retreival:
    """
    Main Exposed Function for  Retreival
    Is : run(self , path : str , type : str = "pdf") -> str 
    """
    def __init__(self):
        pass

    def __load_docx(self , path : str) -> str:
        """
        Private Function for Loading  
        Word File so the f.read() will not work
        Is : __load_docx(self , path : str) -> str 
        """
        loader = Docx2txtLoader(path)
        content = ""
        for page in loader.lazy_load():
            content += page.page_content
        with open("../files/docx/cvpfe.txt" , "w") as f:
            f.write(content)
        return content
    def __load_txt(self , path : str) -> str:
        """
        Private Function for Loading  
        Txt File so the f.read() will not work
        Is : __load_txt(self , path : str) -> str 
        """
        loader = TextLoader(path , encoding="utf-8")
        content = ""
        for page in loader.lazy_load():
            content += page.page_content
        with open("../files/txt/cvpfe.txt" , "w") as f:
            f.write(content)
        return content
    def __load_pdf(self , path : str) -> str:
        """
        Private Function for Loading  
        Pdf File so the f.read() will not work
        Is : __load_pdf(self , path : str) -> str 
        """
        loader = PyPDFLoader(path , images_inner_format="markdown-img")
        # Write the extracted Content to a file
        content = ""
        for page in loader.lazy_load():
            content += page.page_content
        with open("../files/pdf/cvpfe.txt" , "w") as f:
            f.write(content)
        return content


    def run(self , path : str , type : str = "pdf") -> str:
        """
        Main Exposed Function for  Retreival
        Is : run(self , path : str , type : str = "pdf") -> str 
        Args:
            path (str): Path to the File
            type (str): Type of the File (pdf , docx , txt)
        """
        if type == "pdf":
            return self.__load_pdf(path)
        elif type == "docx":
            return self.__load_docx(path)
        elif type == "txt":
            return self.__load_txt(path)
        else:
            raise ValueError("Invalid File Type")


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