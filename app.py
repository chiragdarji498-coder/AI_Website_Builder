from flask import Flask, render_template, request, jsonify
from generator.website_generator import generate_website
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# Website generation endpoint
@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()

    if not data or "prompt" not in data:
        return jsonify({
            "success": False,
            "error": "Prompt is required."
        }), 400

    prompt = data["prompt"]

    try:
        generation_result = generate_website(prompt)

        return jsonify({
            "success": True,
            "message": "Website generated successfully!",
            "preview_url": "/generated/latest/index.html",
            "files": generation_result
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Only used for local development
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
