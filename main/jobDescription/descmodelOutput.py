from pydantic import BaseModel
from typing import List

class Requirement(BaseModel):
    name:str
    
class Responsibility(BaseModel):
    name:str
    
class Qualification(BaseModel):
    name:str
    
class DescmodelOutput(BaseModel):
    requirements: List[Requirement]
    responsibilities: List[Responsibility]
    qualifications: List[Qualification]
    
