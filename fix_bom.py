import os

filepath = 'templates/base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\ufeff', '')
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed BOM from base.html")
