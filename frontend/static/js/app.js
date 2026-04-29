/**
 * app.js — Mini Answer Evaluator frontend logic
 *
 * Handles:
 * - Live rubric preview as user types
 * - API calls to Flask backend (/api/evaluate, /api/compare)
 * - Rendering evaluation results and comparison view
 */

const API_BASE = "https://YOUR-BACKEND-NAME.onrender.com"; // <--- PASTE YOUR ACTUAL RENDER URL HERE (No trailing slash!)

// ── DOM refs ──────────────────────────────────────────────────────────────────
const subjectSelect  = document.getElementById("subjectSelect");
const questionInput  = document.getElementById("questionInput");
const answerInput    = document.getElementById("answerInput");
const rubricPreview  = document.getElementById("rubricPreview");
const resultArea     = document.getElementById("resultArea");
const evalBtn        = document.getElementById("evalBtn");
const compareBtn     = document.getElementById("compareBtn");

// ── Live rubric preview ───────────────────────────────────────────────────────
questionInput.addEventListener("input", debounce(updateRubricPreview, 400));
subjectSelect.addEventListener("change", updateRubricPreview);

async function updateRubricPreview() {
  const question = questionInput.value.trim();
  const subject  = subjectSelect.value;

  if (!question) { rubricPreview.innerHTML = ""; return; }

  try {
    const res  = await fetch(`${API_BASE}/api/retrieve-rubric`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ question, subject })
    });
    const data = await res.json();
    renderRubricPreview(data.rubric, data.is_match);
  } catch {
    rubricPreview.innerHTML = "";
  }
}

function renderRubricPreview(rubric, isMatch) {
  const tagClass = isMatch ? "tag-match" : "tag-fallback";
  const tagLabel = isMatch ? "Subject match" : "Fallback";

  rubricPreview.innerHTML = `
    <div class="rubric-preview">
      <div class="rub-label">
        <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
          <path d="M6 1L1 3.5v5L6 11l5-2.5v-5L6 1zm0 1.5 3.5 1.75L6 6 2.5 4.25 6 2.5zM2 5.5 5.5 7.25v3.5L2 9V5.5zm5 5.25v-3.5L10.5 5.5V9L7 10.75z"/>
        </svg>
        Retrieved Rubric
        <span class="tag ${tagClass}">${tagLabel}</span>
      </div>
      <div class="rub-name">${rubric.name} — ${rubric.max_marks} marks</div>
      <ul class="rubric-criteria">
        ${rubric.criteria.map(c => `<li>${c}</li>`).join("")}
      </ul>
    </div>
  `;
}

// ── Evaluate button ───────────────────────────────────────────────────────────
evalBtn.addEventListener("click", () => runEvaluation(false));
compareBtn.addEventListener("click", () => runEvaluation(true));

async function runEvaluation(compare) {
  const question = questionInput.value.trim();
  const answer   = answerInput.value.trim();
  const subject  = subjectSelect.value;

  if (!question || !answer) {
    resultArea.innerHTML = `
      <div class="error-box">
        <strong>Missing input.</strong><br>
        Please enter both a question and a student answer before evaluating.
      </div>`;
    return;
  }

  setLoading(true);

  try {
    if (compare) {
      const res  = await fetch(`${API_BASE}/api/compare`, {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ question, answer, subject })
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      renderCompare(data);
    } else {
      const res  = await fetch(`${API_BASE}/api/evaluate`, {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ question, answer, subject, use_rubric: true })
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      renderResult(data);
    }
  } catch (err) {
    resultArea.innerHTML = `
      <div class="error-box">
        <strong>Evaluation failed.</strong><br>
        ${err.message || "Could not connect to the backend. It may be sleeping (Render free tier) or unavailable."}
      </div>`;
  } finally {
    setLoading(false);
  }
}

// ── Render: single result ─────────────────────────────────────────────────────
function renderResult(data) {
  const color = scoreColor(data.marks_awarded, data.max_marks);
  const pct   = Math.round((data.marks_awarded / data.max_marks) * 100);

  resultArea.innerHTML = `
    <div class="result-panel">
      <div class="score-display">
        <div class="score-circle">
          ${donutSVG(data.marks_awarded, data.max_marks, color)}
          <div class="score-text">
            <span class="score-num" style="color:${color}">${data.marks_awarded}/${data.max_marks}</span>
            <span class="score-denom">${pct}%</span>
          </div>
        </div>
      </div>

      <div class="result-section feedback-section">
        <div class="rs-label">Feedback</div>
        <p>${escHtml(data.feedback)}</p>
      </div>

      <div class="result-section justification-section">
        <div class="rs-label">Justification</div>
        <p>${escHtml(data.justification)}</p>
      </div>

      <div class="result-section">
        <div class="rs-label">Rubric used</div>
        <p style="font-size:0.82rem">${escHtml(data.rubric_used)}</p>
      </div>
    </div>
  `;
}

// ── Render: comparison view ───────────────────────────────────────────────────
function renderCompare(data) {
  const wr  = data.with_rubric;
  const nor = data.without_rubric;

  resultArea.innerHTML = `
    <div class="result-panel">
      <div style="font-size:0.78rem;color:var(--text3);text-align:center;margin-bottom:0.5rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase">
        Side-by-side comparison
      </div>

      <div class="compare-row">
        <div class="compare-card with-rubric">
          <div class="cc-label">With rubric</div>
          <div class="cc-score" style="color:${scoreColor(wr.marks_awarded, wr.max_marks)}">
            ${wr.marks_awarded}/${wr.max_marks}
          </div>
          <div class="cc-feedback">${escHtml(wr.feedback)}</div>
        </div>
        <div class="compare-card without-rubric">
          <div class="cc-label">Without rubric</div>
          <div class="cc-score" style="color:${scoreColor(nor.marks_awarded, nor.max_marks)}">
            ${nor.marks_awarded}/${nor.max_marks}
          </div>
          <div class="cc-feedback">${escHtml(nor.feedback)}</div>
        </div>
      </div>

      <div class="divider"></div>

      <div class="result-section feedback-section">
        <div class="rs-label">Rubric-based justification</div>
        <p>${escHtml(wr.justification)}</p>
      </div>

      <div class="result-section justification-section">
        <div class="rs-label">General justification</div>
        <p>${escHtml(nor.justification)}</p>
      </div>

      <div class="result-section">
        <div class="rs-label">Rubric retrieved</div>
        <p style="font-size:0.82rem">${escHtml(data.rubric.name)}
          — <span style="color:var(--text3)">${data.rubric_is_match ? "subject match" : "fallback"}</span>
        </p>
      </div>
    </div>
  `;
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function setLoading(on) {
  evalBtn.disabled    = on;
  compareBtn.disabled = on;

  if (on) {
    resultArea.innerHTML = `
      <div class="loading-state">
        <button class="btn" disabled style="width:auto;padding:0.6rem 1.4rem;margin-bottom:1rem">
          <div class="loading-dots"><span></span><span></span><span></span></div>
          Evaluating...
        </button>
        <p style="font-size:0.82rem">Sending to Groq API…</p>
      </div>`;
  }
}

function scoreColor(marks, max) {
  const pct = marks / max;
  if (pct >= 0.8) return "#2a7a4a";
  if (pct >= 0.5) return "#8a5a0a";
  return "#a82010";
}

function donutSVG(marks, max, color) {
  const r    = 42;
  const circ = 2 * Math.PI * r;
  const dash = circ * (marks / max);
  return `
    <svg viewBox="0 0 110 110">
      <circle cx="55" cy="55" r="${r}" fill="none" stroke="#f0ede7" stroke-width="9"/>
      <circle cx="55" cy="55" r="${r}" fill="none" stroke="${color}" stroke-width="9"
        stroke-dasharray="${dash} ${circ}" stroke-dashoffset="${circ / 4}"
        stroke-linecap="round"/>
    </svg>`;
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}