import os
from loguru import logger

from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from langchain.schema import AIMessage
from werkzeug.utils import secure_filename

from backend.src.loading import load_and_process_epub, download_file
from backend.src.rag import answer_question
from backend.src.parsing import extract_cover_image
from backend.src.vectordb import get_sorted_db, clear_vector_db, get_books_list
from backend.src.types import BookImportRequest, Question, Answer, ImportedBook

UPLOAD_FOLDER = 'data/session'
VECTORS_FOLDER = 'data/vectors'
ALLOWED_EXTENSIONS = {'epub'}

app = FastAPI()

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)) -> Response:
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No selected file")

    if "." not in file.filename or file.filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    try:
        percentage = 100

        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        with open(file_path, "wb") as f:
            f.write(await file.read())

        logger.info(f"Processing EPUB for vectorization with {percentage}% of the content...")
        load_and_process_epub(file_path, percentage=percentage)

        cover_image_path = extract_cover_image(file_path, UPLOAD_FOLDER)
        return JSONResponse({"message": f"File uploaded and processed successfully ({percentage}% of the book).", 
                           "cover_image_url": f"/cover-image/{os.path.basename(cover_image_path)}" if cover_image_path else None})

    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/import-book")
async def import_book(book: BookImportRequest) -> Response:
    title = book.title
    if not title:
        raise HTTPException(status_code=400, detail="No title")
    
    url = book.formats["application/epub+zip"]
    if url:
        try:
            file_path = os.path.join(UPLOAD_FOLDER, secure_filename(title + '.epub'))
            path = download_file(url.unicode_string(), file_path)[0]
            load_and_process_epub(path)
            cover_image_path = extract_cover_image(file_path, UPLOAD_FOLDER)
            return JSONResponse({"message": f"File uploaded and processed successfully ({100}% of the book).",
                                "cover_image_url": f"/cover-image/{os.path.basename(cover_image_path)}" if cover_image_path else None})

        except Exception as e:
            logger.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail="No epub URL") 

@app.get("/cover-image/{filename}")
async def serve_cover_image(filename: str) -> Response:
  return JSONResponse({"file": filename})

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