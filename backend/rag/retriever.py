import chromadb
from sentence_transformers import SentenceTransformer
from backend.config import CHROMA_DB_PATH

def retrieve_similar_stories(topic: str, n_results: int = 2) -> str:
    """Retrieve similar stories from ChromaDB"""
    try:
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collection = client.get_or_create_collection("stories")
        
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_embedding = model.encode(topic).tolist()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        if not results["documents"][0]:
            return "No similar stories found."
        
        similar = "Similar story examples:\n\n"
        for doc in results["documents"][0]:
            similar += f"{doc}\n\n---\n\n"
        
        return similar
    except Exception as e:
        return "No similar stories found."