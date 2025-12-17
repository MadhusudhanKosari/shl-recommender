import pandas as pd
from recommender.recommender import recommend_assessments

# Load training data
df = pd.read_excel("data/shl_data.xlsx")
df = df[["Query", "Assessment_url"]].dropna()

def recall_at_k(actual, predicted, k):
    predicted_k = predicted[:k]
    return len(set(actual) & set(predicted_k)) / len(set(actual))

queries = df["Query"].unique()

recalls = []

for q in queries:
    actual_urls = df[df["Query"] == q]["Assessment_url"].tolist()
    predicted_urls = recommend_assessments(q, top_k=10)

    r = recall_at_k(actual_urls, predicted_urls, k=10)
    recalls.append(r)

mean_recall = sum(recalls) / len(recalls)

print("Mean Recall@10:", round(mean_recall, 3))
