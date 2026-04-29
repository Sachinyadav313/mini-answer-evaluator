import os
import json
from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
SYSTEM_PROMPT = """You are an expert academic evaluator for school and college exams. \
Evaluate student answers fairly and constructively based on the provided rubric. \
Return ONLY a valid JSON object."""

# MANDATORY: Fallback rubric for unexpected subjects or missing rubrics
FALLBACK_RUBRIC = {
    "name": "General Evaluation Fallback",
    "max_marks": 5,
    "criteria": [
        "Relevance to the question",
        "Coverage of key points",
        "Clarity of explanation",
        "Logical structure",
        "Language quality"
    ]
}

def build_prompt(question: str, answer: str, rubric: dict, use_rubric: bool) -> str:
    if use_rubric:
        criteria_text = "\n".join(
            f"{i+1}. {c}" for i, c in enumerate(rubric["criteria"])
        )
        return f"""Evaluate the following student answer using the rubric provided.

QUESTION:
{question}

STUDENT ANSWER:
{answer}

RUBRIC — {rubric['name']} (out of {rubric['max_marks']} marks):
{criteria_text}

Return ONLY this JSON object:
{{
  "marks_awarded": <integer from 0 to {rubric['max_marks']}>,
  "max_marks": {rubric['max_marks']},
  "feedback": "<2-3 sentences of constructive feedback for the student>",
  "justification": "<specific explanation of which rubric criteria were met or missed>"
}}"""
    else:
        return f"""Evaluate the following student answer using general academic judgment.

QUESTION:
{question}

STUDENT ANSWER:
{answer}

Evaluate out of 5 marks based on accuracy, completeness, and clarity.

Return ONLY this JSON object:
{{
  "marks_awarded": <integer from 0 to 5>,
  "max_marks": 5,
  "feedback": "<2-3 sentences of constructive feedback for the student>",
  "justification": "<explanation of why these marks were awarded>"
}}"""

def evaluate_answer(question: str, answer: str, rubric: dict = None, use_rubric: bool = True) -> dict:
    # 1. Apply Fallback Rubric if no rubric is provided
    if use_rubric and not rubric:
        rubric = FALLBACK_RUBRIC
    
    default_max = rubric["max_marks"] if rubric else 5
    prompt = build_prompt(question, answer, rubric, use_rubric)

    try:
        # 2. Call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Groq's fastest large model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} # Forces native JSON output
        )

        raw = response.choices[0].message.content.strip()
        result = json.loads(raw)
        
        # 3. Clean and validate types
        result["marks_awarded"] = int(result.get("marks_awarded", 0))
        result["max_marks"]     = int(result.get("max_marks", default_max))
        result["feedback"]      = str(result.get("feedback", ""))
        result["justification"] = str(result.get("justification", ""))

        return result

    except Exception as e:
        # Catch errors gracefully so Flask doesn't crash
        return {
            "marks_awarded": 0,
            "max_marks": default_max,
            "feedback": "An error occurred communicating with the Groq API.",
            "justification": f"System Error: {str(e)}"
        }