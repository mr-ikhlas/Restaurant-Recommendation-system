from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset
data = pd.read_csv("restaurants.csv")

# Clean dataset once
data["Location"] = data["Location"].astype(str).str.strip()
data["Cuisine"] = data["Cuisine"].astype(str).str.strip()
data["Budget"] = data["Budget"].astype(str).str.strip()
data["Rating"] = pd.to_numeric(data["Rating"], errors="coerce")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    recommendations = []

    if request.method == "POST":
        location = request.form.get("location", "").strip().lower()
        cuisine = request.form.get("cuisine", "").strip().lower()
        budget = request.form.get("budget", "").strip().lower()
        min_rating = request.form.get("rating", "").strip()

        filtered_data = data.copy()

        # Filter by location
        if location:
            filtered_data = filtered_data[
                filtered_data["Location"].str.lower() == location
            ]

        # Filter by cuisine
        if cuisine:
            filtered_data = filtered_data[
                filtered_data["Cuisine"].str.lower() == cuisine
            ]

        # Filter by budget
        if budget:
            filtered_data = filtered_data[
                filtered_data["Budget"].str.lower() == budget
            ]

        # Filter by rating
        if min_rating:
            try:
                min_rating = float(min_rating)
                filtered_data = filtered_data[
                    filtered_data["Rating"] >= min_rating
                ]
            except ValueError:
                pass

        recommendations = filtered_data.to_dict(orient="records")

    return render_template("web.html", recommendations=recommendations)


if __name__ == "__main__":
    app.run(debug=True, port=5000)