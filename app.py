from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI()  # Assumes OPENAI_API_KEY is set in environment

resume_text = """
Alanna Taylor
Stuart, Florida
(772) 626-4475
AlannaTaylor@live.com
https://www.linkedin.com/in/pivoting2tech/

Enthusiastic and results-driven professional transitioning into technology from a background in education. Completed IBM’s Applied AI Developer certification, gaining hands-on experience with Python, machine learning, REST APIs, and IBM Cloud. Currently pursuing an engineering certificate to deepen technical knowledge. Skilled in remote collaboration, data-driven decision-making, and technical troubleshooting. Eager to contribute to innovative teams solving real-world challenges through scalable, user-focused technology solutions.

Experience

DARWIN GLOBAL LLC (REMOTE)
Lead Academic Coach (June 2021 – Present)
- Leads and mentors a team of 3+ Academic Coaches in a fully remote, data-driven environment; conducted performance audits and leveraged analytics to drive team efficiency.
- Identifies and resolves systemic LMS and workflow issues, improving student support resolution times.
- Collaborates cross-functionally with stakeholders to improve learner retention and engagement.

Academic Coach (2016 – 2021)
- Supported 400+ adult learners by analyzing performance data and implementing interventions that improved course completion.
- Acted as Tier 1 tech support for platform and account issues; resolved 90% of issues without escalation.
- Maintained FERPA-compliant student records and processed over $1.5M in financial aid awards.
- Delivered career development webinars and academic coaching sessions, enhancing student outcomes.

LOGISTICS HEALTH
Administrative Intake Personnel (Per Diem) (2008 – 2016)
- Managed logistics for military healthcare events serving 300+ participants; streamlined documentation and reduced wait times by 20%.

Education

Bachelor of Science, Indian River State College - Fort Pierce, Florida
- Exceptional Student Education with Reading and ESOL Endorsement

Skills & Certifications

- IBM Applied AI Developer (IBM, 2025)
  Completed 7-course specialization with hands-on projects in Python, machine learning, REST APIs, and IBM Cloud.

- edX Verified Certificates:
  AI for Everyone, Introduction to Generative AI, Prompt Engineering, Developing Generative AI Applications with Python, Python for AI & Development Project

- Florida Educator Certification – Exceptional Student Education K–12 & ESOL (Active)

- Languages/Tools: Python, C#, Flask, IBM Cloud, Jupyter, Google Colab, Git/GitHub

- Frameworks/Platforms: REST APIs, Salesforce Lightning, LMS platforms

- Software: Microsoft Office, Google Suite, Five9 Dialer, Reporting & Analytics tools

- Soft Skills: Excellent communication & documentation, tech troubleshooting, training & coaching, remote collaboration
"""

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