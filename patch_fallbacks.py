import os
import re

files_to_patch = {
    'templates/farmer/listings.html': [
        (r'onerror="this\.src=\'https://images\.unsplash\.com/[^\']+\'"', 'onerror="window.handleImageFallback(this, \'{{ listing.crop_name }}\')"'),
        (r'onerror="this\.src=\'/static/images/[^\']+\'"', 'onerror="window.handleImageFallback(this, \'{{ listing.crop_name }}\')"')
    ],
    'templates/buyer/saved.html': [
        (r'onerror="this\.src=\'https://images\.unsplash\.com/[^\']+\'"', 'onerror="window.handleImageFallback(this, \'{{ listing.crop_name }}\')"'),
        (r'onerror="this\.src=\'/static/images/[^\']+\'"', 'onerror="window.handleImageFallback(this, \'{{ listing.crop_name }}\')"')
    ],
    'static/js/main.js': [
        (r'onerror="this\.src=\'https://images\.unsplash\.com/[^\']+\'"', 'onerror="window.handleImageFallback(this, \'\')"'),
        (r'onerror="this\.src=\'/static/images/[^\']+\'"', 'onerror="window.handleImageFallback(this, \'\')"')
    ],
    'static/js/marketplace.js': [
        (r'onerror="this\.src=\'https://images\.unsplash\.com/[^\']+\'"', 'onerror="window.handleImageFallback(this, \'\')"'),
        (r'onerror="this\.src=\'/static/images/[^\']+\'"', 'onerror="window.handleImageFallback(this, \'\')"')
    ]
}

for filepath, patterns in files_to_patch.items():
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    for old_regex, new_text in patterns:
        content = re.sub(old_regex, new_text, content)
    if orig != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {filepath}")
