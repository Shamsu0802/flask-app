from flask import Flask, request, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load and normalize dataset
df = pd.read_csv("places_cleaned_single_values.csv")
df.columns = df.columns.str.strip().str.lower()
for col in ['mood', 'budget', 'companion', 'time']:
    df[col] = df[col].astype(str).str.strip().str.lower()

# Mappings
time_map = {
    "1-2 hours": "two hours",
    "half day": "half a day",
    "full day": "full day",
    "weekend trip": "weekend trip"
}

budget_map = {
    "low": "low",
    "mid": "mid",
    "high": "high",
    "free": "free"
}

companion_map = {
    "solo": "solo",
    "friends": "friends",
    "family": "family",
    "partner": "date"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questions')
def questions():
    return render_template('questions.html')

@app.route('/get-itinerary', methods=['POST'])
def get_itinerary():
    mood = request.form.get("mood", "").strip().lower()
    time = request.form.get("time", "").strip().lower()
    budget = request.form.get("budget", "").strip().lower()
    companion = request.form.get("companion", "").strip().lower()

    time = time_map.get(time, time)
    budget = budget_map.get(budget, budget)
    companion = companion_map.get(companion, companion)

    filtered_df = df[
        (df['mood'] == mood) &
        (df['time'] == time) &
        (df['budget'] == budget) &
        (df['companion'].str.contains(companion, case=False, na=False))
    ]

    if filtered_df.empty:
        filtered_df = df[df['mood'] == mood]
        message = "Sorry, we couldn't find a perfect match. Here are some similar places!"
    else:
        message = f"Your personalized itinerary for a {mood} mood is ready!"

    places = filtered_df.to_dict(orient='records')

    return render_template("itinerary.html", message=message, places=places)

if __name__ == '__main__':
    app.run(debug=True)
