import os
import re
from config import Config


def save_generated_files(html_pages_dict, css, js):
    """
    Inject CSS and JS into every HTML page and save them
    under static/generated/latest.
    """

    folder = os.path.join(Config.GENERATED_DIR, "latest")
    os.makedirs(folder, exist_ok=True)

    style_tag = (
        f"<style>\n{css}\n</style>"
        if css and css.strip()
        else ""
    )

    script_tag = (
        f"<script>\n{js}\n</script>"
        if js and js.strip()
        else ""
    )

    saved_pages = {}

    for filename, html_content in html_pages_dict.items():

        # Remove old references
        html_content = re.sub(
            r'<link[^>]+style\.css[^>]*>',
            '',
            html_content,
            flags=re.IGNORECASE
        )

        html_content = re.sub(
            r'<script[^>]+script\.js[^>]*></script>',
            '',
            html_content,
            flags=re.IGNORECASE
        )

        # Inject CSS
        if style_tag:
            if re.search(r'</head>', html_content, re.IGNORECASE):
                html_content = re.sub(
                    r'</head>',
                    f'{style_tag}\n</head>',
                    html_content,
                    flags=re.IGNORECASE
                )
            else:
                html_content = style_tag + html_content

        # Inject JS
        if script_tag:
            if re.search(r'</body>', html_content, re.IGNORECASE):
                html_content = re.sub(
                    r'</body>',
                    f'{script_tag}\n</body>',
                    html_content,
                    flags=re.IGNORECASE
                )
            else:
                html_content += script_tag

        # Save page
        file_path = os.path.join(folder, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Store URL path
        saved_pages[filename] = f"/static/generated/latest/{filename}"

    # Remove legacy files
    for old_file in ("style.css", "script.js"):
        old_path = os.path.join(folder, old_file)
        if os.path.exists(old_path):
            os.remove(old_path)

    return {
        "html": saved_pages.get(
            "index.html",
            "/static/generated/latest/index.html"
        ),
        "pages": saved_pages
    }
