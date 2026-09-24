import os
import re

directories = ['.', 'templates', 'templates/auth', 'templates/buyer', 'templates/farmer', 'templates/logistics', 'static/js', 'static/css']
extensions = ['.py', '.html', '.js', '.css', '.env', '.env.example', '.md']

replacements = [
    ("FarmLink AI", "FarmLink AI"),
    ("farmlinkai", "farmlinkai"),
    ("FARMLINKAI", "FARMLINKAI")
]

count = 0
for d in directories:
    for root, dirs, files in os.walk(d):
        if 'venv' in root or '.git' in root or 'node_modules' in root:
            continue
        for f in files:
            if not any(f.endswith(ext) for ext in extensions):
                continue
            
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                continue
                
            orig_content = content
            
            # Special case for CSS class
            content = content.replace("navbar-farmlinkai", "navbar-farmlinkai")
            
            for old, new in replacements:
                content = content.replace(old, new)
                
            if content != orig_content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated {filepath}")
                count += 1

print(f"Total files updated: {count}")
