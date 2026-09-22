import os

replacements = {
    'https://images.unsplash.com/photo-1595841696677-6489ff3f8cd1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80': '/static/images/hero-farmer.jpg',
    'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=500&q=80': '/static/images/market-bg.jpg',
    'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=400': '/static/images/default-crop.jpg',
    'https://images.unsplash.com/photo-1599940824399-b87987ceb72a?w=400&q=80': '/static/images/fallback-crop.jpg'
}

files_to_check = [
    'app.py',
    'templates/index.html',
    'templates/buyer/dashboard.html',
    'templates/farmer/listings.html',
    'templates/buyer/saved.html',
    'static/js/main.js',
    'static/js/marketplace.js'
]

for filepath in files_to_check:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig = content
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    if orig != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Patched {filepath}')
