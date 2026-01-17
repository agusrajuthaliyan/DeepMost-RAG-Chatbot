import os
import chromadb
from chromadb.utils import embedding_functions
from google import genai 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# 1. Setup the Embedding Function
geminief = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=os.getenv("GEMINI_API_KEY"),
    model_name="models/text-embedding-004"
)

# 2. Initialize ChromaDB Client
client = chromadb.PersistentClient(path='./chroma_db')

# 3. Get or Create Collection 
collection = client.get_or_create_collection(
    name="deepmost_collection",
    embedding_function=geminief
)

# 4. Process Data
with open("data/raw/deepmost_data.md", "r", encoding="utf-8") as f:
    text = f.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

chunks = splitter.split_text(text)
print(f"Total chunks created: {len(chunks)}")

# 5. Generate IDs and Add to DB
ids = [f"id_{i}" for i in range(len(chunks))]

collection.add(
    documents=chunks,
    ids=ids
)

print("Successfully embedded the chunks into ChromaDB!")