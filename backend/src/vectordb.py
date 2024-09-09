from loguru import logger
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from backend.config.config import PROVIDER, HOST

def get_embedding_function():
    """Return an Embedding model."""
    if PROVIDER == "openai":
        return OpenAIEmbeddings()
    elif PROVIDER == "ollama":
        return OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=HOST
        )
    else:
        raise ValueError(f"Invalid provider {PROVIDER}")

def get_vector_db(persist_directory: str):
    """Load the vector DB."""
    return Chroma(persist_directory=persist_directory, embedding_function=get_embedding_function())

def get_sorted_db(persist_directory: str):
    # Fetch embeddings from Chroma
    data = get_vector_db(persist_directory).get(include=["metadatas", "documents", "embeddings"])
    metadatas = data["metadatas"]
    documents = data["documents"]
    embeddings = data["embeddings"]
    # Make sortable list
    list = [{"metadatas": metadatas[i], "documents": documents[i], "embeddings": embeddings[i]} for i in range(len(metadatas))]
    list.sort(key = lambda x : x["metadatas"]["start_percentage"])
    list.sort(key = lambda x : x["metadatas"]["source"])
    return list