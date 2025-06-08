# sofie/core/embedder.py
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_model_instance = None

def load_model():
    global _model_instance
    if _model_instance is None:
        _model_instance = SentenceTransformer(MODEL_NAME)
    return _model_instance

def embed_text(model, text):
    return model.encode(text).tolist()