from loguru import logger

from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from langchain.schema import AIMessage

from backend.src.types import BookImportRequest, Question, Answer, ImportedBook

from backend.src.loading import save_and_process_epub, download_and_process_epub
from backend.src.rag import answer_question
from backend.src.vectordb import get_sorted_db, clear_vector_db, get_books_list

UPLOAD_FOLDER = 'data/session'
ALLOWED_EXTENSIONS = {'epub'}

app = FastAPI()

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)) -> Response:
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No selected file")
    if "." not in file.filename or file.filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    try:
        logger.info(f"Processing EPUB for vectorization...")
        await save_and_process_epub(file)
        return {"message": f"File uploaded and processed successfully."}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/import-book")
async def import_book(book: BookImportRequest) -> Response:
    try:
        download_and_process_epub(book)
        return {"message": f"File downloaded and processed successfully."}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cover-image/{filename}")
async def serve_cover_image(filename: str) -> Response:
  return {"file": filename}

@app.post("/ask-question")
async def ask_question(question: Question) -> Answer:
    logger.info(question)
    try:
        answer, docs = answer_question(question.question, question.book, question.percentage)

        # Convert AIMessage to string if needed
        if isinstance(answer, AIMessage):
            answer_content = answer.content
        else:
            answer_content = str(answer)

        docs = [{"content": doc["content"], "position": doc["position"]} for doc in docs]
        logger.info(f"Answer:\n{answer_content}")

        return {"answer": answer_content, "documents": docs}

    except Exception as e:
        return {"error": f"An error occurred: {e}"}

@app.get("/chroma")
async def get_db(book: ImportedBook) -> Response:
    return {"chroma": get_sorted_db(book.title)}

@app.delete("/clear_db")
async def clear_db() -> Response:
    return {"cleardb": clear_vector_db()}

@app.get("/books")
async def get_books() -> list[str]:
    return get_books_list()

@app.get("/status")
async def get_status() -> Response:
    return {
        "message": "The API is up and running.",
        "status": "OK"
    }

# Serve static files from frontend build directory
app.mount("", StaticFiles(directory="frontend/build", html = True), name="frontend")