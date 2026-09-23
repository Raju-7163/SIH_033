import os
import re

tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

hi_adds = '''
    'nav.dashboard': 'डैशबोर्ड',
    'nav.my_listings': 'मेरी लिस्टिंग',
    'nav.add_listing': 'लिस्टिंग जोड़ें',
    'nav.market_prices': 'बाज़ार भाव',
    'nav.requests': 'अनुरोध',
    'nav.profile': 'प्रोफ़ाइल',
    'nav.logout': 'लॉग आउट',
    'nav.marketplace': 'बाज़ार ब्राउज़ करें',
    'nav.my_requests': 'मेरे अनुरोध',
    'nav.saved': 'सहेजा गया',
    'nav.cart': 'मेरी कार्ट',
'''

if "'nav.my_listings': 'मेरी लिस्टिंग'" not in tcontent:
    # Find the hi: block and the last general item
    tcontent = re.sub(r"('general\.date': '[^']+',)", r"\1\n" + hi_adds, tcontent)
    with open(tf, 'w', encoding='utf-8') as f:
        f.write(tcontent)
    print("Added Hindi nav translations")
else:
    print("Already added")
