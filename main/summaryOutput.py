from pydantic import BaseModel

class SummaryOutput(BaseModel):
    output: str