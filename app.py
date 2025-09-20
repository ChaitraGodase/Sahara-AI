from flask import Flask, render_template, request
from chat_utils import generate_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form["message"]
        bot_response = generate_response(user_message)
        return render_template("chat.html", user_message=user_message, bot_response=bot_response)
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True)
