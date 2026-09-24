import os

filepath = 'templates/index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Join <strong class=\"text-white\">2,400+</strong> farmers already earning more", "<span data-i18n='hero.join_farmers'>Join <strong class=\"text-white\">2,400+</strong> farmers already earning more</span>")
content = content.replace("+35% Profit", "<span data-i18n='hero.profit_increase'>+35% Profit</span>")
content = content.replace("Average farmer increase", "<span data-i18n='hero.avg_increase'>Average farmer increase</span>")
content = content.replace("© 2024 FarmLink AI. All rights reserved.", "<span data-i18n='footer.copyright'>© 2024 FarmLink AI. All rights reserved.</span>")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

en_adds = """
    'hero.join_farmers': 'Join <strong class=\"text-white\">2,400+</strong> farmers already earning more',
    'hero.profit_increase': '+35% Profit',
    'hero.avg_increase': 'Average farmer increase',
    'footer.copyright': '© 2024 FarmLink AI. All rights reserved.',
"""

hi_adds = """
    'hero.join_farmers': 'अधिक कमाई करने वाले <strong class=\"text-white\">2,400+</strong> किसानों से जुड़ें',
    'hero.profit_increase': '+35% लाभ',
    'hero.avg_increase': 'औसत किसान वृद्धि',
    'footer.copyright': '© 2024 FarmLink AI. सर्वाधिकार सुरक्षित।',
"""

tcontent = tcontent.replace("'general.date': 'Date',", "'general.date': 'Date',\n" + en_adds)
tcontent = tcontent.replace("'general.date': 'दिनांक',", "'general.date': 'दिनांक',\n" + hi_adds)

with open(tf, 'w', encoding='utf-8') as f:
    f.write(tcontent)

print('Updated translations and index.html')
