import os
from typing import Union

from dotenv import load_dotenv, find_dotenv
from loguru import logger
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.src.loading import EPUBPartialLoader, EPUBProcessingConfig
from backend.src.output import format_docs
from backend.config.config import MODEL

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


def build_rag_chain(result, model=MODEL):
    """Build the RAG chain for retrieving and answering questions."""
    llm = ChatOpenAI(model=model)

    logger.info("Splitting document...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    splits = text_splitter.split_documents(result)

    logger.info("Populating vector store...")
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    logger.info("Building retrieving chain...")
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    return rag_chain


def answer_question(file_path: str, percentage: int, question: str, model=MODEL) -> str:
    """Process the EPUB and answer a question."""
    result = load_and_process_epub(file_path, percentage)
    rag_chain = build_rag_chain(result, model)

    logger.info("Running retrieving chain...")
    answer = rag_chain.invoke(question)

    return answer

