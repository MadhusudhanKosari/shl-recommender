import pandas as pd
from recommender.recommender import recommend_assessments

# Load test data (only Query column)
df = pd.read_excel("data/shl_data.xlsx")
test_queries = df["Query"].dropna().unique()

rows = []

for query in test_queries:
    urls = recommend_assessments(query, top_k=10)
    for url in urls:
        rows.append({
            "Query": query,
            "Assessment_url": url
        })

output = pd.DataFrame(rows)
output.to_csv("submission.csv", index=False)

print("submission.csv generated successfully")
