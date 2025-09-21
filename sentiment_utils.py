# sentiment_utils.py
from textblob import TextBlob

def analyze_sentiment(text: str) -> str:
    try:
        polarity = TextBlob(text).sentiment.polarity
    except Exception:
        polarity = 0.0
    if polarity < -0.2:
        return "Negative"
    elif polarity > 0.2:
        return "Positive"
    else:
        return "Neutral"
