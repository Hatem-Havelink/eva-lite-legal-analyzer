from pydantic import BaseModel
from fastapi import UploadFile

class UploadRequest(BaseModel):
    file: UploadFile

class AnalysisResponse(BaseModel):
    summary: str
    obligations: list[str]
    risks: dict
    sensitive_clauses: list[str]
