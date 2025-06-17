from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import requests
import pdfplumber
from io import BytesIO
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI()  # Uses OPENAI_API_KEY from environment variables automatically

RESUME_URL = "https://alannataylor18.github.io/About_Me/files/RESUME_Taylor%20Alanna%202025_Tech.pdf"

def fetch_resume_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        with pdfplumber.open(BytesIO(response.content)) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error fetching or parsing resume PDF: {e}")
        return None

resume_text = fetch_resume_text(RESUME_URL) or "Resume could not be loaded."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("message", "").strip()

        if not question:
            return jsonify({"reply": "Please enter a question."}), 400

        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if any(re.fullmatch(rf"\b{g}\b", question.lower()) for g in greetings):
            return jsonify({"reply": "Hello! Feel free to ask me questions about Alanna Taylor's resume."})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that answers questions about Alanna Taylor using her resume. "
                        "Here is her resume:\n\n"
                        f"{resume_text}\n\n"
                        "Only answer questions using the information in this resume. "
                        "If the question is not relevant, respond politely."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))