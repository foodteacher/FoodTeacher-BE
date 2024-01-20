from pydantic import BaseModel

class GuestBase(BaseModel):
    query: str
    height: float = None
    weight: float = None
    age: int = None
    gender: str = None
    target_weight: float = None