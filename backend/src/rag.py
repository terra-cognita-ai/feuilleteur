import os
from typing import Union, Tuple, List

from dotenv import load_dotenv, find_dotenv
from loguru import logger
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from backend.src.loading import EPUBPartialLoader, EPUBProcessingConfig
from backend.src.output import format_docs
from backend.config.config import MODEL
from backend.src.prompts import basis_prompt, basis_prompt_2
from pypandoc.pandoc_download import download_pandoc

# see the documentation how to customize the installation path
# but be aware that you then need to include it in the `PATH`
download_pandoc()

# Load environment variables
load_dotenv(find_dotenv())

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
                    "source": document.metadata.get("source", "unknown")
                }
            ))

    return split_documents

def vectorize_documents(splits: List[Document], persist_directory: str):
    """Vectorize the document splits and save them for later retrieval."""
    logger.info("Vectorizing documents...")
    _ = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(), persist_directory=persist_directory)

def load_vectorstore(persist_directory: str):
    """Load the vector store from the persisted directory."""
    logger.info("Loading vector store...")
    return Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())

def build_rag_chain(retriever, model=MODEL):
    """Build the RAG chain for retrieving and answering questions."""
    llm = ChatOpenAI(model=model)
    prompt = basis_prompt_2

    def rag_chain_with_retrieval(question: str):
        logger.info("Retrieving closest documents...")
        print(question)
        docs = retriever.get_relevant_documents(question)
        formatted_docs = format_docs(docs)

        logger.info("Generating answer...")
        context = {"context": formatted_docs, "question": question}

        prompt_result = prompt.invoke(context)
        answer = llm.invoke(prompt_result)
        parsed_answer = StrOutputParser().parse(answer)

        return parsed_answer, docs

    return rag_chain_with_retrieval

def answer_question(persist_directory: str, question: str, model=MODEL) -> Tuple[str, List[dict]]:
    """Answer a question using the pre-vectorized documents."""
    vectorstore = load_vectorstore(persist_directory)
    retriever = vectorstore.as_retriever()
    rag_chain = build_rag_chain(retriever, model)

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