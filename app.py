import os
import json
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, jsonify
import pandas as pd

from chat_utils import generate_response
from sentiment_utils import analyze_sentiment
from recommendations import recommend_activity

app = Flask(__name__)

# Ensure data folder exists and use a safe CSV path
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
CSV_FILE = DATA_DIR / "mood_log.csv"

# Load or initialize mood log
try:
    mood_df = pd.read_csv(CSV_FILE)
    # ensure expected columns
    if set(["date", "mood_text", "sentiment"]) - set(mood_df.columns):
        mood_df = pd.DataFrame(columns=["date", "mood_text", "sentiment"])
except (FileNotFoundError, pd.errors.EmptyDataError):
    mood_df = pd.DataFrame(columns=["date", "mood_text", "sentiment"])

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Chat page
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form.get("message", "").strip()
        if not user_message:
            return render_template("chat.html", error="Please type something.")
        bot_response = generate_response(user_message)
        return render_template("chat.html", user_message=user_message, bot_response=bot_response)
    return render_template("chat.html")

# Chat API for AJAX (optional)
@app.route("/chat_api", methods=["POST"])
def chat_api():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"response": "Please send a message."})
    response = generate_response(message)
    return jsonify({"response": response})

# Mood logging
@app.route("/mood", methods=["GET", "POST"])
def mood():
    global mood_df
    if request.method == "POST":
        mood_text = request.form.get("mood_text", "").strip()
        if not mood_text:
            return render_template("mood.html", error="Please write how you feel.")
        sentiment = analyze_sentiment(mood_text)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = pd.DataFrame([[date, mood_text, sentiment]], columns=["date", "mood_text", "sentiment"])
        mood_df = pd.concat([mood_df, new_row], ignore_index=True)
        # persist
        mood_df.to_csv(CSV_FILE, index=False)
        activities = recommend_activity(sentiment)
        return render_template("mood.html", sentiment=sentiment, activities=activities, mood_text=mood_text)
    return render_template("mood.html")

# Dashboard route
@app.route("/dashboard")
def dashboard():
    global mood_df
    if mood_df.empty:
        data_json = json.dumps([])
    else:
        def s2n(s):
            return 1 if s == "Positive" else (-1 if s == "Negative" else 0)
        data_points = [
            {"date": row["date"], "sentiment": row["sentiment"], "value": s2n(row["sentiment"])}
            for _, row in mood_df.iterrows()
        ]
        data_json = json.dumps(data_points)
    return render_template("dashboard.html", mood_data=data_json)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
@app.route("/healthz")
def health():
    return "OK", 200
