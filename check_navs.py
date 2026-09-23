import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

navs = set(re.findall(r'data-i18n="(nav\.[^"]+)"', content))
print("Navs in base.html:", navs)

with open('static/js/translations.js', 'r', encoding='utf-8') as f:
    js = f.read()

missing = [n for n in navs if n not in js]
print("Missing in translations.js:", missing)
