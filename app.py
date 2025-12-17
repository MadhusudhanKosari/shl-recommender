from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender.recommender import recommend_assessments

app = Flask(__name__)
CORS(app)  # <-- THIS LINE FIXES CORS


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "query missing"}), 400

    urls = recommend_assessments(data["query"])

    results = []
    for url in urls:
        results.append({
            "name": "SHL Assessment",
            "url": url,
            "description": "Recommended based on similar SHL hiring queries",
            "duration": 40,
            "remote_support": "Yes",
            "adaptive_support": "No",
            "test_type": ["K", "P"]
        })

    return jsonify({"recommended_assessments": results}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
