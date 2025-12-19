from main import LoggerSetup
from langchain_ollama import ChatOllama
from abc import ABC, abstractmethod
from typing import Any


class BaseProcessing(ABC):
    """
    Base class for processing CV and Job Description content.
    Provides common extraction logic with customizable admin messages.
    """
    
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info(f"{self.__class__.__name__} instance initialized")
    
    @abstractmethod
    def get_admin_message_template(self, extracted_part: str) -> str:
        """
        Get the admin message template for the specific processing type.
        Must be implemented by subclasses.
        
        Args:
            extracted_part: The part to extract (e.g., 'education', 'skills', 'requirements')
            
        Returns:
            str: The admin message content
        """
        pass
    
    @abstractmethod
    def get_output_schema(self) -> Any:
        """
        Get the output schema for structured output.
        Must be implemented by subclasses.
        
        Returns:
            The Pydantic schema class
        """
        pass
    
    @abstractmethod
    def get_content_type_name(self) -> str:
        """
        Get the name of the content type being processed (e.g., 'CV', 'Job Description').
        Used for logging and user messages.
        
        Returns:
            str: Content type name
        """
        pass
    
    def _pass_to_agent(self, content: str, extracted_part: str) -> Any:
        """
        Pass content to LLM agent to extract structured information.
        Uses deepseek-r1:latest model.
        
        Args:
            content: The content to process
            extracted_part: The specific part to extract
            
        Returns:
            Structured output based on the schema
        """
        llm = ChatOllama(
            model="deepseek-r1:latest",
            temperature=0.0,
            reasoning=False,
            format="json"
        ).with_structured_output(schema=self.get_output_schema())
        
        # Get the customized admin message from the subclass
        admin_message = {
            "role": "system",
            "content": self.get_admin_message_template(extracted_part)
        }
        
        chat_message = {
            "role": "user",
            "content": f"{self.get_content_type_name()} Content:\n{content}\n\nExtract {extracted_part}."
        }
        
        response = llm.invoke([admin_message, chat_message])
        return response
    
    @abstractmethod
    def flatten_objects_to_string(self, objects: Any) -> str:
        """
        Flatten a list of objects to a string.
        Must be implemented by subclasses.
        
        Args:
            objects: The list of objects to flatten
            
        Returns:
            str: The flattened string
        """
        pass

    @abstractmethod
    def run(self, content: str) -> Any:
        """
        Main method to process the content.
        Must be implemented by subclasses.
        
        Args:
            content: The content to process
            
        Returns:
            Processed and structured output
        """
        pass
