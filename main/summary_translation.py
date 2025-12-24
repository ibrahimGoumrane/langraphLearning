from langchain_ollama import ChatOllama
from main.utils import LoggerSetup
import json
from main.summaryOutput import SummaryOutput

class SummaryTranslation:
    """
    Text Processing for Summary and Translation using Granite3-Dense:8B
    Single function, single LLM call - summarizes and translates in one go.
    """
    
    def __init__(self, model: str = "granite3-dense:8b"):
        """Initialize with model name"""
        self.logger = LoggerSetup.get_logger(__name__)
        self.model = model
        self.logger.info(f"SummaryTranslation initialized with model: {model}")
    
    def run(
        self, 
        content: str, 
        target_length: int = 200,
        target_language: str = "English"
    ) -> str:
        """
        Extract key information and translate text in ONE LLM call
        
        Args:
            content: Text to process
            target_length: Target length in characters
            target_language: Target language for extraction
            
        Returns:
            Information-dense extracted text in target language
        """
        self.logger.info(f"Processing text: {len(content)} chars → {target_length} chars key extraction + {target_language} translation")
        
        try:
            llm = ChatOllama(
                model=self.model,
                temperature=0.3,
                reasoning=False,
                format="json"
            ).with_structured_output(schema=SummaryOutput)
            
            system_message = {
                "role": "system",
                "content": f"""You are an expert information extractor for CV-Job matching systems.
CRITICAL: The downstream matching system is BLIND and will ONLY see your extracted output.
Extract ALL key matching components and translate to {target_language}."""
            }
            
            user_message = {
                "role": "user",
                "content": f"""Extract key information from this CV/Job Description for matching purposes.

CRITICAL INSTRUCTIONS:
1. Extract ALL key components: skills, technologies, experience, qualifications, requirements, responsibilities
2. Preserve specific technical terms, tools, frameworks, certifications, years of experience
3. Include education levels, project types, domain expertise
4. Keep ALL matching-relevant information - the next system is blind to the original text
5. Be information-dense, prioritize completeness over brevity
6. Translate to {target_language}
7. Target approximately {target_length} characters (but prioritize completeness)

Text to extract from:
{content}

Return the information-dense extracted {target_language} text with ALL key matching components."""
            }
            
            response = llm.invoke([system_message, user_message])
            
            # Allow 20% overflow to preserve critical information
            max_length = int(target_length * 1.2)
            output = response.output[:max_length] if len(response.output) > max_length else response.output
            
            self.logger.info(f"Successfully extracted key information: {len(output)} chars")
            return output
            
        except Exception as e:
            self.logger.error(f"Error: {str(e)}", exc_info=True)
            raise


# Example usage
if __name__ == "__main__":
    processor = SummaryTranslation(model="granite3-dense:8b")
    
    sample_text = """
    John Doe is a Senior Software Engineer with 8 years of experience in full-stack development. 
    He specializes in Python, JavaScript, and cloud technologies including AWS and Azure. 
    John has led multiple teams and successfully delivered over 20 projects. 
    He holds a Master's degree in Computer Science and is certified in AWS Solutions Architecture.
    """
    
    result = processor.run(sample_text, target_length=150, target_language="Spanish")
    print(f"Result ({len(result)} chars): {result}")

