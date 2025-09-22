import nltk

# ensure vader lexicon is available in the environment
def _ensure_vader():
    try:
        nltk.data.find("sentiment/vader_lexicon")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)

_ensure_vader()

from nltk.sentiment import SentimentIntensityAnalyzer

_sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> str:
    if not text or not text.strip():
        return "Neutral"
    score = _sia.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"
