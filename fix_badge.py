import os
filepath = 'templates/index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Revolutionizing Indian Agriculture", "<span data-i18n='hero.badge'>Revolutionizing Indian Agriculture</span>")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

en_adds = "'hero.badge': 'Revolutionizing Indian Agriculture',\n"
hi_adds = "'hero.badge': 'भारतीय कृषि में क्रांति',\n"

tcontent = tcontent.replace("'general.date': 'Date',", "'general.date': 'Date',\n" + en_adds)
tcontent = tcontent.replace("'general.date': 'दिनांक',", "'general.date': 'दिनांक',\n" + hi_adds)

with open(tf, 'w', encoding='utf-8') as f:
    f.write(tcontent)

print('Updated translations and index.html for badge')
