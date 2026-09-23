import os
import re

# Add missing translations to translations.js
tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

en_adds = '''
    'auth.aadhaar_label': 'Aadhaar Number',
    'auth.aadhaar_kyc': '(for KYC verification)',
    'auth.aadhaar_placeholder': 'Enter 12-digit Aadhaar number',
    'auth.aadhaar_help': 'Only the last 4 digits are stored. Your full number is never saved.',
    'auth.aadhaar_invalid': 'Please enter a valid 12-digit Aadhaar number.',
    'logistics.dash_title': 'Logistics Dashboard',
    'logistics.welcome_back': 'Welcome back,',
    'logistics.view_available': 'View Available Deliveries',
    'logistics.available_stat': 'Available',
    'logistics.my_deliveries_stat': 'My Deliveries',
    'logistics.in_transit_stat': 'In Transit',
    'logistics.delivered_stat': 'Delivered',
    'logistics.available_title': 'Available Deliveries',
    'logistics.available_desc': 'Browse paid orders waiting for a logistics partner. Accept deliveries to add them to your queue.',
    'logistics.browse_btn': 'Browse',
    'logistics.my_deliveries_title': 'My Deliveries',
    'logistics.my_deliveries_desc': 'Track and update the status of deliveries you have accepted. Update from Picked Up → In Transit → Delivered.',
    'logistics.view_mine_btn': 'View Mine',
    'logistics.accept': 'Accept Delivery',
    'logistics.update_status': 'Update Status',
    'logistics.picked_up': 'Picked Up',
    'logistics.in_transit': 'In Transit',
    'logistics.delivered': 'Delivered',
    'logistics.no_available': 'No available deliveries right now.',
    'logistics.no_mine': 'You have not accepted any deliveries yet.',
    'market.buy_now': 'Buy Now',
    'market.add_to_cart': 'Add to Cart',
    'market.combine_listings': 'Combine Listings',
    'market.target_qty': 'Target Quantity',
    'market.total_est_cost': 'Total Estimated Cost',
    'market.selected_farmers': 'Selected Farmers',
    'market.contact_reveal': 'Farmer contact info revealed after acceptance',
    'market.checkout': 'Checkout',
    'market.payment': 'Payment',
    'nav.collapse_sidebar': 'Collapse Sidebar',
    'nav.expand_sidebar': 'Expand Sidebar',
    'nav.logistics_dashboard': 'Dashboard',
    'nav.logistics_available': 'Available Deliveries',
    'nav.logistics_my': 'My Deliveries',
    'market.price_per_kg': 'Price / kg',
    'market.price_per_quintal': 'Price / Quintal',
    'market.price_per_tonne': 'Price / Tonne',
'''

hi_adds = '''
    'auth.aadhaar_label': 'आधार संख्या',
    'auth.aadhaar_kyc': '(KYC सत्यापन के लिए)',
    'auth.aadhaar_placeholder': '12 अंकों का आधार नंबर दर्ज करें',
    'auth.aadhaar_help': 'केवल अंतिम 4 अंक संग्रहीत किए जाते हैं। आपका पूरा नंबर कभी सहेजा नहीं जाता है।',
    'auth.aadhaar_invalid': 'कृपया एक मान्य 12-अंकीय आधार संख्या दर्ज करें।',
    'logistics.dash_title': 'लॉजिस्टिक्स डैशबोर्ड',
    'logistics.welcome_back': 'वापसी पर स्वागत है,',
    'logistics.view_available': 'उपलब्ध डिलीवरी देखें',
    'logistics.available_stat': 'उपलब्ध',
    'logistics.my_deliveries_stat': 'मेरी डिलीवरी',
    'logistics.in_transit_stat': 'रास्ते में',
    'logistics.delivered_stat': 'पहुंचा दिया',
    'logistics.available_title': 'उपलब्ध डिलीवरी',
    'logistics.available_desc': 'लॉजिस्टिक्स पार्टनर की प्रतीक्षा कर रहे सशुल्क ऑर्डर ब्राउज़ करें। उन्हें अपनी कतार में जोड़ने के लिए डिलीवरी स्वीकार करें।',
    'logistics.browse_btn': 'ब्राउज़ करें',
    'logistics.my_deliveries_title': 'मेरी डिलीवरी',
    'logistics.my_deliveries_desc': 'आपके द्वारा स्वीकार की गई डिलीवरी की स्थिति को ट्रैक और अपडेट करें। पिकअप → रास्ते में → डिलीवर से अपडेट करें।',
    'logistics.view_mine_btn': 'मेरा देखें',
    'logistics.accept': 'डिलीवरी स्वीकार करें',
    'logistics.update_status': 'स्थिति अपडेट करें',
    'logistics.picked_up': 'पिकअप हो गया',
    'logistics.in_transit': 'रास्ते में',
    'logistics.delivered': 'पहुंचा दिया',
    'logistics.no_available': 'अभी कोई डिलीवरी उपलब्ध नहीं है।',
    'logistics.no_mine': 'आपने अभी तक कोई डिलीवरी स्वीकार नहीं की है।',
    'market.buy_now': 'अभी खरीदें',
    'market.add_to_cart': 'कार्ट में डालें',
    'market.combine_listings': 'लिस्टिंग मिलाएं',
    'market.target_qty': 'लक्ष्य मात्रा',
    'market.total_est_cost': 'कुल अनुमानित लागत',
    'market.selected_farmers': 'चयनित किसान',
    'market.contact_reveal': 'स्वीकृति के बाद किसान संपर्क जानकारी का पता चला',
    'market.checkout': 'चेकआउट',
    'market.payment': 'भुगतान',
    'nav.collapse_sidebar': 'साइडबार छोटा करें',
    'nav.expand_sidebar': 'साइडबार बड़ा करें',
    'nav.logistics_dashboard': 'डैशबोर्ड',
    'nav.logistics_available': 'उपलब्ध डिलीवरी',
    'nav.logistics_my': 'मेरी डिलीवरी',
    'market.price_per_kg': 'मूल्य / किलो',
    'market.price_per_quintal': 'मूल्य / क्विंटल',
    'market.price_per_tonne': 'मूल्य / टन',
'''

if "'auth.aadhaar_label'" not in tcontent:
    tcontent = tcontent.replace("'general.date': 'Date',", "'general.date': 'Date',\n" + en_adds)
    tcontent = tcontent.replace("'general.date': 'दिनांक',", "'general.date': 'दिनांक',\n" + hi_adds)
    with open(tf, 'w', encoding='utf-8') as f:
        f.write(tcontent)
    print("Updated translations.js")

