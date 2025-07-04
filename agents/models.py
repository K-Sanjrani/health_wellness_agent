from pydantic import BaseModel
from typing import Optional, List, Dict

class UserSessionContext(BaseModel):
    name: str
    uid: int
    goals: List[str] = []
    preferences: Dict[str, str] = {}