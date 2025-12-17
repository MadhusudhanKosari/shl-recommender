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
    scores = {}

    for _, row in df.iterrows():
        past_query = row["Query"].lower()
        url = row["Assessment_url"]

        score = 0
        for word in keywords:
            if word in past_query:
                score += 1

        if score > 0:
            scores[url] = scores.get(url, 0) + score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [url for url, _ in ranked[:top_k]]
