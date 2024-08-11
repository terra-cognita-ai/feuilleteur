import os
import sys
import argparse

from dotenv import load_dotenv, find_dotenv
from loguru import logger
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import nltk

from src.loading import EPUBPartialLoader, EPUBProcessingConfig
from src.output import format_docs
from config.config import MODEL

# Load environment variables
load_dotenv(find_dotenv())

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Process an EPUB file and ask questions without spoilers.")
    parser.add_argument(
        '--percentage',
        type=int,
        default=10,
        help="Percentage of the book to process (default: 10%)"
    )
    parser.add_argument(
        '--question',
        type=str,
        required=True,
        help="The question you want to ask about the book"
    )
    args = parser.parse_args()

    logger.info("Loading document...")
    config = EPUBProcessingConfig(
        file_path="../data/dumas_monte_cristo_1.epub",
        percentage=args.percentage
    )
    # Create an instance of the custom chain
    epub_chain = EPUBPartialLoader(config)

    # Run the chain
    result = epub_chain({"input": None})

    # Print the selected text
    logger.info(f"Selected Text (up to {config.percentage}% of the content):")

    llm = ChatOpenAI(model=MODEL)

    logger.info("Splitting document...")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    splits = text_splitter.split_documents(result)

    logger.info("Populating vector store...")

    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Retrieve and generate using the relevant snippets of the book.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    logger.info("Building retrieving chain...")

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    logger.info("Running retrieving chain...")
    answer = rag_chain.invoke(args.question)

    logger.info(f"Answer:\n{answer}")

if __name__ == "__main__":
    main()