import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_URL = "https://fast-flux-demo.replicate.workers.dev/api/generate-image"

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "ApI RuNnInG SuCeSsFuLlY! MaDe By @NgYT777Gg",
        "usage": "/generate?q=your_text"
    })

@app.route("/generate", methods=["GET"])
def generate():
    text = request.args.get("q")

    if not text:
        return jsonify({"error": "Missing parameter: q"}), 400

    try:
        req_url = f"{BASE_URL}?text={text}"
        r = requests.get(req_url)

        return jsonify({
            "status": "success",
            "input_text": text,
            "api_response": r.json()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
