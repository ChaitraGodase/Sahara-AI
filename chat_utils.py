from transformers import pipeline

# Load a small Hugging Face model
chatbot = pipeline("text-generation", model="distilgpt2")

def generate_response(user_message):
    # Simple rule-based replies
    if "stress" in user_message.lower():
        return "I'm sorry you're feeling stressed 💙 Try taking deep breaths or a short break."
    elif "sad" in user_message.lower():
        return "It's okay to feel sad sometimes 🌸 Talking about it can help. Want to share more?"
    elif "happy" in user_message.lower():
        return "That's amazing! 🎉 Keep doing what makes you feel happy!"
    
    # Fallback to AI model
    try:
        response = chatbot(user_message, max_length=60, num_return_sequences=1)
        return response[0]['generated_text']
    except:
        return "I'm here for you. Can you tell me more?"
