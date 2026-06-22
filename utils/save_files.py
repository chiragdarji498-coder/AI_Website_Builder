import os
import re
from config import Config

def save_generated_files(html_pages_dict, css, js):
    """
    Takes a dictionary of HTML pages, injects the shared CSS and JS into 
    every single page, and saves them to the static/generated directory.
    """
    # Use the Config path to ensure cross-platform compatibility
    folder = os.path.join(Config.GENERATED_DIR, 'latest')
    os.makedirs(folder, exist_ok=True)
    
    # We will track the main index file to return to the frontend
    main_file_path = "/static/generated/latest/index.html"

    # Prepare CSS and JS tags once
    style_tag = f"<style>\n{css}\n</style>" if css and css.strip() else ""
    script_tag = f"<script>\n{js}\n</script>" if js and js.strip() else ""

    # Loop through every page the AI generated (index.html, about.html, etc.)
    for filename, html_content in html_pages_dict.items():
        
        # Remove old references to external style.css and script.js if they are present
        html_content = re.sub(r'<link[^>]+style\.css[^>]*>', '', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<script[^>]+script\.js[^>]*></script>', '', html_content, flags=re.IGNORECASE)

        # Inject CSS into the <head> section of THIS page
        if style_tag:
            if "</head>" in html_content.lower():
                html_content = re.sub(r'</head>', f'{style_tag}\n</head>', html_content, flags=re.IGNORECASE)
            else:
                html_content = style_tag + html_content

        # Inject JS into the end of the <body> section of THIS page
        if script_tag:
            if "</body>" in html_content.lower():
                html_content = re.sub(r'</body>', f'{script_tag}\n</body>', html_content, flags=re.IGNORECASE)
            else:
                html_content = html_content + script_tag

        # Save the consolidated file (e.g., folder/about.html)
        file_path = os.path.join(folder, filename)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(html_content)

    # Clean up separate standalone files if they exist from older generations
    for old_file in ["style.css", "script.js"]:
        filepath = os.path.join(folder, old_file)
        if os.path.exists(filepath):
            os.remove(filepath)

    # Return the index path so the iframe knows where to start looking
    return {
        "html": main_file_path
    }