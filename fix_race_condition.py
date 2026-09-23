import os

filepath = 'templates/base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import json
with open('static/data/crop_images.json', 'r', encoding='utf-8') as f:
    crop_images_json = f.read()

# Replace the fetch logic with inline object
old_script = '''    window.cropImages = {};
    fetch('/static/data/crop_images.json')
        .then(res => res.json())
        .then(data => {
            window.cropImages = data;
        })
        .catch(err => console.error('Failed to load crop images map', err));'''

new_script = f'    window.cropImages = {crop_images_json};'

content = content.replace(old_script, new_script)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Inlined cropImages into base.html")
