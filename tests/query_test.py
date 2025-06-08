from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest

# --- 1. Load model and connect to Qdrant
model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="localhost", port=6333)

collection_name = "sofie_test"

# --- 2. Define your search query
query_text = "what is sofie for?"
query_vector = model.encode(query_text).tolist()

# --- 3. Run semantic search
search_results = client.query_points(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=3,
    with_payload=True,
)

# --- 4. Show results
print(f"\n🔍 Results for query: '{query_text}'\n")

for i, point in enumerate(search_results, 1):
    print(f"Result {i}:")
    print(f"  ID:       {point.id}")
    print(f"  Score:    {point.score:.4f}")
    print(f"  Preview:  {point.payload.get('preview', '')[:100]}...\n")
