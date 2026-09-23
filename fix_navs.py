import os

tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

en_adds = '''
    'nav.dashboard': 'Dashboard',
    'nav.my_listings': 'My Listings',
    'nav.add_listing': 'Add Listing',
    'nav.market_prices': 'Market Prices',
    'nav.requests': 'Requests',
    'nav.profile': 'Profile',
    'nav.logout': 'Logout',
    'nav.marketplace': 'Browse Marketplace',
    'nav.my_requests': 'My Requests',
    'nav.saved': 'Saved',
    'nav.cart': 'My Cart',
'''

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

if "'nav.my_listings'" not in tcontent:
    tcontent = tcontent.replace("'general.date': 'Date',", "'general.date': 'Date',\n" + en_adds)
    tcontent = tcontent.replace("'general.date': 'दिनांक',", "'general.date': 'दिनांक',\n" + hi_adds)
    with open(tf, 'w', encoding='utf-8') as f:
        f.write(tcontent)
    print("Added nav translations")
