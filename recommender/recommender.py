from recommender.load_data import load_train_data
import re
STOPWORDS = {
    "i", "am", "for", "with", "and", "or", "the", "a", "an",
    "to", "in", "on", "of", "it", "is", "are", "be", "this",
    "that", "as", "at", "by", "from", "we", "you", "they",
    "looking", "hire", "hiring", "need", "required", "required"
}
SKILL_KEYWORDS = {
    "java": "Java programming",
    "python": "Python programming",
    "sql": "SQL skills",
    "sales": "sales roles",
    "analyst": "analyst roles",
    "manager": "managerial roles",
    "product": "product-focused roles",
    "marketing": "marketing roles"
}

EXPERIENCE_KEYWORDS = {
    "year": "experience requirements",
    "years": "experience requirements",
    "experience": "experience requirements",
    "senior": "senior-level roles",
    "junior": "entry-level roles"
}

df = load_train_data()

def extract_keywords(query):
    """
    Very simple keyword extractor:
    - lowercase
    - remove symbols
    - split words
    """
    query = query.lower()
    query = re.sub(r"[^a-z0-9 ]", " ", query)
    words = query.split()
    return set(words)

def recommend_assessments(query, top_k=5):
    query_text = query.lower()
    results = []

    for _, row in df.iterrows():
        past_query = row["Query"].lower()
        url = row["Assessment_url"]

        score = 0
        reasons = []

        # Skill-based reasoning
        for key, label in SKILL_KEYWORDS.items():
            if key in query_text and key in past_query:
                score += 3
                if label not in reasons:
                    reasons.append(label)

        # Experience-based reasoning
        for key, label in EXPERIENCE_KEYWORDS.items():
            if key in query_text and key in past_query:
                score += 2
                if label not in reasons:
                    reasons.append(label)

        # Duration awareness
        if "40" in query_text and "40" in past_query:
            score += 2
            reasons.append("40-minute assessment duration")

        # Skip completely irrelevant rows
        if score == 0:
            continue

        # Build human-friendly reason
        if reasons:
            reason_text = "Relevant for " + " and ".join(reasons[:2])
        else:
            reason_text = "Relevant for " + summarize_query_intent(query)

        results.append({
            "url": url,
            "score": score,
            "reason": reason_text
        })

    # Sort by relevance
    ranked = sorted(results, key=lambda x: x["score"], reverse=True)
    return ranked[:top_k]

def summarize_query_intent(query):
    query = query.lower()

    if "java" in query:
        return "Java developer hiring requirements"
    if "product" in query:
        return "product-oriented role requirements"
    if "analyst" in query:
        return "analyst role requirements"
    if "sales" in query:
        return "sales role hiring needs"
    if "manager" in query:
        return "managerial role requirements"

    if "experience" in query or "year" in query:
        return "experience-based hiring requirements"

    return "the given hiring requirements"


