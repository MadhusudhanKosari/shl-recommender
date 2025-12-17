from urllib import response
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

    recommendations = recommend_assessments(data["query"])

    response = {
        "recommended_assessments": [
            {
                "name": "SHL Assessment",
                "url": item["url"],
                "description": item["reason"],
                "duration": 40,
                "remote_support": "Yes",
                "adaptive_support": "No",
                "test_type": ["K", "P"]
            }
            for item in recommendations
        ]
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
