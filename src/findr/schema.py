from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Literal
from datetime import datetime

TypeT = Literal["job","contract","gig","apprenticeship","training","tender"]

class Opportunity(BaseModel):
    op_id: str
    source: str
    title: str
    org: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    url: Optional[HttpUrl] = None
    region: Optional[str] = None
    type: TypeT = "job"
    pay_min: Optional[float] = None
    pay_max: Optional[float] = None
    pay_unit: Optional[str] = None
    close_at: Optional[datetime] = None
    requirements: List[str] = []
    tags: List[str] = []
    raw_path: Optional[str] = None

class MatchResult(BaseModel):
    op_id: str
    score: float
    explain: List[str] = []
