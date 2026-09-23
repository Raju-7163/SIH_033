import os

filepath = 'seed.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('photos.get(l["crop"], photos["Tomato"])', 'photos.get(l["crop"], "/static/images/no-image.svg")')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
