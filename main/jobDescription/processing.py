from main.processing import BaseProcessing
from main.jobDescription.descmodelOutput import DescmodelOutput
from typing import Any


class DescProcessing(BaseProcessing):
    """
    Job Description Processing Class - inherits from BaseProcessing.
    Method: run(jd_content: str) -> DescmodelOutput
    Extracts: requirements, responsibilities, qualifications
    """
    
    def get_admin_message_template(self, extracted_part: str) -> str:
        """
        Get Job Description-specific admin message template.
        
        Args:
            extracted_part: The part to extract (requirements, responsibilities, etc.)
            
        Returns:
            str: Job Description extractor admin message
        """
        return (
            f"You are a professional Job Description analyzer. "
            f"Extract ONLY the {extracted_part} from the given Job Description content. "
            "Return the result in JSON format. "
            "If no relevant information is found, return null. "
            "Do not include explanations, opinions, or unrelated content."
        )
    
    def get_output_schema(self) -> Any:
        """Return the Job Description output schema."""
        return DescmodelOutput
    
    def get_content_type_name(self) -> str:
        """Return the content type name."""
        return "Job Description"
    
    def __extract_requirements(self, jd_content: str):
        return self._pass_to_agent(jd_content, "requirements")

    def __extract_responsibilities(self, jd_content: str):
        return self._pass_to_agent(jd_content, "responsibilities")

    def __extract_qualifications(self, jd_content: str):
        return self._pass_to_agent(jd_content, "qualifications")
    def flatten_objects_to_string(self , objects : dict) -> dict[str , str]:
        # Extract the parts of the job description (objects is a dict, not a Pydantic model)
        requirements = objects.get("requirements", [])
        responsibilities = objects.get("responsibilities", [])
        qualifications = objects.get("qualifications", [])

        # Flatten each part into its own string 
        requirements_str = ' '.join([requirement.name for requirement in requirements])
        responsibilities_str = ' '.join([responsibility.name for responsibility in responsibilities])
        qualifications_str = ' '.join([qualification.name for qualification in qualifications])

        return {
            "requirements": requirements_str,
            "responsibilities": responsibilities_str,
            "qualifications": qualifications_str
        }
    def run(self, jd_content: str, output_format: str = "json") -> DescmodelOutput:
        """
        Process Job Description content and extract all sections.
        
        Args:
            jd_content: Raw Job Description text content
            output_format: Format of the output (json or string)
            
        Returns:
            DescmodelOutput: Structured Job Description data
        """
        self.logger.info(f"Starting job description processing. Content length: {len(jd_content)} characters")
        
        try:
            requirements = self.__extract_requirements(jd_content).requirements
            self.logger.debug("Requirements extracted")
            
            responsibilities = self.__extract_responsibilities(jd_content).responsibilities
            self.logger.debug("Responsibilities extracted")
            
            qualifications = self.__extract_qualifications(jd_content).qualifications
            self.logger.debug("Qualifications extracted")
            
            result: DescmodelOutput = {
                    "requirements": requirements,
                    "responsibilities": responsibilities,
                    "qualifications": qualifications
                }
            self.logger.info("Job description processing completed successfully")

            if output_format == "json":
                return result
            elif output_format == "string":
                return  self.flatten_objects_to_string(result)
                        
        except Exception as e:
            self.logger.error(f"Error during job description processing: {str(e)}", exc_info=True)
            raise



