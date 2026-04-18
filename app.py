import os
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="BUP-Guardian",
    page_icon="🎓",
    layout="centered"
)

@st.cache_resource
def load_db():
    client = chromadb.PersistentClient(path=os.path.join(BASE_DIR, "chroma_db"))
    ef = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_collection(name="bup_policies", embedding_function=ef)
    return collection

@st.cache_resource
def load_groq():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

collection = load_db()
groq_client = load_groq()

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

st.title("🎓 BUP-Guardian")
st.caption("Your 24/7 assistant for BUP academic policies and guidelines")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask anything about BUP rules..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Searching BUP guidelines..."):
        answer = ask(prompt)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)