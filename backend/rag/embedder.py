import chromadb
import json
from sentence_transformers import SentenceTransformer
from backend.config import CHROMA_DB_PATH

def embed_sample_stories():
    """Load sample stories into ChromaDB"""
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection("stories")
    
    # Load sample stories
    with open("data/sample_stories.json", "r") as f:
        stories = json.load(f)
    
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    documents = []
    embeddings = []
    ids = []
    metadatas = []
    
    for i, story in enumerate(stories):
        text = f"{story['topic']} {story['genre']} {story['script']}"
        embedding = model.encode(text).tolist()
        
        documents.append(story["script"])
        embeddings.append(embedding)
        ids.append(f"story_{i}")
        metadatas.append({
            "topic": story["topic"],
            "genre": story["genre"]
        })
    
    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    
    print(f"Embedded {len(stories)} stories into ChromaDB")

if __name__ == "__main__":
    embed_sample_stories()