from typing import Union, Tuple, List

from dotenv import load_dotenv, find_dotenv
from loguru import logger
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from backend.src.output import format_docs
from backend.config.config import MODEL
from backend.config.config import PROVIDER
from backend.config.config import HOST
from backend.src.prompts import basis_prompt, basis_prompt_2
from backend.src.vectordb import get_vector_db

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
            percentage_mid = (percentage_end + percentage_start) / 2

            current_position += len(split) if i == 0 else (chunk_size - chunk_overlap)
            split_documents.append(Document(
                page_content=split,
                metadata={
                    "start_percentage": percentage_start,
                    "mid_percentage": percentage_mid,
                    "end_percentage": percentage_end,
                    "source": document.metadata.get("source_doc_0", "unknown")
                }
            ))

    return split_documents

def build_rag_chain(source: str, percentage: int):
    """Build the RAG chain for retrieving and answering questions."""
    llm = get_llm()
    prompt = basis_prompt_2
    vectorstore = get_vector_db(source)
    retriever = vectorstore.as_retriever(search_kwargs={"filter":{"end_percentage": {"$lt": percentage}}})

    def rag_chain_with_retrieval(question: str):
        logger.info("Retrieving closest documents...")
        logger.info(source)
        print(question)
        docs = retriever.get_relevant_documents(question)
        # docs = retriever.invoke(question)
        formatted_docs = format_docs(docs)

        logger.info("Generating answer...")
        context = {"context": formatted_docs, "question": question}

        prompt_result = prompt.invoke(context)
        answer = llm.invoke(prompt_result)
        parsed_answer = StrOutputParser().parse(answer)

        return parsed_answer, docs

    return rag_chain_with_retrieval

def answer_question(question: str, source: str, percentage: int) -> Tuple[str, List[dict]]:
    """Answer a question using the pre-vectorized documents."""
    rag_chain = build_rag_chain(source, percentage)

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