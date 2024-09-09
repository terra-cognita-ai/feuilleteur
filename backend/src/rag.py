import os
from typing import Union, Tuple, List

from dotenv import load_dotenv, find_dotenv
from loguru import logger
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from backend.src.loading import EPUBPartialLoader, EPUBProcessingConfig
from backend.src.output import format_docs
from backend.config.config import MODEL
from backend.config.config import PROVIDER
from backend.config.config import HOST
from backend.src.prompts import basis_prompt, basis_prompt_2
from backend.src.vectordb import get_vector_db
from pypandoc.pandoc_download import download_pandoc

# see the documentation how to customize the installation path
# but be aware that you then need to include it in the `PATH`
download_pandoc()

# Load environment variables
load_dotenv(find_dotenv())

def get_llm():
    """Return an LLM."""
    if PROVIDER == "openai":
        return ChatOpenAI(
            model=MODEL
        )
    elif PROVIDER == "ollama":
        return ChatOllama(
            model=MODEL,
            base_url=HOST
        )
    else:
        raise ValueError(f"Invalid provider {PROVIDER}")

def load_and_process_epub(file_path: Union[str, bytes, os.PathLike], percentage: int):
    """Load and process the EPUB file."""
    logger.info("Loading document...")
    config = EPUBProcessingConfig(
        file_path=file_path,
        percentage=percentage
    )
    epub_chain = EPUBPartialLoader(config)
    result = epub_chain({"input": None})

    logger.info(f"Selected Text (up to {config.percentage}% of the content):")
    return result

def split_documents_with_positions(documents, chunk_size=2000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    total_length = sum([len(doc.page_content) for doc in documents])
    split_documents = []
    current_position = 0
    for document in documents:
        splits = splitter.split_text(document.page_content)
        for i, split in enumerate(splits):
            start_position = current_position
            end_position = start_position + len(split)
            percentage_start = (start_position / total_length) * 100
            percentage_end = (end_position / total_length) * 100

            current_position += len(split) if i == 0 else (chunk_size - chunk_overlap)
            split_documents.append(Document(
                page_content=split,
                metadata={
                    "start_percentage": percentage_start,
                    "end_percentage": percentage_end,
                    "source": document.metadata.get("source_doc_0", "unknown")
                }
            ))

    return split_documents

def vectorize_documents(splits: List[Document], persist_directory: str):
    """Vectorize the document splits and save them for later retrieval."""
    logger.info("Vectorizing documents...")
    get_vector_db(persist_directory).add_documents(splits)

def build_rag_chain(retriever, source: str):
    """Build the RAG chain for retrieving and answering questions."""
    llm = get_llm()
    prompt = basis_prompt_2

    def rag_chain_with_retrieval(question: str):
        logger.info("Retrieving closest documents...")
        print(question)
        docs = retriever.get_relevant_documents(question, metadata = {"source": source})
        formatted_docs = format_docs(docs)

        logger.info("Generating answer...")
        context = {"context": formatted_docs, "question": question}

        prompt_result = prompt.invoke(context)
        answer = llm.invoke(prompt_result)
        parsed_answer = StrOutputParser().parse(answer)

        return parsed_answer, docs

    return rag_chain_with_retrieval

def answer_question(persist_directory: str, question: str, source: str) -> Tuple[str, List[dict]]:
    """Answer a question using the pre-vectorized documents."""
    vectorstore = get_vector_db(persist_directory)
    retriever = vectorstore.as_retriever()
    rag_chain = build_rag_chain(retriever, source)

    logger.info("Running retrieving chain...")
    answer, closest_docs = rag_chain(question)

    closest_docs_with_positions = []
    for doc in closest_docs:
        metadata = doc.metadata
        position_info = f"{metadata['start_percentage']:.2f}% - {metadata['end_percentage']:.2f}%"
        closest_docs_with_positions.append({
            "content": doc.page_content,
            "position": position_info,
            "source": metadata.get("source", "unknown")
        })

    return answer, closest_docs_with_positions