from pydantic import BaseModel, Field, FilePath, FileUrl, HttpUrl, model_validator
from pydantic.functional_validators import AfterValidator
from typing_extensions import TypedDict
from typing import Optional
import uuid

class Person(BaseModel):
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

BookFormats = TypedDict("BookFormats",{
    "application/epub+zip": str,
    "image/jpeg": str
})

class BookMetadataBase(BaseModel):
    title: str

class GutenbergBook(BookMetadataBase):
    id: int
    formats: BookFormats
    authors: list[Person] = []
    translators: list[Person] = []
    languages: list[str] = []
    subjects: list[str] = []
    
class BookMetadata(BookMetadataBase):
    uuid: str
    authors: str
    translators: str
    languages: str
    cover_url: str = ""

class BookReference(BaseModel):
    uuid: str

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
