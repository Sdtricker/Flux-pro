import requests
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

BASE_URL = "https://fast-flux-demo.replicate.workers.dev/api/generate-image"

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API active",
        "usage": "/generate?q=your_text"
    })

@app.route("/generate", methods=["GET"])
def generate():
    text = request.args.get("q")

    if not text:
        return jsonify({"error": "Missing parameter: q"}), 400

    try:
        # Make request to replicate worker
        url = f"{BASE_URL}?text={text}"
        r = requests.get(url)

        # If it's NOT an image
        if "image" not in r.headers.get("Content-Type", ""):
            return jsonify({
                "error": "API did not return an image",
                "content_type": r.headers.get("Content-Type"),
                "raw": r.text
            }), 400

        # DIRECT DOWNLOAD RESPONSE
        return Response(
            r.content,
            mimetype="image/png",
            headers={
                "Content-Disposition": "attachment; filename=generated.png"
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
