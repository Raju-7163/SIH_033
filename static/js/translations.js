// Translation dictionary for English and Hindi
const translations = {
  en: {
    // Navbar
    'nav.home': 'Home',
    // Landing
    'hero.title': 'Farm Fresh, Direct to You',
    'hero.subtitle': 'Connecting farmers directly with buyers. No middlemen. Better prices for everyone.',
    'hero.cta_farmer': "I'm a Farmer",
    'hero.cta_buyer': "I'm a Buyer",
    'hero.stat_farmers': 'Farmers Onboarded',
    'hero.stat_volume': 'Trade Volume (₹)',
    'hero.stat_crops': 'Crop Varieties',
    'hero.stat_states': 'States Covered',
    // How it works
    'how.title': 'How AgriConnect Works',
    'how.step1_title': 'Farmer Lists Produce',
    'how.step1_desc': 'Farmers upload their harvest details, quantity, and asking price.',
    'how.step2_title': 'Buyer Discovers',
    'how.step2_desc': 'Buyers search, filter, and compare listings with live market prices.',
    'how.step3_title': 'Direct Deal',
    'how.step3_desc': 'Connect directly, negotiate, and transact — zero commission.',
    // Auth
    'auth.login': 'Login',
    'auth.signup': 'Sign Up',
    'auth.email': 'Email',
    'auth.password': 'Password',
    'auth.name': 'Full Name',
    'auth.phone': 'Phone Number',
    'auth.state': 'State',
    'auth.district': 'District',
    'auth.role_farmer': 'I am a Farmer',
    'auth.role_buyer': 'I am a Buyer',
    // Marketplace
    'market.title': 'Browse Marketplace',
    'market.search': 'Search crops...',
    'market.filter_state': 'Filter by State',
    'market.price_range': 'Price Range (₹/unit)',
    'market.send_interest': 'Send Interest',
    'market.vs_market': 'vs Market',
    'market.fair': 'Fair Price',
    'market.overpriced': 'Above Market',
    'market.map_view': 'Map View',
    'market.grid_view': 'Grid View',
    // Dashboard
    'dash.total_listings': 'Total Listings',
    'dash.requests_received': 'Requests Received',
    'dash.activity': 'Activity This Month',
    'dash.accept': 'Accept',
    'dash.reject': 'Reject',
    'dash.add_listing': 'Add New Listing',
    // General
    'general.loading': 'Loading...',
    'general.no_data': 'No data available',
    'general.success': 'Success!',
    'general.error': 'Something went wrong.',
    'general.submit': 'Submit',
    'general.cancel': 'Cancel',
    'general.save': 'Save Changes',
    'general.quantity': 'Quantity',
    'general.price': 'Price',
    'general.location': 'Location',
    'general.status': 'Status',
    'general.date': 'Date',
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
    'nav.logistics_dashboard': 'Dashboard',
    'nav.logistics_available': 'Available Deliveries',
    'nav.logistics_my': 'My Deliveries',
    'nav.collapse_sidebar': 'Collapse Sidebar',
    'nav.expand_sidebar': 'Expand Sidebar',






    'payment.title': 'Complete Payment',
    'payment.demo_desc': 'Demo Payment - No real transaction',
    'payment.method': 'Payment Method',
    'payment.upi': 'UPI ID or Card Number',
    'payment.demo_note': 'Any value accepted - this is a demo.',
    'payment.pay_btn': 'Pay',
    'payment.processing': 'Processing...',
    'payment.success': 'Payment Successful!',
    'payment.success_toast': 'Payment successful! Your order is confirmed.',
    'payment.retry': 'Retry Payment',
    'payment.network_error': 'Network error. Please try again.',
    'payment.failed': 'Payment failed. Try again.',
    'payment.deal_accepted': 'Deal accepted - contact the farmer to arrange payment and delivery.',
    'payment.pay_now': 'Pay',
    'market.send_req_btn': 'Send Request',
    'market.confirm_purchase': 'Confirm Purchase',
    'market.pooled_warning': 'We couldn\'t find enough active listings to fully cover your requested quantity. Showing the best available combination.',
    'market.send_pooled_req': 'Send Pooled Request',


    'market.shopping_cart': 'Shopping Cart',
    'market.proceed_checkout': 'Proceed to Checkout',
    'market.cart_total': 'Total:',
    'market.cart_empty': 'Your cart is empty.',
    'market.close': 'Close',


    'market.contact_revealed': 'Farmer Contact (Revealed)',
    'market.contact_reveal_msg': 'Farmer contact revealed after acceptance.',
    'market.contact_reveal_short': 'Contact revealed on accept',


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
    'market.price_per_kg': 'Price / kg',
    'market.price_per_quintal': 'Price / Quintal',
    'market.price_per_tonne': 'Price / Tonne',


    'auth.slogan': 'Empowering farmers, serving buyers',
    'auth.slogan_desc': 'Join the most trusted agricultural marketplace in India.',
    'auth.feat1': 'Direct farmer-to-buyer connection',
    'auth.feat2': 'Live mandi price comparison',
    'auth.feat3': 'Zero commission platform',
    'auth.welcome': 'Welcome Back',
    'auth.sign_in_desc': 'Sign in to your AgriConnect account',
    'auth.remember': 'Remember me',
    'auth.forgot': 'Forgot password?',
    'auth.no_account': 'Don\'t have an account?',
    'auth.create': 'Create an Account',
    'auth.join_today': 'Join AgriConnect today',
    'auth.have_account': 'Already have an account?',
    'auth.back': 'Back to home',
    'auth.demo': 'Demo Credentials',

'hero.badge': 'Revolutionizing Indian Agriculture',


    'hero.join_farmers': 'Join <strong class="text-white">2,400+</strong> farmers already earning more',
    'hero.profit_increase': '+35% Profit',
    'hero.avg_increase': 'Average farmer increase',
    'footer.copyright': '© 2026 AgriConnect. All rights reserved.',


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

  },
  hi: {
    // Navbar
    'nav.home': 'होम',
    // Landing
    'hero.title': 'खेत से सीधे आपके पास',
    'hero.subtitle': 'किसानों को सीधे खरीदारों से जोड़ें। कोई बिचौलिया नहीं। सभी के लिए बेहतर दाम।',
    'hero.cta_farmer': 'मैं किसान हूँ',
    'hero.cta_buyer': 'मैं खरीदार हूँ',
    'hero.stat_farmers': 'पंजीकृत किसान',
    'hero.stat_volume': 'व्यापार मात्रा (₹)',
    'hero.stat_crops': 'फसल किस्में',
    'hero.stat_states': 'राज्य',
    // How it works
    'how.title': 'AgriConnect कैसे काम करता है',
    'how.step1_title': 'किसान उपज सूचीबद्ध करें',
    'how.step1_desc': 'किसान अपनी फसल की जानकारी, मात्रा और मूल्य अपलोड करते हैं।',
    'how.step2_title': 'खरीदार खोजें',
    'how.step2_desc': 'खरीदार सूचियाँ खोजते, फ़िल्टर करते और लाइव बाज़ार मूल्यों से तुलना करते हैं।',
    'how.step3_title': 'सीधा सौदा',
    'how.step3_desc': 'सीधे जुड़ें, बातचीत करें और लेन-देन करें — शून्य कमीशन।',
    // Auth
    'auth.login': 'लॉगिन',
    'auth.signup': 'पंजीकरण',
    'auth.email': 'ईमेल',
    'auth.password': 'पासवर्ड',
    'auth.name': 'पूरा नाम',
    'auth.phone': 'फ़ोन नंबर',
    'auth.state': 'राज्य',
    'auth.district': 'ज़िला',
    'auth.role_farmer': 'मैं किसान हूँ',
    'auth.role_buyer': 'मैं खरीदार हूँ',
    // Marketplace
    'market.title': 'बाज़ार देखें',
    'market.search': 'फसल खोजें...',
    'market.filter_state': 'राज्य से फ़िल्टर',
    'market.price_range': 'मूल्य सीमा (₹/इकाई)',
    'market.send_interest': 'रुचि भेजें',
    'market.vs_market': 'बाज़ार से तुलना',
    'market.fair': 'उचित मूल्य',
    'market.overpriced': 'बाज़ार से अधिक',
    'market.map_view': 'नक्शा दृश्य',
    'market.grid_view': 'ग्रिड दृश्य',
    // Dashboard
    'dash.total_listings': 'कुल लिस्टिंग',
    'dash.requests_received': 'प्राप्त अनुरोध',
    'dash.activity': 'इस महीने की गतिविधि',
    'dash.accept': 'स्वीकार',
    'dash.reject': 'अस्वीकार',
    'dash.add_listing': 'नई लिस्टिंग जोड़ें',
    // General
    'general.loading': 'लोड हो रहा है...',
    'general.no_data': 'कोई डेटा उपलब्ध नहीं',
    'general.success': 'सफलता!',
    'general.error': 'कुछ गलत हो गया।',
    'general.submit': 'जमा करें',
    'general.cancel': 'रद्द करें',
    'general.save': 'बदलाव सहेजें',
    'general.quantity': 'मात्रा',
    'general.price': 'मूल्य',
    'general.location': 'स्थान',
    'general.status': 'स्थिति',
    'general.date': 'तारीख',
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
    'nav.logistics_dashboard': 'डैशबोर्ड',
    'nav.logistics_available': 'उपलब्ध डिलीवरी',
    'nav.logistics_my': 'मेरी डिलीवरी',
    'nav.collapse_sidebar': 'साइडबार छोटा करें',
    'nav.expand_sidebar': 'साइडबार बड़ा करें',



  }
};

// Current language state
let currentLang = localStorage.getItem('agriconnect_lang') || 'en';

// Apply translations to all elements with data-i18n attribute
function applyTranslations(lang) {
  currentLang = lang;
  localStorage.setItem('agriconnect_lang', lang);
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (translations[lang][key]) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = translations[lang][key];
      } else {
        el.innerHTML = translations[lang][key];
      }
    }
  });
  // Update toggle button text
  const btn = document.getElementById('lang-toggle-btn');
  if (btn) btn.textContent = lang === 'en' ? 'हिं' : 'EN';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  applyTranslations(currentLang);
});
