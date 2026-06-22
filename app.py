from flask import Flask, render_template, request, jsonify
from generator.website_generator import generate_website

# Create Flask app
app = Flask(__name__)


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# Website generation API
@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        # Get JSON data
        data = request.get_json()

        # Validate request
        if not data or "prompt" not in data:
            return jsonify({
                "success": False,
                "error": "Prompt is required."
            }), 400

        prompt = data["prompt"]

        # Generate website
        generation_result = generate_website(prompt)

        return jsonify({
            "success": True,
            "message": "Website generated successfully!",
            "preview_url": "/static/generated/latest/index.html",
            "files": generation_result
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Health check endpoint (recommended for Render)
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# Local development only
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
