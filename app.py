# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from datetime import datetime
import json
from chat_utils import generate_response
from sentiment_utils import analyze_sentiment
from recommendations import recommend_activity

app = Flask(__name__)

CSV_FILE = "mood_log.csv"

# load or init mood log
try:
    mood_df = pd.read_csv(CSV_FILE)
except Exception:
    mood_df = pd.DataFrame(columns=["date", "mood_text", "sentiment"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form.get("message", "").strip()
        if not user_message:
            return render_template("chat.html", error="Please type something.")
        bot_response = generate_response(user_message)
        return render_template("chat.html", user_message=user_message, bot_response=bot_response)
    return render_template("chat.html")

@app.route("/chat_api", methods=["POST"])
def chat_api():
    # for AJAX (optional)
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"response": "Please send a message."})
    response = generate_response(message)
    return jsonify({"response": response})

@app.route("/mood", methods=["GET", "POST"])
def mood():
    global mood_df
    if request.method == "POST":
        mood_text = request.form.get("mood_text", "").strip()
        if not mood_text:
            return render_template("mood.html", error="Please write how you feel.")
        sentiment = analyze_sentiment(mood_text)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mood_df = pd.concat([mood_df, pd.DataFrame([[date, mood_text, sentiment]], columns=mood_df.columns)], ignore_index=True)
        mood_df.to_csv(CSV_FILE, index=False)
        activities = recommend_activity(sentiment)
        return render_template("mood.html", sentiment=sentiment, activities=activities, mood_text=mood_text)
    return render_template("mood.html")

@app.route("/dashboard")
def dashboard():
    global mood_df
    # prepare data for client-side Chart.js
    if mood_df.empty:
        data_json = json.dumps([])
    else:
        # map sentiment to numbers for plotting
        def s2n(s):
            return 1 if s == "Positive" else (-1 if s == "Negative" else 0)
        data_points = [
            {"date": row["date"], "sentiment": row["sentiment"], "value": s2n(row["sentiment"])}
            for _, row in mood_df.iterrows()
        ]
        data_json = json.dumps(data_points)
    return render_template("dashboard.html", mood_data=data_json)

if __name__ == "__main__":
    # Use host='0.0.0.0' if you plan to expose via ngrok
    app.run(debug=True, host="127.0.0.1", port=5000)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
