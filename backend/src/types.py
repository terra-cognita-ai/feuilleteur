from pydantic import BaseModel, Field, FilePath, FileUrl
from typing_extensions import TypedDict
from typing import Optional
import uuid

UUID = uuid.UUID

class Person(BaseModel):
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

BookFormats = TypedDict("BookFormats",{
    "application/epub+zip": FileUrl,
    "image/jpeg": FileUrl
})

class BookImportRequest(BaseModel):
    title: str
    formats: BookFormats
    authors: list[Person] = []
    translators: list[Person] = []
    languages: list[str] = []
    subjects: Optional[list[str]] = None
    gutenberg_id: Optional[int] = None
    
class BookMetadata(BookImportRequest):
    epub_path: Optional[FilePath] = None
    cover_path: Optional[FilePath] = None

class ImportedBook(BookMetadata):
    uuid: Optional[UUID] = None

class Question(BaseModel):
    question: str
    book: str
    percentage: int = 100

class Document(BaseModel):
    content: str
    position: str        

class Answer(BaseModel):
    answer: str
    documents: list[Document]
