import os
import chromadb
import json
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "chunks.json"), "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

client = chromadb.PersistentClient(path=os.path.join(BASE_DIR, "chroma_db"))
ef = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(name="bup_policies", embedding_function=ef)

print("Storing chunks in ChromaDB...")
ids = [f"chunk_{i}" for i in range(len(chunks))]
collection.add(documents=chunks, ids=ids)

print(f"Successfully stored {len(chunks)} chunks!")
print("Vector database ready!")