import os
import json

filepath = 'static/js/translations.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# I will just insert these keys before the closing brace of 'en' and 'hi' dictionaries
# Instead of parsing js, I'll use simple string replacement since I know the structure

en_additions = """
    'dash.requests_sent': 'Requests Sent',
    'dash.saved_listings': 'Saved Listings',
    'dash.active_deals': 'Active Deals',
    'dash.recent_requests': 'Recent Requests',
    'dash.view_all': 'View All',
    'dash.manage_deals': 'Manage deals',
    'dash.discover_fresh_produce': 'Discover Fresh Produce',
    'dash.discover_desc': 'Connect directly with farmers across India for the best quality and prices.',
    'market.discover': 'Discover Marketplace',
    'market.state_label': 'State',
    'market.all_states': 'All States',
    'market.max_price': 'Max Price (₹)',
    'market.need_more': 'Need more quantity?',
    'market.combine_desc': 'No single farmer has enough — combine listings to reach your goal.',
    'market.no_listings': 'No listings found',
    'market.try_adjusting': 'Try adjusting your filters or search criteria.',
    'market.filters': 'Filters',
    'market.total_price': 'Total Price',
"""

hi_additions = """
    'dash.requests_sent': 'भेजे गए अनुरोध',
    'dash.saved_listings': 'सहेजी गई लिस्टिंग',
    'dash.active_deals': 'सक्रिय सौदे',
    'dash.recent_requests': 'हाल के अनुरोध',
    'dash.view_all': 'सभी देखें',
    'dash.manage_deals': 'सौदे प्रबंधित करें',
    'dash.discover_fresh_produce': 'ताज़ा उपज खोजें',
    'dash.discover_desc': 'सर्वोत्तम गुणवत्ता और कीमतों के लिए पूरे भारत में किसानों से सीधे जुड़ें।',
    'market.discover': 'बाज़ार खोजें',
    'market.state_label': 'राज्य',
    'market.all_states': 'सभी राज्य',
    'market.max_price': 'अधिकतम मूल्य (₹)',
    'market.need_more': 'अधिक मात्रा चाहिए?',
    'market.combine_desc': 'किसी एक किसान के पास पर्याप्त मात्रा नहीं है — लक्ष्य तक पहुँचने के लिए लिस्टिंग मिलाएं।',
    'market.no_listings': 'कोई लिस्टिंग नहीं मिली',
    'market.try_adjusting': 'अपने फ़िल्टर या खोज मानदंड को समायोजित करने का प्रयास करें।',
    'market.filters': 'फ़िल्टर',
    'market.total_price': 'कुल मूल्य',
"""

content = content.replace("'general.date': 'Date',", "'general.date': 'Date',\n" + en_additions)
content = content.replace("'general.date': 'दिनांक',", "'general.date': 'दिनांक',\n" + hi_additions)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated translations.js')
