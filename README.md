# Mini Answer Evaluator

AI-Powered Rubric-Based Evaluation System using Groq (Llama 3)

---

## Overview

Mini Answer Evaluator is an AI-driven system that automatically evaluates student answers using structured rubrics and LLM intelligence.

Given a question, student answer, and subject-specific rubric, the system generates:

* Marks (out of maximum)
* Constructive feedback
* Justification based on rubric criteria

It also features a Compare Mode, demonstrating how rubric-based evaluation improves grading consistency over generic evaluation.

---

## Demo Walkthrough

The system uses rubric-aware LLM evaluation to ensure consistent and explainable grading.

---

### Step 1: Input Question and Answer

User provides a question and student response.

![Main UI](./assets/UI.png)

---

### Step 2: Evaluation Output

The system generates marks, feedback, and justification.

![Evaluation Result](./assets/Result.png)

---

### Step 3: Compare Mode

Shows the difference between rubric-based and general evaluation.

![Compare Mode](./assets/Compare.png)

---

## Demo Output

### Input

Question: Define Newton’s Second Law of Motion
Answer: Force is equal to mass times acceleration

---

### Output

```json id="o1i9nw"
{
  "marks": 4,
  "feedback": "The answer correctly explains the concept but lacks clarity in defining variables.",
  "justification": "Concept is correct, but explanation is incomplete."
}
```

---

## Deployment

The project follows a decoupled architecture, with frontend and backend deployed separately.

---

## Live Demo

Frontend (Vercel):
https://mini-answer-evaluator.vercel.app

Backend API (Render):
https://mini-answer-evaluator.onrender.com

Note: The backend is hosted on a free tier and may take 30–50 seconds to respond after inactivity.

---

## Deployment Configuration

### Backend (Render)

* Environment: Python 3
* Root Directory: backend
* Build Command:

  ```bash
  pip install -r requirements.txt
  ```
* Start Command:

  ```bash
  gunicorn app:app
  ```
* Environment Variable: GROQ_API_KEY

---

### Frontend (Vercel)

* Framework: Static HTML, CSS, JavaScript
* Root Directory: frontend
* API Integration: app.js points to the Render backend
* Deployment: Automatic deployment via GitHub

---

## Project Structure

```id="0sfbkg"
mini-answer-evaluator/
├── backend/
│   ├── app.py
│   ├── rubrics.py
│   ├── evaluator.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│
├── assets/
│   ├── ui.png
│   ├── result.png
│   └── compare.png
│
└── README.md
```

---

## Setup and Running

### 1. Clone Repository

```bash id="yifph6"
git clone https://github.com/Sachinyadav313/mini-answer-evaluator.git
cd mini-answer-evaluator
```

---

### 2. Backend Setup

```bash id="czcfn5"
cd backend
python -m venv venv
```

Activate environment:

Linux/Mac:

```bash id="6fdl7k"
source venv/bin/activate
```

Windows:

```bash id="5y1qdn"
venv\Scripts\activate
```

Install dependencies:

```bash id="f9mqh4"
pip install -r requirements.txt
```

Setup environment variables:

```bash id="brzeyr"
cp .env.example .env
```

Add API key:

```bash id="j21r5h"
GROQ_API_KEY=your_api_key_here
```

Run backend:

```bash id="tkgptj"
python app.py
```

---

### 3. Frontend

Open in browser:

```id="r4lpld"
frontend/index.html
```

Ensure backend is running before using the application.

---

## API Endpoints

| Method | Endpoint             | Description        |
| ------ | -------------------- | ------------------ |
| POST   | /api/retrieve-rubric | Retrieve rubric    |
| POST   | /api/evaluate        | Evaluate answer    |
| POST   | /api/compare         | Compare evaluation |

---

## System Design

### Rubric Retrieval

* Keyword frequency matching
* Selects best rubric
* Fallback if no match

Supported subjects: Physics, Mathematics, Chemistry, English, Biology, History

---

### Prompt Strategy

With Rubric:

* Criteria-based scoring
* Justification included

Without Rubric:

* General evaluation
* Based on clarity and accuracy

---

### Structured Output

* JSON-based response
* Uses Groq structured output
* Eliminates parsing issues

---

## Rubric Format

```json id="4yaz95"
{
  "name": "Physics",
  "keywords": ["force", "motion"],
  "max_marks": 5,
  "criteria": ["Definition", "Formula"]
}
```

---

## Future Improvements

* Embedding-based retrieval
* Per-criterion scoring
* Rubric editor UI
* Database integration (SQLite)
* Batch evaluation

---

## Tech Stack

Backend: Python, Flask
LLM: Groq API (Llama 3.3 70B)
Frontend: HTML, CSS, JavaScript
Retrieval: Keyword matching

---

## Environment Variables

```id="3nt1wk"
GROQ_API_KEY=your_api_key
```

---

## Why This Project Stands Out

* Combines LLM with structured rubrics
* Produces explainable outputs
* Clean modular architecture
* Real-world application in education

---

## Final Note

This project demonstrates how combining simple retrieval systems with powerful LLMs can create scalable, explainable, and production-ready AI solutions.

---
