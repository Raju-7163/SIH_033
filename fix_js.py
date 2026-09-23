import os

filepath = 'static/js/main.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('onerror="window.handleImageFallback(this, \'\')"', 'onerror="window.handleImageFallback(this, \'\')"')
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

filepath = 'static/js/marketplace.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('onerror="window.handleImageFallback(this, \'\')"', 'onerror="window.handleImageFallback(this, \'\')"')
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
