import os

filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the environment variable override BEFORE import google.generativeai
if 'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION' not in content:
    content = content.replace(
        'import google.generativeai as genai',
        'import os\nos.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"\nimport google.generativeai as genai'
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Patched app.py")
