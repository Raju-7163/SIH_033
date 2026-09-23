import json

with open('new_urls.json', 'r') as f:
    results = json.load(f)

with open('static/data/crop_images.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=4)

filepath = 'templates/base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re
old_script = re.search(r'window\.cropImages\s*=\s*\{.*?\};', content, flags=re.DOTALL)
if old_script:
    new_script = f'window.cropImages = {json.dumps(results)};'
    content = content.replace(old_script.group(0), new_script)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Updated base.html")
