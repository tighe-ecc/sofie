# sofie/core/client.py
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

COLLECTION_NAME = "sofie_test"

_client_instance = None

def get_qdrant_client():
    global _client_instance
    if _client_instance is None:
        _client_instance = QdrantClient(
            host="localhost",
            grpc_port=6334,
            prefer_grpc=True,
            timeout=3.0,
        )

        # Live test to confirm connection is working
        try:
            collections = _client_instance.get_collections().collections
            print(f"✅ Qdrant connected. Found {len(collections)} collections.")
        except Exception as e:
            print("❌ Qdrant test failed:", e)

    return _client_instance

def ensure_collection(client, collection_name, vector_size):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
