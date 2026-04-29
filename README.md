🎓 Mini Answer Evaluator

A rubric-based student answer evaluation system powered by Groq (Llama 3). Built as part of the Evalvia project.

---

🚀 Overview

Mini Answer Evaluator is designed to automatically assess student responses using structured rubrics. Given a question, a student answer, and a subject-specific rubric, the system evaluates performance and provides meaningful insights.

It returns:
• Marks awarded (out of maximum marks)
• Constructive feedback (student-friendly)
• Clear justification (based on rubric criteria)

It also includes a Compare Mode, which evaluates answers both with and without rubrics to highlight the importance of structured grading.

---

📂 Project Structure

mini-answer-evaluator/

backend/
• app.py → Flask API server (3 endpoints)
• rubrics.py → Rubric definitions + keyword-based retrieval
• evaluator.py → Groq API integration + prompt engineering
• requirements.txt
• .env.example

frontend/
• index.html → Main UI
• static/
 • css/style.css
 • js/app.js → API calls + rendering

README.md

---

⚙️ Setup & Running

1. Clone the Repository

git clone https://github.com/Sachinyadav313/mini-answer-evaluator.git
cd mini-answer-evaluator

---

2. Backend Setup

cd backend
python -m venv venv

Activate environment:
Linux/Mac: source venv/bin/activate
Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Setup environment variables:
cp .env.example .env
(Add your Groq API key)

Run server:
python app.py

Backend runs at: http://localhost:5000

---

3. Frontend

Simply open:
frontend/index.html

Note: Ensure backend is running before evaluation.

---

🌐 API Endpoints

POST /api/retrieve-rubric
→ Returns matched rubric based on question

POST /api/evaluate
→ Evaluates answer (with or without rubric)

POST /api/compare
→ Returns both evaluations side-by-side

---

🧠 System Design

Rubric Retrieval
• Uses keyword frequency matching
• Counts keyword occurrences per rubric
• Selects highest matching rubric
• Falls back to general rubric if no match

Subjects supported:
Physics, Mathematics, Chemistry, English, Biology, History + Fallback

---

Prompt Strategy

Two evaluation modes:

1. With Rubric
   • Explicit criteria passed to LLM
   • Marks awarded per criterion
   • Detailed reasoning included

2. Without Rubric
   • General academic evaluation
   • Based on accuracy, clarity, completeness
   • Scored out of 5

System Prompt:
"You are an expert academic evaluator. Evaluate answers fairly and return ONLY valid JSON."

---

Structured Output

• Uses Groq structured JSON response
• response_format = { "type": "json_object" }
• Eliminates parsing issues
• Ensures reliable backend processing

---

📋 Rubric Format

Example:

{
"name": "Physics (Class 12)",
"keywords": ["force", "motion", "newton", "energy"],
"max_marks": 5,
"criteria": [
"Correct definition or concept (1 mark)",
"Accurate formula with symbols (1 mark)"
]
}

To add a new subject → update RUBRICS in rubrics.py

---

🔮 Future Improvements

• Regex-based word matching (avoid false positives)
• Embedding-based semantic retrieval
• Per-criterion scoring (more granular evaluation)
• Rubric editor UI for teachers
• Answer history with database (SQLite)
• Batch evaluation via CSV upload

---

💻 Tech Stack

Backend → Python 3.12, Flask, python-dotenv
LLM → Groq API (llama-3.3-70b-versatile)
Frontend → HTML, CSS, JavaScript (Vanilla)
Rubric Retrieval → Keyword frequency matching

---

🔐 Environment Variables

GROQ_API_KEY → Your Groq API key

---

✨ Why This Project Stands Out

• Combines LLM evaluation with structured rubrics
• Demonstrates practical AI in education
• Clean architecture (separate retrieval + evaluation layers)
• Built for extensibility and real-world use

---

📌 Final Note

This project showcases how combining simple retrieval techniques with powerful LLMs can create reliable, explainable, and scalable evaluation systems.

---
