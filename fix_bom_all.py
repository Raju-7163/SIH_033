import os

for root, dirs, files in os.walk('.'):
    if '.git' in root: continue
    for file in files:
        if file.endswith(('.html', '.js', '.json', '.py', '.css')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if '\ufeff' in content:
                    content = content.replace('\ufeff', '')
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Removed BOM from {filepath}")
            except Exception:
                pass
