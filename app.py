from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

resume_text = """
Stuart, Florida  
Alanna Taylor  
(772) 626-4475  
AlannaTaylor@live.com  
https://alannataylor18.github.io/About_Me/  
https://www.linkedin.com/in/pivoting2tech/

Enthusiastic and results-driven professional transitioning into technology from a background in education. Completed IBM’s Applied AI Developer certification with hands-on experience in Python, machine learning, REST APIs, and IBM Cloud. Currently pursuing an engineering certificate to deepen technical expertise. Demonstrated success in data analysis, workflow optimization, LMS management, Excel-based reporting, and technical troubleshooting in a fully remote environment. Eager to contribute to innovative teams solving real-world challenges with scalable, user-focused solutions.

Experience  
DARWIN GLOBAL LLC (REMOTE)  
Lead Academic Coach — JUNE 2021 - PRESENT  
● Manage and mentor a remote team of Academic Coaches using real-time performance dashboards and KPIs.  
● Perform data extraction and analysis from LMS to generate weekly performance and engagement reports using Excel (PivotTables, formulas).  
● Troubleshoot and resolve LMS and workflow system issues; often serve as liaison with IT for backend fixes.  
● Built custom workflows to streamline academic intervention processes, reducing student resolution time by 30%.  
● Collaborate cross-functionally with stakeholders (Product, IT, Student Services) to enhance platform functionality and data integrity.

Academic Coach — 2016-2021  
● Supported 400+ adult learners by analyzing performance data and implementing interventions that improved course completion.  
● Acted as Tier 1 tech support for platform and account issues; resolved 90% of issues without escalation.  
● Maintained accurate student records in alignment with accreditation/FERPA standards, ensuring data integrity and accountability.  
● Maintained FERPA-compliant student records and processed over $1.5M in financial aid awards.  
● Delivered career development webinars and academic coaching sessions, enhancing student outcomes.

LOGISTICS HEALTH  
Administrative Intake Personnel (PER DIEM) — 2008-2016  
● Managed logistics for military healthcare events serving 300+ participants; streamlined documentation and reduced wait times by 20%.

Education  
Bachelor of Science, Indian River State College - Fort Pierce, Florida  
Exceptional Student Education with Reading and ESOL Endorsement

Skills & Certifications  
● IBM Applied AI Developer (IBM, 2025)  
Completed 7-course specialization with hands-on projects in Python, machine learning, REST APIs, and IBM Cloud.  
edX Verified Certificates: AI for Everyone, Introduction to Generative AI, Prompt Engineering, Developing Generative AI Applications with Python, Python for AI & Development Project

● Programming & Tools: Python, Jupyter Notebooks, IBM Watson, REST APIs, Git/GitHub, VS Code, JSON  
● Cloud & AI Platforms: IBM Cloud, Watson NLP, Watson Assistant, Watson Studios  
● Software: Microsoft Office, Google Suite, Five9 Dialer, Reporting & Analytics tools  
● Data & Troubleshooting: Data analytics, LMS systems, FERPA compliance, ticketing systems  
● Other Tools: Excel, Google Workspace, Microsoft Teams, Zoom, Canvas LMS, Blackboard, Salesforce  
● Soft Skills: Excellent communication & documentation, tech troubleshooting, training & coaching, remote collaboration
"""

@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running. POST to /chat with a question."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("message", "").strip()

        if not question:
            return jsonify({"reply": "Please enter a question."}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant helping answer questions about Alanna Taylor based on her resume. "
                        "Respond in a friendly, conversational tone. Only use information from the resume. If the question is off-topic, say so politely."
                    )
                },
                {
                    "role": "user",
                    "content": f"This is Alanna Taylor's resume:\n{resume_text}"
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        reply = response.choices[0].message["content"].strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))