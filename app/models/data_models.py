from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    sql_query: Optional[str] = None
    explanation: Optional[str] = None