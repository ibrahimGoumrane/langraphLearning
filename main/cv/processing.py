from main.processing import BaseProcessing
from main.cv.cvmodelOutput import CvmodelOutput
from typing import Any


class CvProcessing(BaseProcessing):
    """
    CV Processing Class - inherits from BaseProcessing.
    Method: run(cv_content: str) -> CvmodelOutput
    Extracts: education, skills, experience, certifications, projects
    """
    def __init__(self):
        super().__init__()
    def get_admin_message_template(self, extracted_part: str) -> str:
        """
        Get CV-specific admin message template.
        
        Args:
            extracted_part: The part to extract (education, skills, etc.)
            
        Returns:
            str: CV extractor admin message
        """
        return (
            f"You are a professional CV extractor. "
            f"Extract ONLY the {extracted_part} from the given CV content. "
            "Return the result in JSON format. "
            "If no relevant information is found, return null. "
            "Do not include explanations, opinions, or unrelated content."
        )
    
    def get_output_schema(self) -> Any:
        """Return the CV output schema."""
        return CvmodelOutput
    
    def get_content_type_name(self) -> str:
        """Return the content type name."""
        return "CV"
    
    def __extract_education(self, cv_content: str):
        return self._pass_to_agent(cv_content, "education")

    def __extract_skills(self, cv_content: str):
        return self._pass_to_agent(cv_content, "skills")

    def __extract_experience(self, cv_content: str):
        return self._pass_to_agent(cv_content, "experience")

    def __extract_certifications(self, cv_content: str):
        return self._pass_to_agent(cv_content, "certifications")

    def __extract_projects(self, cv_content: str):
        return self._pass_to_agent(cv_content, "projects")
   
    def flatten_objects_to_string(self , objects : dict) -> dict[str , str]:
        # Extract the parts of the cv (objects is a dict, not a Pydantic model)
        education = objects.get("education", [])
        skills = objects.get("skills", [])
        experience = objects.get("experience", [])
        certifications = objects.get("certifications", [])
        projects = objects.get("projects", [])

        # Flatten each part into its own string 
        education_str = ' '.join([f"{edu.degree} {edu.field_of_study} {edu.school}" for edu in education])
        skills_str = ' '.join([skill.name for skill in skills])
        experience_str = ' '.join([f"{exp.position} at {exp.company}. {exp.description}" for exp in experience])
        certifications_str = ' '.join([cert.name for cert in certifications])
        projects_str = ' '.join([f"{proj.name}. {proj.description}" for proj in projects])
    
        return {
            "education": education_str,
            "skills": skills_str,
            "experience": experience_str,
            "certifications": certifications_str,
            "projects": projects_str
        }

    def run(self, cv_content: str , output_format: str = "json") -> CvmodelOutput:
        """
        Process CV content and extract all sections.
        
        Args:
            cv_content: Raw CV text content
            output_format: Format of the output (json or string)
            
        Returns:
            CvmodelOutput: Structured CV data
        """
        self.logger.info(f"Starting CV processing. Content length: {len(cv_content)} characters")
        
        try:
            education = self.__extract_education(cv_content).education
            self.logger.debug("Education extracted")

            skills = self.__extract_skills(cv_content).skills
            self.logger.debug("Skills extracted")

            experience = self.__extract_experience(cv_content).experience
            self.logger.debug("Experience extracted")

            certifications = self.__extract_certifications(cv_content).certifications
            self.logger.debug("Certifications extracted")

            projects = self.__extract_projects(cv_content).projects
            self.logger.debug("Projects extracted")
            result: CvmodelOutput = {
                    "education": education,
                    "skills": skills,
                    "experience": experience,
                    "certifications": certifications,
                    "projects": projects
                }
            self.logger.info("CV processing completed successfully")
            self.logger.info(f"CV structured: {result}")
            if output_format == "json":
                return result
            elif output_format == "string":
                return self.flatten_objects_to_string(result)
        except Exception as e:
            self.logger.error(f"Error during CV processing: {str(e)}", exc_info=True)
            raise


if __name__ == "__main__":
    Text_content = """
    GOUMRANE IBRAHIM Software Engineer | Backend Java Specialist Casablanca, Morocco | +212 776 209 303 | ibrahimgoumrane01@gmail.com Portfolio: www.ibrahimgoumrane.dev

PROFESSIONAL SUMMARY Software Engineer specializing in AI and Backend Development with a strong foundation in Java and Spring Boot. Experienced in building scalable full-stack solutions, designing RESTful architectures, and deploying to cloud environments like AWS and GCP . seeking to leverage experience in microservices and data engineering to contribute to high-performance backend systems.





TECHNICAL SKILLS


Backend & Core: Java, Spring Boot, Python, SQL, RESTful APIs.


Data & Databases: MySQL, PostgreSQL, MongoDB, Redis.




DevOps & Cloud: Docker, AWS (Academy Graduate), GCP (Digital Leader), Linux, CI/CD.



Web & Frameworks: Laravel, React, Next.js, Django.

PROFESSIONAL EXPERIENCE

Full Stack Developer & Project Lead | EHC Remote | 01/06/2025 – 01/11/2025 

Developed a robust recruitment platform solution using Spring Boot and React.js.

Managed the deployment of backend services on VPS environments.

Led a dynamic team and coordinated directly with the client to meet strict deadlines.

Full Stack Developer & Project Lead (Freelance) | Financiana Remote | 01/06/2025 – 01/09/2025 

Architected a financial platform integrating automated AI analysis and OCR.

Implemented CI/CD pipelines via GitHub to streamline development and deployment.

Managed complex relational data structures using MySQL.

Software Engineer Intern | Numeric Way Remote | 27/06/2024 – 27/08/2024 

Built a Jira-style project management platform with real-time collaboration features.

Developed backend services and managed multi-user architecture.

KEY PROJECTS


FaceAttendance.AI: Automated attendance system utilizing Docker and Redis for high-performance data handling.


Rehab Management CMS: Developed a custom CMS using MySQL for patient tracking and exercise management.


MCP Server (Knowledge Management): Python-based server optimization using vector embeddings and document similarity algorithms.

EDUCATION

Diplôme d'Ingénieur in AI & Software Engineering École Nationale Supérieure d'Arts et Métiers (ENSAM), Casablanca | 2021 – 2026 

CERTIFICATIONS


AWS Academy Graduate - Cloud Foundations 


GCP Digital Leader 


Back-End Development - Meta 


Agile Development & Scrum - IBM
    """

    cv_processing = CvProcessing()
    print("Processing CV content...")
    cv_content = cv_processing.run(Text_content)
    print("CV Processing Complete!")

    # Save to csv
    with open("cv_content.txt", "w", newline="") as file:
        file.write(str(cv_content))

    print(cv_content)
