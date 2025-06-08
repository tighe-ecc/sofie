# sofie/core/indexer.py
import hashlib
import uuid
from pathlib import Path
from qdrant_client.models import PointStruct
from .embedder import load_model, embed_text
from .client import get_qdrant_client, ensure_collection, COLLECTION_NAME

def index_file(file_path: Path):
    model = load_model()
    client = get_qdrant_client()
    text = file_path.read_text()
    embedding = embed_text(model, text)
    ensure_collection(client, COLLECTION_NAME, len(embedding))

    file_hash = hashlib.sha256(str(file_path).encode()).hexdigest()
    doc_id = str(uuid.UUID(file_hash[:32]))

    point = PointStruct(
        id=doc_id,
        vector=embedding,
        payload={
            "source": str(file_path),
            "length": len(text),
            "type": "text",
            "preview": text[:200],
        },
    )

    client.upsert(collection_name=COLLECTION_NAME, points=[point])
    print(f"Indexed {file_path.name} into collection '{COLLECTION_NAME}'")