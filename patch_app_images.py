import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add JSON import if not present
if 'import json' not in content:
    content = content.replace('import os', 'import os\nimport json')

# Load crop_images at top
top_code = '''
# Load crop images mapping
crop_images_map = {}
try:
    with open('static/data/crop_images.json', 'r', encoding='utf-8') as f:
        crop_images_map = json.load(f)
except Exception as e:
    print("Warning: Could not load crop_images.json", e)
'''
if 'crop_images_map = {}' not in content:
    content = content.replace('app = Flask(__name__)', top_code + '\napp = Flask(__name__)')

# Update farmer_add_listing
content = content.replace(
    'photo_url = "/static/images/default-crop.jpg"',
    'photo_url = crop_images_map.get(crop_name, "/static/images/no-image.svg")'
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
