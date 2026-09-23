import os

files_to_patch = {
    'templates/buyer/my_requests.html': [
        ('Farmer Contact (Revealed)', '<span data-i18n="market.contact_revealed">Farmer Contact (Revealed)</span>'),
        ('Farmer contact revealed after acceptance.', '<span data-i18n="market.contact_reveal_msg">Farmer contact revealed after acceptance.</span>')
    ],
    'templates/farmer/requests.html': [
        ('Contact revealed on accept', '<span data-i18n="market.contact_reveal_short">Contact revealed on accept</span>')
    ]
}

for filepath, replacements in files_to_patch.items():
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    for old, new in replacements:
        if 'data-i18n' in old: continue
        content = content.replace(old, new)
    if orig != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {filepath}")
