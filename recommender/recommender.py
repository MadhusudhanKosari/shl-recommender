from recommender.load_data import load_train_data
import re

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
    keywords = extract_keywords(query)
    query_text = query.lower()

    results = []

    for _, row in df.iterrows():
        past_query = row["Query"].lower()
        url = row["Assessment_url"]

        score = 0
        reasons = []

        # keyword overlap
        for word in keywords:
            if word in past_query:
                score += 2
                if word not in reasons:
                    reasons.append(word)

        # role-specific boost
        for role in ["java", "python", "sql", "analyst", "sales", "manager"]:
            if role in query_text and role in past_query:
                score += 3
                reasons.append(f"{role} role relevance")

        # duration awareness
        if "40" in query_text and "40" in past_query:
            score += 2
            reasons.append("matches 40-minute assessment duration")

        if score > 0:
            reason_text = "Matched " + ", ".join(reasons[:3]) if reasons else "Relevant to similar SHL hiring queries"

            results.append({
                "url": url,
                "score": score,
                "reason": reason_text
            })

    # sort by score
    ranked = sorted(results, key=lambda x: x["score"], reverse=True)

    return ranked[:top_k]


