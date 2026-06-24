from fastapi import FastAPI
from .schemas import PredictRequest, PredictResponse
from .model import predict_entities

app = FastAPI(title="NER API")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest):
    entities = predict_entities(payload.text)
    print(entities)
    return {"entities": entities}
