import os
import re

tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

# Strip out all lines containing 'nav.' except 'nav.home'
lines = tcontent.split('\n')
clean_lines = []
for line in lines:
    if 'nav.' in line and 'nav.home' not in line:
        continue
    clean_lines.append(line)

tcontent = '\n'.join(clean_lines)

# Now, we know there are two blocks: en and hi.
# We can find the 'general.date' line in each block.
en_navs = '''    'nav.dashboard': 'Dashboard',
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
    'nav.logistics_dashboard': 'Dashboard',
    'nav.logistics_available': 'Available Deliveries',
    'nav.logistics_my': 'My Deliveries',
    'nav.collapse_sidebar': 'Collapse Sidebar',
    'nav.expand_sidebar': 'Expand Sidebar',
'''

hi_navs = '''    'nav.dashboard': 'डैशबोर्ड',
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
    'nav.logistics_dashboard': 'डैशबोर्ड',
    'nav.logistics_available': 'उपलब्ध डिलीवरी',
    'nav.logistics_my': 'मेरी डिलीवरी',
    'nav.collapse_sidebar': 'साइडबार छोटा करें',
    'nav.expand_sidebar': 'साइडबार बड़ा करें',
'''

parts = re.split(r"('general\.date': '[^']+',)", tcontent)
if len(parts) == 5:
    # parts[0]
    # parts[1] (en general.date)
    # parts[2]
    # parts[3] (hi general.date)
    # parts[4]
    new_content = parts[0] + parts[1] + '\n' + en_navs + parts[2] + parts[3] + '\n' + hi_navs + parts[4]
    with open(tf, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully rebuilt nav translations.")
else:
    print("Could not split properly, found", len(parts), "parts")

