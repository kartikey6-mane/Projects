from pydantic import BaseModel
from typing import List, Optional

class ChatIn(BaseModel):
    text: str

class FaqOut(BaseModel):
    id: int
    category: str
    question: str
    answer: str
    score: float

class ChatOut(BaseModel):
    reply: str
    matches: Optional[List[FaqOut]] = None