import re
import random
from sentiment_utils import analyze_sentiment

PATTERN_RESPONSES = [
    (r"\bstress(ed)?\b", "I'm sorry you're feeling stressed. Small breaks and breathing exercises can help."),
    (r"\b(exam|exams|test|project)\b", "Exams are tough — break tasks into small steps and try the Pomodoro method."),
    (r"\b(sad|depress|lonely)\b", "I'm here for you. Do you want to talk about what's making you feel this way?"),
    (r"\banxious\b", "That sounds hard. Try grounding: 5 deep breaths, name 5 things you see."),
    (r"\bhelp\b", "If you're in immediate danger, please contact local emergency services or a helpline. I'm also here to listen."),
    (r"\b(hello|hi|hey)\b", "Hey! How are you feeling today?"),
    (r"\bthank(s| you)\b", "You're welcome — I'm glad I could help.")
]

FALLBACKS = [
    "I hear you. Tell me more about what's on your mind.",
    "Thanks for sharing — I'm listening. Can you say a bit more?",
    "That sounds important. What happened before you felt this way?"
]

def generate_response(user_input: str) -> str:
    text = user_input.lower()
    base = None
    for pattern, response in PATTERN_RESPONSES:
        if re.search(pattern, text):
            base = response
            break
    if base is None:
        base = random.choice(FALLBACKS)

    # add empathy based on sentiment
    try:
        sentiment = analyze_sentiment(user_input)
    except Exception:
        sentiment = "Neutral"

    if sentiment == "Negative":
        extra = " 💜 I sense you're feeling down. Try 3 deep breaths or take a short walk. If things feel unsafe, contact a helpline."
    elif sentiment == "Positive":
        extra = " 🌟 That's great to hear! Keep it up."
    else:
        extra = ""
    return base + extra
