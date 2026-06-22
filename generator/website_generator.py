from flask import Flask, request, jsonify
import os
import json
import re
from groq import Groq
from utils.save_files import save_generated_files
from config import Config

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=Config.GROQ_API_KEY)


def clean_ai_output(code_string):
    if not code_string:
        return ""

    cleaned = (
        code_string.replace('\\n', '\n')
        .replace('\\t', '\t')
        .replace('\\"', '"')
    )

    cleaned = re.sub(
        r'^```[a-z]*\n',
        '',
        cleaned,
        flags=re.MULTILINE | re.IGNORECASE
    )
    cleaned = re.sub(r'\n```$', '', cleaned, flags=re.MULTILINE)

    return cleaned.strip("`").strip()


def generate_website(prompt):
    system_prompt = """
    You are an expert Senior Full-Stack Developer and UI/UX Designer.
    Generate a complete, modern, responsive website based on the user's prompt.
    Return ONLY a JSON object.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Create a massive, comprehensive website for: {prompt}"
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=6500
    )

    generated_content = response.choices[0].message.content
    website_data = json.loads(generated_content)

    html_pages = website_data.get("html_pages", {})

    if not html_pages and "html" in website_data:
        html_pages = {"index.html": website_data["html"]}

    for filename, content in html_pages.items():
        cleaned_html = clean_ai_output(content)

        if hasattr(Config, "WEB3FORMS_KEY") and Config.WEB3FORMS_KEY:
            cleaned_html = cleaned_html.replace(
                "YOUR_PUBLIC_API_KEY_HERE",
                Config.WEB3FORMS_KEY
            )

        html_pages[filename] = cleaned_html

    css_code = clean_ai_output(website_data.get("css", ""))
    js_code = clean_ai_output(website_data.get("js", ""))

    save_paths = save_generated_files(
        html_pages,
        css_code,
        js_code
    )

    return {
        "status": "success",
        "paths": save_paths
    }


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        result = generate_website(prompt)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
