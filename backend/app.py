from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.src.main import answer_question  # Replace with actual module name

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/', methods=['GET'])
def get_status():
    return {"message": "The API is up and running."}

@app.route('/ask-question', methods=['POST'])
def ask_question():
    data = request.json
    file_path = data.get('file_path', '../data/dumas_monte_cristo_1.epub')
    percentage = data.get('percentage', 10)  # Default to 10% if not provided
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        answer = answer_question(file_path, percentage, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8890, debug=True)