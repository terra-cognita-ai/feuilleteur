import os

from loguru import logger
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from langchain.schema import AIMessage
from urllib.request import urlretrieve

from werkzeug.utils import secure_filename
from backend.src.rag import load_and_process_epub, split_documents_with_positions, vectorize_documents, answer_question
from backend.src.vectordb import get_sorted_db, get_books_list, clear_vector_db
from backend.src.parsing import extract_cover_image

UPLOAD_FOLDER = 'data/session'
VECTORS_FOLDER = 'data/vectors'
UPLOADED_FILE_NAME = 'uploaded_book.epub'
ALLOWED_EXTENSIONS = {'epub'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['VECTORS_FOLDER'] = VECTORS_FOLDER
CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', defaults=dict(filename=None))
@app.route('/<path:filename>', methods=['GET', 'POST'])
def index(filename):
    filename = filename or 'index.html'
    if request.method == 'GET':
        return send_from_directory('../frontend/build', filename)

    return jsonify(request.data)

@app.route('/status', methods=['GET'])
def get_status():
    return {
        "message": "The API is up and running.",
        "status": "OK"
    }

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Get the percentage from the request
        percentage = int(request.form.get('percentage', 100))

        # Process and vectorize the EPUB file
        logger.info(f"Processing EPUB for vectorization with {percentage}% of the content...")
        result = load_and_process_epub(file_path, percentage=percentage)
        splits = split_documents_with_positions(result)
        vectorize_documents(splits)

        # Extract cover image
        cover_image_path = extract_cover_image(file_path, app.config['UPLOAD_FOLDER'])
        if cover_image_path:
            cover_image_url = f"/cover-image/{os.path.basename(cover_image_path)}"
        else:
            cover_image_url = None

        return jsonify({"message": f"File uploaded and processed successfully ({percentage}% of the book).", "cover_image_url": cover_image_url}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400
    
@app.route('/import-book', methods=['POST'])
def import_book():
    logger.info(request.json)

    title = request.json.get('title', '')
    formats = request.json.get('formats', [])
    url = formats['application/epub+zip']
    
    if not title:
        return jsonify({"error": "No title"}), 400
    
    if url:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(title + '.epub'))
        file = urlretrieve(url, file_path)
        percentage = int(request.form.get('percentage', 100))

        # Process and vectorize the EPUB file
        logger.info(f"Processing EPUB for vectorization with {percentage}% of the content...")
        result = load_and_process_epub(file[0], percentage=percentage)
        splits = split_documents_with_positions(result)
        vectorize_documents(splits)

        # Extract cover image
        cover_image_path = extract_cover_image(file[0], app.config['UPLOAD_FOLDER'])
        if cover_image_path:
            cover_image_url = f"/cover-image/{os.path.basename(cover_image_path)}"
        else:
            cover_image_url = None

        return jsonify({"message": f"File uploaded and processed successfully ({percentage}% of the book).", "cover_image_url": cover_image_url}), 200
    else:
        return jsonify({"error": "No epub URL"}), 400

@app.route('/cover-image/<filename>', methods=['GET'])
def serve_cover_image(filename):
    return send_from_directory("../data/session", filename)

@app.route('/ask-question', methods=['POST'])
def ask_question():
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], UPLOADED_FILE_NAME)):
        return jsonify({"error": "No file uploaded yet."}), 400

    question = request.json.get('question', '')
    book = request.json.get('book', '')
    percentage = int(request.json.get('percentage', ''))

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        answer, docs = answer_question(question, book, percentage)

        # Convert AIMessage to string if needed
        if isinstance(answer, AIMessage):
            answer_content = answer.content
        else:
            answer_content = str(answer)

        docs = [{"content": doc["content"], "position": doc["position"]} for doc in docs]

        logger.info(f"Answer:\n{answer_content}")

        return jsonify({"answer": answer_content, "documents": docs, "status": "ok"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/chroma', methods=['GET'])
def get_db():
    book = request.json.get('book', '')
    return {"chroma": get_sorted_db(book)}

@app.route('/cleardb', methods=['GET'])
def clear_db():
    return {"cleardb": clear_vector_db()}

@app.route('/books', methods=['GET'])
def get_books():
    return {"books": get_books_list()}

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(VECTORS_FOLDER):
        os.makedirs(VECTORS_FOLDER)
    app.run(host='0.0.0.0', port=8890, debug=True)