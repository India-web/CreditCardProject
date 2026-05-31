from flask import Flask, request, jsonify, render_template
from credit_card_project import validate_card, generate_card, CARD_TABLE
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Pass all card types to template
    card_types = sorted(set([card[0] for card in CARD_TABLE]))
    return render_template("index.html", card_types=card_types)

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json() or {}
    number = data.get("number", "").replace(" ", "")  # Remove spaces
    
    if not number:
        return jsonify({"valid": False, "message": "Please enter a card number"})
    
    result = validate_card(number)
    
    if isinstance(result, dict):
        if result.get("valid"):
            return jsonify({
                "valid": True,
                "issuer": result.get("issuer"),
                "category": result.get("category")
            })
        else:
            return jsonify({"valid": False, "message": result.get("message", "Invalid card")})
    
    return jsonify({"valid": False, "message": "Invalid card number"})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    card_type = data.get("cardType", "")
    
    if not card_type:
        return jsonify({"card": None, "error": "No card type selected"})
    
    card = generate_card(card_type)
    
    if card:
        # Format card number with spaces
        formatted = ' '.join([card[i:i+4] for i in range(0, len(card), 4)])
        return jsonify({"card": card, "formatted": formatted})
    
    return jsonify({"card": None, "error": "Could not generate card"})

@app.route("/card_types", methods=["GET"])
def get_card_types():
    types = sorted(set([card[0] for card in CARD_TABLE]))
    return jsonify({"types": types})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
