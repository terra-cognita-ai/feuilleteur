from loguru import logger
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from backend.config.config import PROVIDER, HOST

VECTORS_FOLDER = 'data/vectors'

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

def get_vector_db(collection: str):
    """Load the vector DB."""
    return Chroma(persist_directory=VECTORS_FOLDER, embedding_function=get_embedding_function(), collection_name=collection)

def clear_vector_db():
    books = get_books_list()
    for book in books:
        get_vector_db(book).delete_collection()
    return

def get_sorted_db(collection: str):
    # Fetch embeddings from Chroma
    data = get_vector_db(collection).get(include=["metadatas", "documents", "embeddings"])
    metadatas = data["metadatas"]
    documents = data["documents"]
    embeddings = data["embeddings"]
    # Make sortable list
    list = [{"metadatas": metadatas[i], "documents": documents[i], "embeddings": embeddings[i]} for i in range(len(metadatas))]
    list.sort(key = lambda x : x["metadatas"]["start_percentage"] + x["metadatas"]["end_percentage"]) # sort by midpoint
    list.sort(key = lambda x : x["metadatas"]["source"]) # sort by origin (book)
    return list

def get_books_list():
    res = get_vector_db("default_collection")._client.list_collections()
    return list(filter(lambda x: x != "default_collection", list(map(lambda x : x.name, res))))

def clear_book(book_name: str):
    db = get_vector_db(book_name)
    db.delete_collection()
    return