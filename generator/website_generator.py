import os
import json
import re
from groq import Groq
from utils.save_files import save_generated_files
from config import Config

# Initialize the Groq client
client = Groq(api_key=Config.GROQ_API_KEY)

def clean_ai_output(code_string):
    """
    Cleans up common formatting errors LLMs make in JSON mode, 
    such as double-escaped newlines and markdown wrappers.
    """
    if not code_string:
        return ""
        
    # 1. Fix double-escaped newlines and tabs
    cleaned = code_string.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
    
    # 2. Remove markdown code block wrappers if the AI accidentally included them
    cleaned = re.sub(r'^```[a-z]*\n', '', cleaned, flags=re.MULTILINE|re.IGNORECASE)
    cleaned = re.sub(r'\n```$', '', cleaned, flags=re.MULTILINE)
    
    # 3. Strip dangling backticks just in case
    cleaned = cleaned.strip("`").strip()
    
    return cleaned

def generate_website(prompt):
    """
    Takes a user prompt, asks the AI to generate a website, 
    and saves the resulting HTML, CSS, and JS files.
    """
    system_prompt = """
    You are an expert Senior Full-Stack Developer and UI/UX Designer.
    Generate a complete, modern, responsive website based on the user's prompt.
    Return ONLY a JSON object with the exact following structure:
    {
      "html_pages": {
        "index.html": "<massive, long-scrolling home page with ALL sections>",
        "about.html": "<dedicated about page>",
        "contact.html": "<dedicated contact page>"
      },
      "css": "<the complete shared style.css code>",
      "js": "<the complete shared script.js code>"
    }
    
    CRITICAL RULES:
    1. HYBRID ARCHITECTURE (LONG-SCROLL + MULTI-PAGE):
       - Do NOT make the website small. 'index.html' MUST be a comprehensive, long-scrolling landing page. It must contain MULTIPLE full-height sections stacked vertically (e.g., <section id="home">, <section id="about">, <section id="services">, <section id="contact">). It should feel like a massive, premium website.
       - You MUST ALSO generate separate, dedicated files for these sections (e.g., "about.html", "contact.html") inside the 'html_pages' object.
       - The navigation menu should use anchor links (href="#about") on the index page to jump to sections, and absolute links (href="index.html") on the sub-pages to go back.
       
    2. WRITE PURE HTML. Do NOT use markdown lists (like * Home) inside the HTML. Use actual <ul>, <li>, and <nav> tags.
    3. Do NOT wrap the code in markdown blocks (e.g., ```html). Just output the raw code string.
    4. NEVER use local image paths. Use Lorem Flickr. Example: <img src="[https://loremflickr.com/800/600/nature](https://loremflickr.com/800/600/nature)" alt="Nature">
    
    5. CRITICAL RULE FOR FORMS: If you create a contact form or newsletter signup on any page, you MUST make it functionally ready for Web3Forms. 
       - Set the form tag exactly like this: <form action="[https://api.web3forms.com/submit](https://api.web3forms.com/submit)" method="POST">
       - The very first element inside the form MUST be: <input type="hidden" name="access_key" value="YOUR_PUBLIC_API_KEY_HERE">
       - Ensure all visible inputs have a 'name' attribute (e.g., name="name", name="email", name="message").
    """

    try:
        # Call the LLM
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a massive, comprehensive website for: {prompt}"}
            ],
            response_format={ "type": "json_object" }, 
            max_tokens=6500 # Slightly increased to allow for the massive index.html file
        )

        # Extract the content
        generated_content = response.choices[0].message.content
        website_data = json.loads(generated_content)

        # 1. Extract Pages
        html_pages = website_data.get("html_pages", {})
        
        # Fallback
        if not html_pages and "html" in website_data: 
            html_pages = {"index.html": website_data["html"]}
            
        # 2. Clean all pages and inject Web3Forms Key
        for filename, content in html_pages.items():
            cleaned_html = clean_ai_output(content)
            
            if hasattr(Config, 'WEB3FORMS_KEY') and Config.WEB3FORMS_KEY:
                cleaned_html = cleaned_html.replace("YOUR_PUBLIC_API_KEY_HERE", Config.WEB3FORMS_KEY)
                
            html_pages[filename] = cleaned_html
            
        # 3. Clean CSS and JS
        css_code = clean_ai_output(website_data.get("css", ""))
        js_code = clean_ai_output(website_data.get("js", ""))

        # 4. Save all files
        save_paths = save_generated_files(html_pages, css_code, js_code)

        return {
            "status": "success",
            "paths": save_paths
        }

    except Exception as e:
        print(f"Error generating website: {e}")
        raise e