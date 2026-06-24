from pydantic import BaseModel

class PredictRequest(BaseModel):
    text: str

class Entity(BaseModel):
    text: str
    label: str
    score: float

class PredictResponse(BaseModel):
    entities: list[Entity]
