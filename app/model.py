from transformers import pipeline
from .settings import settings

LABEL_MAP = {
    "ORG": "Organization",
    "LOC": "Location",
    "PER": "Person",
    "MISC": "Miscellaneous",
}

ner_pipeline = pipeline(
    "token-classification",
    model=settings.HF_MODEL,
    tokenizer=settings.HF_MODEL,
    aggregation_strategy="simple"
)

def predict_entities(text: str):
    predictions = ner_pipeline(text)

    return [
        {
            "text": p["word"],
            # "label": p["entity_group"],
            "label": LABEL_MAP.get(p["entity_group"], p["entity_group"]),
            "score": round(float(p["score"]), 4),
        }
        for p in predictions
    ]
