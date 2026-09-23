import os

files_to_patch = [
    'templates/auth/login.html',
    'templates/auth/signup.html',
    'templates/base.html',
    'templates/index.html',
    'static/js/translations.js'
]

for filepath in files_to_patch:
    if not os.path.exists(filepath):
        print(f'{filepath} not found.')
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace("2024 AgriConnect", "2026 AgriConnect")
    # Also replace just 2024 in case there's any other copyright string in Hindi
    new_content = new_content.replace("2024", "2026")
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Patched {filepath}')
