import os

filepath = 'config.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
if 'GEMINI_API_KEY' not in content:
    content += "\nGEMINI_API_KEY = os.getenv('GEMINI_API_KEY')\n"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

filepath_app = 'app.py'
with open(filepath_app, 'r', encoding='utf-8') as f:
    app_content = f.read()

app_content = app_content.replace('api_key = os.environ.get("GEMINI_API_KEY")', 'api_key = config.GEMINI_API_KEY')
with open(filepath_app, 'w', encoding='utf-8') as f:
    f.write(app_content)
