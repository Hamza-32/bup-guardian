import chromadb
import json
from chromadb.utils import embedding_functions

# Load chunks
with open(r"e:\Semester8\AI\Lab\Project\bup-guardian\chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# Set up ChromaDB with built-in embedding (no sentence-transformers needed)
client = chromadb.PersistentClient(path=r"e:\Semester8\AI\Lab\Project\bup-guardian\chroma_db")

ef = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="bup_policies",
    embedding_function=ef
)

# Store chunks in batches
print("Storing chunks in ChromaDB...")
ids = [f"chunk_{i}" for i in range(len(chunks))]

collection.add(
    documents=chunks,
    ids=ids
)

print(f"Successfully stored {len(chunks)} chunks!")
print("Vector database ready at chroma_db/")