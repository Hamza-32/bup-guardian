import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

client = chromadb.PersistentClient(path=os.path.join(BASE_DIR, "chroma_db"))
ef = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_collection(name="bup_policies", embedding_function=ef)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(question):
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n\n".join(results['documents'][0])
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are BUP-Guardian, an assistant for Bangladesh University of Professionals. Answer questions based only on the provided context from BUP's official academic guidelines. If the answer is not in the context, say 'I could not find this in the BUP guidelines.'"
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Testing BUP-Guardian...\n")
    answer = ask("What is the motto of BUP?")
    print("Q: What is the motto of BUP?")
    print("A:", answer)