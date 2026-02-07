from flask import Flask, request, jsonify, render_template
from your_card_code import validate_card, generate_card

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json() or {}
    return jsonify(validate_card(data.get("number", "")))

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    card = generate_card(data.get("cardType", ""))
    return jsonify({"card": card})

if __name__ == "__main__":
    app.run(debug=True)
