from pca import pca
from langchain_chroma import Chroma
from loguru import logger

from backend.src.vectordb import get_sorted_db

# TRY UMAP instead of PCA ?

def get_sorted_embeddings(persist_directory: str):
    list = get_sorted_db(persist_directory)
    embeddings = [x["embeddings"] for x in list]
    return embeddings

def apply_pca(persist_directory: str):
    # Apply PCA to the embeddings
    values = get_sorted_embeddings(persist_directory)
    model = pca(n_components=3)
    transformed_embeddings = model.fit_transform(values)
    logger.info(transformed_embeddings["PC"])
    return