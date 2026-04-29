<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini Answer Evaluator - README</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            background-color: #ffffff;
            margin: 0;
            padding: 40px 20px;
        }
        .container {
            max-width: 850px;
            margin: 0 auto;
            background: #ffffff;
            padding: 30px 40px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border: 1px solid #e1e4e8;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            color: #f37b21; /* Groq Orange */
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 1.1em;
            color: #586069;
            margin-bottom: 40px;
            font-style: italic;
        }
        h2 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 8px;
            color: #24292e;
            margin-top: 40px;
        }
        h3 {
            color: #24292e;
            margin-top: 25px;
        }
        p, li {
            font-size: 16px;
            color: #333333;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin-bottom: 8px;
        }
        pre {
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 14px;
            line-height: 1.45;
        }
        code {
            background-color: #f6f8fa;
            color: #d73a49;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 14px;
        }
        pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
        }
        blockquote {
            padding: 10px 20px;
            margin: 20px 0;
            border-left: 5px solid #f37b21;
            background-color: #fff8f2;
            color: #24292e;
            border-radius: 0 6px 6px 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            padding: 12px 15px;
            border: 1px solid #dfe2e5;
            text-align: left;
        }
        th {
            background-color: #f6f8fa;
            font-weight: 600;
        }
        tr:nth-child(even) {
            background-color: #fcfcfc;
        }
        .highlight {
            font-weight: bold;
            color: #f37b21;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>🎓 Mini Answer Evaluator</h1>
    <div class="subtitle">A rubric-based student answer evaluation system powered by Groq (Llama 3). Built as part of the Evalvia project.</div>

    <h2>✨ What It Does</h2>
    <p>Given a <strong>question</strong>, a <strong>student answer</strong>, and a <strong>rubric</strong> (auto-retrieved by subject), the system uses the Groq API to return:</p>
    <ul>
        <li><strong>Marks awarded</strong> out of a maximum</li>
        <li><strong>Feedback</strong> — constructive, student-friendly</li>
        <li><strong>Justification</strong> — which rubric criteria were met or missed</li>
    </ul>
    <p>It also supports a <strong>compare mode</strong> that runs evaluation both with and without the rubric side-by-side, showing how structured rubrics improve grading consistency.</p>

    <h2>📂 Project Structure</h2>
<pre><code>mini-answer-evaluator/
├── backend/
│   ├── app.py            # Flask API server (3 endpoints)
│   ├── rubrics.py        # Rubric definitions + keyword-based retrieval
│   ├── evaluator.py      # Groq API integration + prompt building
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html        # Main UI
│   └── static/
│       ├── css/style.css
│       └── js/app.js     # API calls + rendering
└── README.md</code></pre>

    <h2>🚀 Setup & Running</h2>

    <h3>1. Clone the repo</h3>
<pre><code>git clone https://github.com/your-username/mini-answer-evaluator.git
cd mini-answer-evaluator</code></pre>

    <h3>2. Backend</h3>
<pre><code>cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your Groq API key</code></pre>

<pre><code>python app.py
# Flask runs on http://localhost:5000</code></pre>

    <h3>3. Frontend</h3>
    <p>Open <code>frontend/index.html</code> directly in your browser — no build step needed.</p>
    <blockquote>
        <strong>Note:</strong> Make sure the Flask backend is running before you evaluate.
    </blockquote>

    <h2>🌐 API Endpoints</h2>
    <table>
        <thead>
            <tr>
                <th>Method</th>
                <th>Endpoint</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>POST</code></td>
                <td><span class="highlight">/api/retrieve-rubric</span></td>
                <td>Returns the matched rubric for a question</td>
            </tr>
            <tr>
                <td><code>POST</code></td>
                <td><span class="highlight">/api/evaluate</span></td>
                <td>Evaluates an answer with or without rubric</td>
            </tr>
            <tr>
                <td><code>POST</code></td>
                <td><span class="highlight">/api/compare</span></td>
                <td>Returns both with-rubric and without-rubric results</td>
            </tr>
        </tbody>
    </table>

    <h2>🧠 Approach</h2>

    <h3>Rubric Retrieval</h3>
    <p>Simple <strong>keyword frequency matching</strong> — no embeddings required.</p>
    <p>Each rubric has a list of domain keywords. The question text is lowercased and each rubric's keywords are counted. The rubric with the highest match count wins. If no keywords match, the mandatory <strong>fallback rubric</strong> (general academic quality) is safely used.</p>
    <p><em>Subjects covered:</em> Physics, Mathematics, Chemistry, English, Biology, History + Fallback.</p>

    <h3>Prompt Design</h3>
    <p>Two prompt modes are used:</p>
    <ul>
        <li><strong>With rubric</strong> — Passes the numbered criteria explicitly. The LLM is instructed to award marks per criterion and explain which were met or missed.</li>
        <li><strong>Without rubric</strong> — The LLM evaluates on general academic merit (accuracy, completeness, clarity) out of 5.</li>
    </ul>
    <p>Both prompts instruct the model to return <strong>only valid JSON</strong> with no preamble or markdown fences. The core system prompt used is:</p>
    <blockquote>
        System: "You are an expert academic evaluator for school and college exams. Evaluate student answers fairly and constructively based on the provided rubric. Return ONLY a valid JSON object."
    </blockquote>

    <h3>Structured Output</h3>
    <p>To guarantee stability and avoid messy string parsing, the backend leverages Groq's native structured JSON output feature by passing <code>response_format={"type": "json_object"}</code> in the API call. The response is immediately loaded into a Python dictionary, validated, type-cast, and sent to the frontend.</p>

    <h2>📋 Rubric Format</h2>
    <p>Each rubric follows this structure:</p>
<pre><code>{
  "name": "Physics (Class 12)",
  "keywords": ["force", "motion", "newton", ...],
  "max_marks": 5,
  "criteria": [
    "Correct definition or statement of the concept (1 mark)",
    "Relevant formula stated accurately with symbols defined (1 mark)",
    ...
  ]
}</code></pre>
    <p>To add a new subject, add an entry to <code>RUBRICS</code> in <code>backend/rubrics.py</code>.</p>

    <h2>🔮 Improvements I Would Make</h2>
    <ol>
        <li><strong>Regex Word Boundary Matching</strong> — Currently, the rubric retrieval uses basic substring matching. A future improvement would be to use Regex word boundaries (e.g., <code>re.search(r'\b' + kw + r'\b', q)</code>) to ensure we only match whole words, preventing false positives.</li>
        <li><strong>Embedding-based retrieval</strong> — Use semantic similarity (e.g. <code>sentence-transformers</code>) instead of keyword matching for more robust rubric selection, especially for ambiguous questions.</li>
        <li><strong>Per-criterion scoring</strong> — Ask the LLM to score each rubric criterion individually (0 or 1) rather than a single total, giving finer-grained and more auditable results.</li>
        <li><strong>Rubric editor UI</strong> — Let teachers create and edit rubrics in the browser without touching code.</li>
        <li><strong>Answer history</strong> — Store past evaluations in a lightweight database (SQLite) so teachers can track student progress over time.</li>
        <li><strong>Batch evaluation</strong> — Upload a CSV of student answers and evaluate all at once.</li>
    </ol>

    <h2>💻 Tech Stack</h2>
    <table>
        <thead>
            <tr>
                <th>Layer</th>
                <th>Technology</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Backend</strong></td>
                <td>Python 3.12, Flask, python-dotenv</td>
            </tr>
            <tr>
                <td><strong>LLM</strong></td>
                <td>Groq API (<code>llama-3.3-70b-versatile</code>)</td>
            </tr>
            <tr>
                <td><strong>Frontend</strong></td>
                <td>Vanilla HTML/CSS/JS (no framework)</td>
            </tr>
            <tr>
                <td><strong>Rubric retrieval</strong></td>
                <td>Keyword frequency matching</td>
            </tr>
        </tbody>
    </table>

    <h2>🔐 Environment Variables</h2>
    <table>
        <thead>
            <tr>
                <th>Variable</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>GROQ_API_KEY</code></td>
                <td>Your Groq API key (get one for free at console.groq.com)</td>
            </tr>
        </tbody>
    </table>
</div>

</body>
</html>