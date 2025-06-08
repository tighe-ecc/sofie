from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import CollectionStatus, PointStruct, VectorParams, Distance
import hashlib
import uuid
from pathlib import Path

# --- 1. Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- 2. Read file
file_path = Path("testdata/example.txt")
text = file_path.read_text()

# --- 3. Embed full text (in real use, you'd chunk it first)
embedding = model.encode(text).tolist()

# --- 4. Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

collection_name = "sofie_test"

# --- 5. Create collection (if not already exists)
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=len(embedding), distance=Distance.COSINE),
    )

# --- 6. Create a unique ID for this file (based on path)
file_hash = hashlib.sha256(str(file_path).encode()).hexdigest()
doc_id = str(uuid.UUID(file_hash[:32]))

# --- 7. Prepare point with metadata ("payload")
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

# --- 8. Upsert point into Qdrant
client.upsert(collection_name=collection_name, points=[point])

print(f"✅ Indexed {file_path.name} into collection '{collection_name}'")
