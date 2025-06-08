# sofie/cli/query.py
from pathlib import Path
from sofie.core.embedder import load_model, embed_text
from sofie.core.client import get_qdrant_client, COLLECTION_NAME

def query_text(query: str):
    model = load_model()
    client = get_qdrant_client()
    query_vector = embed_text(model, query)

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=3,
        with_payload=True,
    )

    print(f"\nResults for query: '{query}'\n")
    for i, point in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"  ID:      {point.id}")
        print(f"  Score:   {point.score:.4f}")
        print(f"  Preview: {point.payload.get('preview', '')[:100]}\n")
