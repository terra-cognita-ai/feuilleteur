import os

from loguru import logger
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from werkzeug.utils import secure_filename
from backend.src.rag import answer_question  # Replace with actual module name
from backend.src.parsing import extract_cover_image  # Import the parsing utility

UPLOAD_FOLDER = 'data/session'
UPLOADED_FILE_NAME = 'uploaded_book.epub'
ALLOWED_EXTENSIONS = {'epub'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)  # This will enable CORS for all routes


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def get_status():
    return {"message": "The API is up and running."}


@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(UPLOADED_FILE_NAME)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract cover image
        cover_image_path = extract_cover_image(file_path, app.config['UPLOAD_FOLDER'])
        print(cover_image_path)
        if cover_image_path:
            cover_image_url = f"/cover-image/{os.path.basename(cover_image_path)}"
        else:
            cover_image_url = None

        return jsonify({"message": "File uploaded successfully.", "cover_image_url": cover_image_url}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400


@app.route('/cover-image/<filename>', methods=['GET'])
def serve_cover_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/ask-question', methods=['POST'])
def ask_question():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], UPLOADED_FILE_NAME)

    if not os.path.exists(file_path):
        return jsonify({"error": "No file uploaded yet."}), 400

    percentage = int(request.json.get('percentage', 10))
    question = request.json.get('question', '')

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        answer, docs = answer_question(file_path, percentage, question)
        docs = [doc.page_content for doc in docs]

        logger.info(f"Answer:\n{answer.content}")

        return jsonify({"answer": answer.content,
                        "documents": docs})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=8890, debug=True)