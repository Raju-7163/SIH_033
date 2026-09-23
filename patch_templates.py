import os
import re

files_to_patch = {
    'templates/auth/signup.html': [
        ('Aadhaar Number', '<span data-i18n="auth.aadhaar_label">Aadhaar Number</span>'),
        ('(for KYC verification)', '<span data-i18n="auth.aadhaar_kyc">(for KYC verification)</span>'),
        ('Enter 12-digit Aadhaar number', '" data-i18n="auth.aadhaar_placeholder" placeholder="Enter 12-digit Aadhaar number'),
        ('Only the last 4 digits are stored. Your full number is never saved.', '<span data-i18n="auth.aadhaar_help">Only the last 4 digits are stored. Your full number is never saved.</span>'),
        ('Please enter a valid 12-digit Aadhaar number.', '<span data-i18n="auth.aadhaar_invalid">Please enter a valid 12-digit Aadhaar number.</span>')
    ],
    'templates/logistics/dashboard.html': [
        ('>Logistics Dashboard<', ' data-i18n="logistics.dash_title">Logistics Dashboard<'),
        ('Welcome back,', '<span data-i18n="logistics.welcome_back">Welcome back,</span>'),
        ('View Available Deliveries', '<span data-i18n="logistics.view_available">View Available Deliveries</span>'),
        ('>Available<', ' data-i18n="logistics.available_stat">Available<'),
        ('>My Deliveries<', ' data-i18n="logistics.my_deliveries_stat">My Deliveries<'),
        ('>In Transit<', ' data-i18n="logistics.in_transit_stat">In Transit<'),
        ('>Delivered<', ' data-i18n="logistics.delivered_stat">Delivered<'),
        ('>Available Deliveries<', ' data-i18n="logistics.available_title">Available Deliveries<'),
        ('>Browse paid orders waiting for a logistics partner. Accept deliveries to add them to your queue.<', ' data-i18n="logistics.available_desc">Browse paid orders waiting for a logistics partner. Accept deliveries to add them to your queue.<'),
        ('Browse <i', '<span data-i18n="logistics.browse_btn">Browse</span> <i'),
        ('>Track and update the status of deliveries you have accepted. Update from Picked Up → In Transit → Delivered.<', ' data-i18n="logistics.my_deliveries_desc">Track and update the status of deliveries you have accepted. Update from Picked Up → In Transit → Delivered.<'),
        ('View Mine <i', '<span data-i18n="logistics.view_mine_btn">View Mine</span> <i')
    ],
    'templates/logistics/available_deliveries.html': [
        ('>Available Deliveries<', ' data-i18n="logistics.available_title">Available Deliveries<'),
        ('>Accept Delivery<', ' data-i18n="logistics.accept">Accept Delivery<'),
        ('>No available deliveries right now.<', ' data-i18n="logistics.no_available">No available deliveries right now.<')
    ],
    'templates/logistics/my_deliveries.html': [
        ('>My Deliveries<', ' data-i18n="logistics.my_deliveries_title">My Deliveries<'),
        ('>Update Status<', ' data-i18n="logistics.update_status">Update Status<'),
        ('>Picked Up<', ' data-i18n="logistics.picked_up">Picked Up<'),
        ('>In Transit<', ' data-i18n="logistics.in_transit">In Transit<'),
        ('>Delivered<', ' data-i18n="logistics.delivered">Delivered<'),
        ('>You have not accepted any deliveries yet.<', ' data-i18n="logistics.no_mine">You have not accepted any deliveries yet.<')
    ],
    'templates/logistics/profile.html': [
        ('>Profile<', ' data-i18n="logistics.profile">Profile<')
    ],
    'templates/buyer/marketplace.html': [
        ('>Buy Now<', ' data-i18n="market.buy_now">Buy Now<'),
        ('>Add to Cart<', ' data-i18n="market.add_to_cart">Add to Cart<'),
        ('>Combine Listings<', ' data-i18n="market.combine_listings">Combine Listings<'),
        ('>Target Quantity<', ' data-i18n="market.target_qty">Target Quantity<'),
        ('>Total Estimated Cost<', ' data-i18n="market.total_est_cost">Total Estimated Cost<'),
        ('>Selected Farmers (<', ' data-i18n="market.selected_farmers">Selected Farmers (<'),
        ('>Payment<', ' data-i18n="market.payment">Payment<')
    ],
    'templates/base.html': [
        ('>Collapse Sidebar<', ' data-i18n="nav.collapse_sidebar">Collapse Sidebar<'),
        ('>Expand Sidebar<', ' data-i18n="nav.expand_sidebar">Expand Sidebar<'),
        ('href="{{ url_for(\'logistics_dashboard\') }}" class="nav-link', 'href="{{ url_for(\'logistics_dashboard\') }}" data-i18n="nav.logistics_dashboard" class="nav-link'),
        ('href="{{ url_for(\'logistics_available\') }}" class="nav-link', 'href="{{ url_for(\'logistics_available\') }}" data-i18n="nav.logistics_available" class="nav-link'),
        ('href="{{ url_for(\'logistics_my_deliveries\') }}" class="nav-link', 'href="{{ url_for(\'logistics_my_deliveries\') }}" data-i18n="nav.logistics_my" class="nav-link')
    ],
    'static/js/marketplace.js': [
        ('>Buy Now<', ' data-i18n="market.buy_now">Buy Now<'),
        ('>Add to Cart<', ' data-i18n="market.add_to_cart">Add to Cart<')
    ],
    'templates/buyer/dashboard.html': [
        ('>Checkout<', ' data-i18n="market.checkout">Checkout<')
    ],
    'templates/farmer/requests.html': [
        ('>Farmer contact info revealed after acceptance<', ' data-i18n="market.contact_reveal">Farmer contact info revealed after acceptance<')
    ],
    'templates/farmer/market_prices.html': [
        ('>Price / kg<', ' data-i18n="market.price_per_kg">Price / kg<'),
        ('>Price / Quintal<', ' data-i18n="market.price_per_quintal">Price / Quintal<'),
        ('>Price / Tonne<', ' data-i18n="market.price_per_tonne">Price / Tonne<')
    ]
}

# Fix some problematic ones manually in JS if needed
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

