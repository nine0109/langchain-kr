from pydantic import BaseModel
from typing import Optional, List
from fastapi import UploadFile

class QueryRequest(BaseModel):
    query: str
    model: Optional[str] = "deepseek"

class DocumentUpload(BaseModel):
    files: List[UploadFile]
    description: Optional[str] = None

class VectorDBUpdate(BaseModel):
    force_rebuild: Optional[bool] = False