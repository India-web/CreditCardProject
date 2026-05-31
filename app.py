from flask import Flask, request, jsonify, render_template
from credit_card_project import validate_card, generate_card
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json() or {}
    number = data.get("number", "")

    result = validate_card(number)

    if isinstance(result, dict):
        return jsonify(result)

    return jsonify({"result": result})


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    card_type = data.get("cardType", "")

    card = generate_card(card_type)

    return jsonify({"card": card})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
