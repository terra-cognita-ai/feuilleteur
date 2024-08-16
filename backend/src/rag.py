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

    # Adjust the RAG chain to retrieve closest documents along with generating the answer
    def rag_chain_with_retrieval(question: str):
        logger.info("Retrieving closest documents...")
        docs = retriever.get_relevant_documents(question)
        formatted_docs = format_docs(docs)

        logger.info("Generating answer...")
        context = {"context": formatted_docs, "question": question}

        # Ensure context is passed correctly to the prompt
        prompt_result = prompt.invoke(context)

        # Ensure LLM invocation is correct
        answer = llm.invoke(prompt_result)

        # Parse the final output
        parsed_answer = StrOutputParser().parse(answer)

        return parsed_answer, docs  # Return both the answer and the closest documents

    return rag_chain_with_retrieval


def answer_question(file_path: str, percentage: int, question: str, model=MODEL) -> Tuple[str, List[dict]]:
    """Process the EPUB and answer a question, returning the closest vectors used."""
    result = load_and_process_epub(file_path, percentage)
    rag_chain = build_rag_chain(result, model)

    logger.info("Running retrieving chain...")
    answer, closest_docs = rag_chain(question)  # Run the chain and get both answer and docs
    return answer, closest_docs  # Return the answer and the closest vectors (documents)