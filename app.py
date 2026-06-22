from flask import Flask, render_template, request, jsonify
from generator.website_generator import generate_website
import os
from dotenv import load_dotenv

# Load environment variables (API keys, etc.)
load_dotenv()

app = Flask(__name__)

# Serve the main landing page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to handle the generation request from frontend
@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    
    if not data or 'prompt' not in data:
        return jsonify({"error": "Prompt is required."}), 400
        
    prompt = data['prompt']
    
    try:
        # Call your AI generation logic
        # This function will handle the LLM interaction and file saving
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

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)