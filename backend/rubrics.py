"""
rubrics.py — Rubric definitions and keyword-based retrieval logic.

Each rubric has:
  - name: Display name
  - keywords: Words used to match this rubric to a question
  - max_marks: Total marks for this rubric
  - criteria: List of marking criteria (each worth 1 mark)
"""

RUBRICS = {
    "physics": {
        "name": "Physics (Class 12)",
        "keywords": [
            "force", "motion", "velocity", "acceleration", "newton", "energy",
            "work", "power", "momentum", "wave", "current", "voltage", "resistance",
            "electric", "magnetic", "light", "optics", "lens", "refraction",
            "reflection", "gravitation", "pressure", "fluid", "thermodynamics",
            "heat", "temperature", "law", "formula", "equation", "mass", "density",
            "friction", "torque", "inertia", "displacement", "speed", "frequency",
            "amplitude", "wavelength", "capacitor", "inductor", "circuit", "charge",
            "potential", "field", "nucleus", "radioactive", "photoelectric"
        ],
        "max_marks": 5,
        "criteria": [
            "Correct definition or statement of the concept (1 mark)",
            "Relevant formula stated accurately with symbols defined (1 mark)",
            "Derivation or explanation of the formula if asked (1 mark)",
            "Correct numerical application or worked example (1 mark)",
            "Units, significant figures, and SI notation correct (1 mark)"
        ]
    },

    "mathematics": {
        "name": "Mathematics (Class 12)",
        "keywords": [
            "prove", "differentiate", "integrate", "derivative", "integral",
            "matrix", "determinant", "vector", "limit", "continuity", "function",
            "equation", "solve", "graph", "calculus", "probability", "statistics",
            "mean", "median", "mode", "binomial", "theorem", "set", "relation",
            "sequence", "series", "arithmetic", "geometric", "triangle", "circle",
            "parabola", "ellipse", "hyperbola", "coordinate", "line", "plane",
            "angle", "polygon", "area", "volume", "permutation", "combination",
            "logarithm", "exponential", "inverse", "domain", "range", "bijection"
        ],
        "max_marks": 5,
        "criteria": [
            "Correct identification of the method or approach (1 mark)",
            "All steps shown clearly and logically (1 mark)",
            "Intermediate calculations correct (1 mark)",
            "Final answer correct with proper units or simplification (1 mark)",
            "No missing steps; conclusion stated clearly (1 mark)"
        ]
    },

    "chemistry": {
        "name": "Chemistry (Class 12)",
        "keywords": [
            "reaction", "element", "compound", "bond", "atom", "molecule",
            "electron", "proton", "neutron", "acid", "base", "salt", "ph",
            "oxidation", "reduction", "catalyst", "polymer", "organic", "inorganic",
            "periodic", "valency", "mole", "molarity", "concentration", "equilibrium",
            "rate", "enthalpy", "entropy", "gibbs", "electrode", "electrolysis",
            "cell", "galvanic", "ester", "alcohol", "aldehyde", "ketone",
            "carboxylic", "amine", "benzene", "hybridization", "isomer", "alkane",
            "alkene", "alkyne", "reagent", "solubility", "precipitate"
        ],
        "max_marks": 5,
        "criteria": [
            "Correct statement of the concept or definition (1 mark)",
            "Balanced chemical equation where applicable (1 mark)",
            "Explanation of mechanism or process (1 mark)",
            "Correct use of chemical names, symbols, and formulas (1 mark)",
            "Application or example provided accurately (1 mark)"
        ]
    },

    "english": {
        "name": "English (Class 10)",
        "keywords": [
            "theme", "character", "plot", "story", "poem", "prose", "author",
            "writer", "passage", "comprehension", "essay", "letter", "paragraph",
            "vocabulary", "grammar", "tense", "voice", "narration", "figure",
            "speech", "metaphor", "simile", "alliteration", "rhyme", "stanza",
            "chapter", "moral", "lesson", "explain", "describe", "analyze",
            "summarize", "compare", "tone", "mood", "setting", "conflict",
            "protagonist", "antagonist", "dialogue", "narrative", "literary"
        ],
        "max_marks": 5,
        "criteria": [
            "Relevance to the question and coverage of central idea (1 mark)",
            "Key points or textual evidence included (1 mark)",
            "Clarity and coherence of explanation (1 mark)",
            "Correct grammar, spelling, and sentence structure (1 mark)",
            "Use of appropriate vocabulary and expression (1 mark)"
        ]
    },

    "biology": {
        "name": "Biology (Class 12)",
        "keywords": [
            "cell", "organism", "dna", "rna", "gene", "chromosome", "mitosis",
            "meiosis", "photosynthesis", "respiration", "digestion", "excretion",
            "reproduction", "evolution", "ecosystem", "food", "chain", "web",
            "enzyme", "hormone", "nerve", "brain", "heart", "blood", "tissue",
            "organ", "system", "bacteria", "virus", "fungi", "plant", "animal",
            "classification", "taxonomy", "ecology", "mutation", "heredity",
            "protein", "amino", "osmosis", "diffusion", "membrane", "nucleus",
            "chloroplast", "mitochondria", "ribosome", "antibody", "antigen"
        ],
        "max_marks": 5,
        "criteria": [
            "Correct definition or identification of the biological concept (1 mark)",
            "Accurate description of the process or structure (1 mark)",
            "Relevant diagram or labeled parts mentioned if applicable (1 mark)",
            "Correct scientific terminology used throughout (1 mark)",
            "Examples or applications stated correctly (1 mark)"
        ]
    },

    "history": {
        "name": "History (Class 10)",
        "keywords": [
            "war", "revolution", "empire", "colonialism", "independence", "movement",
            "century", "civilization", "culture", "trade", "treaty", "leader",
            "president", "king", "queen", "nation", "state", "government", "reform",
            "society", "economy", "religion", "art", "architecture", "period",
            "dynasty", "battle", "cause", "effect", "consequence", "impact",
            "change", "continuity", "industrial", "french", "world", "british",
            "indian", "nationalist", "colonial", "freedom", "struggle", "protest"
        ],
        "max_marks": 5,
        "criteria": [
            "Accurate identification of the historical event, period, or person (1 mark)",
            "Key causes or background context explained (1 mark)",
            "Main events or developments described in sequence (1 mark)",
            "Impact or consequences discussed (1 mark)",
            "Dates, names, and facts used correctly (1 mark)"
        ]
    },

    "fallback": {
        "name": "General (Fallback Rubric)",
        "keywords": [],
        "max_marks": 5,
        "criteria": [
            "Relevance to the question asked (1 mark)",
            "Coverage of all key points required by the question (1 mark)",
            "Clarity and coherence of the explanation (1 mark)",
            "Logical structure and flow of the answer (1 mark)",
            "Quality of language and correct terminology (1 mark)"
        ]
    }
}


def detect_subject(question: str) -> tuple[str, bool]:
    """
    Detect the subject from the question text using keyword frequency matching.
    Returns (subject_key, matched) where matched=False means fallback was used.
    """
    q = question.lower()
    best_subject = "fallback"
    best_score = 0

    for key, rubric in RUBRICS.items():
        if key == "fallback":
            continue
        score = sum(1 for kw in rubric["keywords"] if kw in q)
        if score > best_score:
            best_score = score
            best_subject = key

    return best_subject, best_score > 0


def get_rubric(question: str, subject_override: str = "auto") -> tuple[dict, bool]:
    """
    Retrieve the most relevant rubric for a given question.

    Args:
        question: The exam question text
        subject_override: Explicit subject key, or "auto" to detect from question

    Returns:
        (rubric_dict, is_match) where is_match=False means fallback was used
    """
    if subject_override and subject_override != "auto":
        rubric = RUBRICS.get(subject_override, RUBRICS["fallback"])
        return rubric, subject_override in RUBRICS

    subject, matched = detect_subject(question)
    return RUBRICS[subject], matched
