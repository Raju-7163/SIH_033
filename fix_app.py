filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('import os\nos.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"\nimport google.generativeai as genai', 'import google.generativeai as genai')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
