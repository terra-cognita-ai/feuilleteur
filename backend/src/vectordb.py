from loguru import logger
from typing import List
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document
from backend.config.config import PROVIDER, HOST
from backend.src.types import BookMetadata
import uuid, json

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

def vectorize_documents(splits: List[Document], book: BookMetadata):
    """Vectorize the document splits and save them for later retrieval."""
    logger.info("Vectorizing documents...")
    clear_book(book)
    return Chroma(persist_directory=VECTORS_FOLDER, 
                  embedding_function=get_embedding_function(), 
                  collection_name=book.uuid, collection_metadata=book.__dict__).add_documents(splits)

def get_vector_db(collection : str) -> Chroma:
    """Load the vector DB."""
    return Chroma(persist_directory=VECTORS_FOLDER, embedding_function=get_embedding_function(), collection_name=collection)

def get_book(book: BookMetadata) -> Chroma:
    """Load the vector DB."""
    return Chroma(persist_directory=VECTORS_FOLDER, embedding_function=get_embedding_function(), collection_name=book.uuid)

def clear_book(book: BookMetadata):
    db = get_vector_db(book.uuid)
    db.delete_collection()
    return

def clear_vector_db():
    collections = get_vector_db("default_collection")._client.list_collections()
    for collection in collections:
        get_vector_db(collection.name).delete_collection()
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

def get_books_list() -> list[BookMetadata]:
    res = get_vector_db("default_collection")._client.list_collections()
    res = list(filter(lambda x: x.metadata, res))
    return list(map(lambda x : x.metadata, res))
