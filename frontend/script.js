const API_URL = "https://shl-recommender-api-b57h.onrender.com/recommend";

function getRecommendations() {
  const query = document.getElementById("queryInput").value.trim();
  if (!query) {
    alert("Please enter a query");
    return;
  }

  document.getElementById("results").innerHTML = "";
  document.getElementById("loading").classList.remove("hidden");

  fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ query: query })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("loading").classList.add("hidden");

      const resultsDiv = document.getElementById("results");

      data.recommended_assessments.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
          <h3>${item.name}</h3>
          <p><strong>Why recommended:</strong> ${item.description}</p>
          <p><strong>Duration:</strong> ${item.duration} mins</p>
          <p><strong>Test Type:</strong> ${item.test_type.join(", ")}</p>
          <a href="${item.url}" target="_blank">View Assessment</a>
        `;

        resultsDiv.appendChild(card);
      });
    })
    .catch(err => {
      document.getElementById("loading").classList.add("hidden");
      alert("Error fetching recommendations");
      console.error(err);
    });
}
