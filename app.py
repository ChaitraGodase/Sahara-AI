# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
import json
from chat_utils import generate_response
from sentiment_utils import analyze_sentiment
from recommendations import recommend_activity

app = Flask(__name__)

CSV_FILE = "mood_log.csv"

# Load or initialize mood log
try:
    mood_df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
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
        mood_df = pd.concat(
            [mood_df, pd.DataFrame([[date, mood_text, sentiment]], columns=mood_df.columns)],
            ignore_index=True
        )
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

# Main entry point
if __name__ == "__main__":
    # host='0.0.0.0' allows external access (ngrok or Render)
    app.run(debug=True, host="0.0.0.0", port=5000)
