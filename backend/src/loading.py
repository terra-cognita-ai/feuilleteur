from typing import List
from loguru import logger
from pydantic import BaseModel, Field
from langchain_core.documents.base import Document
from langchain_unstructured import UnstructuredLoader
from langchain_community.document_loaders.epub import UnstructuredEPubLoader

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