import json
import re
from groq import Groq
from utils.save_files import save_generated_files
from config import Config

# Initialize Groq client
client = Groq(api_key=Config.GROQ_API_KEY)


def clean_ai_output(code_string):
    """
    Cleans up common formatting issues in AI output.
    """
    if not code_string:
        return ""

    cleaned = (
        code_string.replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace('\\"', '"')
    )

    cleaned = re.sub(
        r"^```[a-z]*\n",
        "",
        cleaned,
        flags=re.MULTILINE | re.IGNORECASE
    )

    cleaned = re.sub(
        r"\n```$",
        "",
        cleaned,
        flags=re.MULTILINE
    )

    return cleaned.strip("`").strip()


def generate_website(prompt):
    """
    Generate a website from a user prompt.
    """

    system_prompt = """
    You are an expert Senior Full-Stack Developer and UI/UX Designer.
    Generate a complete, modern, responsive website based on the user's prompt.

    Return ONLY a JSON object with this structure:

    {
      "html_pages": {
        "index.html": "...",
        "about.html": "...",
        "contact.html": "..."
      },
      "css": "...",
      "js": "..."
    }
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
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

        # Get HTML pages
        html_pages = website_data.get("html_pages", {})

        # Fallback
        if not html_pages and "html" in website_data:
            html_pages = {
                "index.html": website_data["html"]
            }

        # Clean HTML pages
        for filename, content in html_pages.items():

            cleaned_html = clean_ai_output(content)

            if Config.WEB3FORMS_KEY:
                cleaned_html = cleaned_html.replace(
                    "YOUR_PUBLIC_API_KEY_HERE",
                    Config.WEB3FORMS_KEY
                )

            html_pages[filename] = cleaned_html

        # Clean CSS and JS
        css_code = clean_ai_output(
            website_data.get("css", "")
        )

        js_code = clean_ai_output(
            website_data.get("js", "")
        )

        # Save generated files
        save_paths = save_generated_files(
            html_pages,
            css_code,
            js_code
        )

        return {
            "status": "success",
            "paths": save_paths
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
