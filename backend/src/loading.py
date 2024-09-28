from typing import List
from loguru import logger
from pydantic import BaseModel, Field
from langchain_core.documents.base import Document
from langchain_unstructured import UnstructuredLoader
from langchain_community.document_loaders.epub import UnstructuredEPubLoader
from typing import Union
from backend.src.rag import split_documents_with_positions
from backend.src.vectordb import vectorize_documents
from backend.src.parsing import extract_cover_image
from backend.src.types import GutenbergBook, BookMetadata
from urllib.request import urlretrieve
from werkzeug.utils import secure_filename
from fastapi import UploadFile
import os, uuid

UPLOAD_FOLDER = 'data/session'

def generate_unique_id(book: BookMetadata):
    authors = list(map(lambda a : a.name, book.authors))
    translators = list(map(lambda t : t.name, book.translators))
    unique_string = " ".join([book.title] + authors + translators + book.languages).lower()
    unique_string = ''.join(letter for letter in unique_string if letter.isalnum())
    logger.info(unique_string)
    return uuid.uuid5(uuid.NAMESPACE_OID, unique_string).hex

def make_book_metadata(book: GutenbergBook) -> BookMetadata:
    return BookMetadata(
        title = book.title,
        uuid = generate_unique_id(book), 
        authors = "&".join([author.name for author in book.authors]), 
        translators =  "&".join([translator.name for translator in book.translators]),
        languages =  "&".join([language for language in book.languages]),
        cover_url = book.formats["image/jpeg"]
    )

def download_file(url: str, file_path: str):
    return urlretrieve(url, file_path)

def download_and_process_epub(book: GutenbergBook):
    """Download and process the EPUB file."""
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(book.title + ".epub"))
    url = book.formats["application/epub+zip"]
    logger.info("Downloading EPUB from URL: {}".format(url))
    path, _ = download_file(url, file_path)
    book_metadata = make_book_metadata(book)
    logger.info(book_metadata)
    return load_and_process_epub(path, book_metadata)

async def save_and_process_epub(file: UploadFile):
    """Save and process the EPUB file."""
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    with open(file_path, "wb") as f:
        f.write(await file.read())
    cover_url = extract_cover_image(file_path).replace("data/session/" , "cover/")
    book = GutenbergBook(title= secure_filename(file.filename.replace(".epub", "")), id = 0, formats={"image/jpeg": cover_url, "application/epub+zip": file_path})
    return load_and_process_epub(file_path, make_book_metadata(book))

def load_and_process_epub(file_path: Union[str, bytes, os.PathLike], book: BookMetadata):
    """Load and process the EPUB file."""
    logger.info("Loading document...")
    config = EPUBProcessingConfig(
        file_path=file_path,
        percentage=100
    )
    epub_chain = EPUBPartialLoader(config)
    result = epub_chain({"input": None})

    logger.info(f"Selected Text (up to {config.percentage}% of the content):")

    splits = split_documents_with_positions(result)
    vectorize_documents(splits, book)
    return result

class EPUBProcessingConfig(BaseModel):
    file_path: str
    percentage: int

    class Config:
        extra = "forbid"


class EPUBPartialLoader(UnstructuredLoader):
    config: EPUBProcessingConfig = Field(description="Config to select the partial loader parameters")

    def __init__(self, config: EPUBProcessingConfig):
        self.config = config

        # Define the step function here
        def load_and_process_epub():
            logger.info("Loading EPUB...")
            text_content = self.load_epub()  # Call instance method to load EPUB
            selected_text = self.get_text_up_to_percentage(text_content)  # Call instance method to get text
            return {"content": selected_text}

        # Initialize the SimpleSequentialChain with the steps
        super().__init__(chains=[load_and_process_epub])

    def load_epub(self):
        loader = UnstructuredEPubLoader(self.config.file_path, strategy="fast")
        documents = loader.load()
        return documents

    @staticmethod
    def merge_documents_data(documents: List[Document]):
        full_text = '\n'.join(doc.page_content for doc in documents)
        full_metadata = [{f"{mtd_key}_doc_{i}": mtd_value
                          for (mtd_key, mtd_value) in doc.metadata.items()}
                         for i, doc in enumerate(documents)]
        # Convert the list of dictionaries to a single dict
        full_metadata = {k: v for d in full_metadata for k, v in d.items()}
        return full_text, full_metadata

    @staticmethod
    def create_final_documents(text, metadata):
        full_document = Document(page_content=text,
                                 metadata=metadata)
        return full_document

    def get_text_up_to_percentage(self, text):
        total_length = len(text)
        cut_off_index = int(total_length * (self.config.percentage / 100.0))
        return text[:cut_off_index]

    def __call__(self, inputs) -> List[Document]:
        documents = self.load_epub()
        full_text, full_sources = self.merge_documents_data(documents)
        selected_text = self.get_text_up_to_percentage(full_text)
        final_document = self.create_final_documents(selected_text, full_sources)
        return [final_document]

    @property
    def input_keys(self):
        return []

    @property
    def output_keys(self):
        return ["content"]