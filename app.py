import os
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(page_title="Deepmost AI Assistant", page_icon="🤖")
st.title("🤖 Deepmost AI Assistant")

# Initialize Gemini & ChromaDB
gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=os.getenv("GEMINI_API_KEY"),
    model_name="models/text-embedding-004"
)
client = chromadb.PersistentClient(path='./chroma_db')
collection = client.get_collection(name="deepmost_collection", embedding_function=gemini_ef)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# --- SESSION STATE (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("How can I help you today?"):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. RAG Retrieval
    results = collection.query(query_texts=[prompt], n_results=3)
    context = "\n\n".join(results['documents'][0])

    # 3. Generate Answer
    with st.chat_message("assistant"):
        # We include the last 2 messages for a small "memory" window
        history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-3:]])
        
        full_prompt = f"""
        You are an expert for a startup called DeepmostAI. Answer based ONLY on the context provided. If you don't know the answer to any questions, please do mention that you dont know.
        CONTEXT: {context}
        CHAT HISTORY: {history_context}
        USER QUESTION: {prompt}
        """
        
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})