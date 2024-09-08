from pca import pca
from langchain_chroma import Chroma
from loguru import logger

# TRY UMAP instead of PCA ?

def get_sorted_embeddings(chroma: Chroma):
    # Fetch embeddings from Chroma
    data = chroma.get(include=["embeddings", "metadatas"])
    values = data["embeddings"]
    metadatas = data["metadatas"]
    # Make sortable list
    list = [[values[i], metadatas[i]["start_percentage"]] for i in range(len(values))]
    list.sort(key = lambda x : x[1])
    values = [x[0] for x in list]
    return values

def apply_pca(chroma: Chroma):
    # Apply PCA to the embeddings
    values = get_sorted_embeddings(chroma)
    model = pca(n_components=3)
    transformed_embeddings = model.fit_transform(values)
    logger.info(transformed_embeddings["PC"])
    return values