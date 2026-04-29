import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
load_dotenv()

from rubrics import get_rubric
from evaluator import evaluate_answer

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/retrieve-rubric", methods=["POST"])
def retrieve_rubric():
    """
    Endpoint: POST /api/retrieve-rubric
    Body: { "question": "...", "subject": "auto" | "physics" | ... }
    Returns the matched rubric for a given question.
    """
    data = request.get_json()
    question = data.get("question", "").strip()
    subject = data.get("subject", "auto")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    rubric, is_match = get_rubric(question, subject)
    return jsonify({
        "rubric": rubric,
        "is_match": is_match
    })


@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    """
    Endpoint: POST /api/evaluate
    Body: { "question": "...", "answer": "...", "subject": "auto", "use_rubric": true }
    Returns: { marks_awarded, max_marks, feedback, justification, rubric_used }
    """
    data = request.get_json()
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    subject = data.get("subject", "auto")
    use_rubric = data.get("use_rubric", True)

    if not question or not answer:
        return jsonify({"error": "Both question and answer are required"}), 400

    rubric, is_match = get_rubric(question, subject)
    result = evaluate_answer(question, answer, rubric, use_rubric)
    result["rubric_used"] = rubric["name"] if use_rubric else "None (general judgment)"
    result["rubric_is_match"] = is_match

    return jsonify(result)


@app.route("/api/compare", methods=["POST"])
def compare():
    """
    Endpoint: POST /api/compare
    Body: { "question": "...", "answer": "...", "subject": "auto" }
    Returns both with-rubric and without-rubric evaluations side by side.
    """
    data = request.get_json()
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    subject = data.get("subject", "auto")

    if not question or not answer:
        return jsonify({"error": "Both question and answer are required"}), 400

    rubric, is_match = get_rubric(question, subject)

    with_rubric = evaluate_answer(question, answer, rubric, use_rubric=True)
    without_rubric = evaluate_answer(question, answer, rubric, use_rubric=False)

    return jsonify({
        "with_rubric": {**with_rubric, "rubric_used": rubric["name"]},
        "without_rubric": {**without_rubric, "rubric_used": "None (general judgment)"},
        "rubric": rubric,
        "rubric_is_match": is_match
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)