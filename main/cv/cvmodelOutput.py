from pydantic import BaseModel
from typing import List

class Education(BaseModel):
    school:str
    degree:str
    field_of_study:str
    start_date:str
    end_date:str

class Skill(BaseModel):
    name:str

class Experience(BaseModel):
    company:str
    position:str
    start_date:str
    end_date:str
    description:str
    
class Certification(BaseModel):
    name:str

    
class Project(BaseModel):
    name:str
    description:str
    
class CvmodelOutput(BaseModel):
    education: List[Education]
    skills: List[Skill]
    experience: List[Experience]
    certifications: List[Certification]
    projects: List[Project]