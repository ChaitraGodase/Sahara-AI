def recommend_activity(sentiment):
    if sentiment == "Negative":
        return [
            "Try 5 deep breaths (4-4-4).",
            "Take a 10-minute walk outside.",
            "Write 3 things you're grateful for."
        ]
    elif sentiment == "Neutral":
        return [
            "Try a 5-minute stretch.",
            "Listen to a calming song.",
            "Plan the next 30 minutes of your day."
        ]
    elif sentiment == "Positive":
        return [
            "Share your good mood with a friend!",
            "Keep a note of what made you happy today."
        ]
    return []
