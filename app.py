from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Load the QA pipeline once on startup
qa_pipeline = pipeline("question-answering", model="deepset/tinyroberta-squad2")

@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running. POST to /chat with a question."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("message")
        if not question:
            return jsonify({"reply": "Please enter a question."}), 400

        # Default resume-like context
        context = (
            "Alanna Taylor is a tech-savvy professional skilled in Python, "
            "web development, and machine learning. She has experience with "
            "Flask, IBM Watson APIs, and GitHub Pages."
        )

        result = qa_pipeline(question=question, context=context)
        return jsonify({"reply": result.get("answer", "No answer found.")})

    except Exception as e:
        return jsonify({"reply": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)