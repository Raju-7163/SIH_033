import os

files_to_patch = {
    'templates/buyer/dashboard.html': [
        ('Requests Sent</p>', '<span data-i18n="dash.requests_sent">Requests Sent</span></p>'),
        ('Saved Listings</p>', '<span data-i18n="dash.saved_listings">Saved Listings</span></p>'),
        ('Active Deals</p>', '<span data-i18n="dash.active_deals">Active Deals</span></p>'),
        ('>Recent Requests<', ' data-i18n="dash.recent_requests">Recent Requests<'),
        ('>View All<', ' data-i18n="dash.view_all">View All<'),
        ('>Manage deals ', ' data-i18n="dash.manage_deals">Manage deals '),
        ('>Discover Fresh Produce<', ' data-i18n="dash.discover_fresh_produce">Discover Fresh Produce<'),
        ('>Connect directly with farmers across India for the best quality and prices.<', ' data-i18n="dash.discover_desc">Connect directly with farmers across India for the best quality and prices.<'),
        ('>Browse Marketplace<', ' data-i18n="market.title">Browse Marketplace<')
    ],
    'templates/buyer/marketplace.html': [
        ('>Discover Marketplace<', ' data-i18n="market.discover">Discover Marketplace<'),
        ('>State<', ' data-i18n="market.state_label">State<'),
        ('>All States<', ' data-i18n="market.all_states">All States<'),
        ('>Max Price (₹)<', ' data-i18n="market.max_price">Max Price (₹)<'),
        ('>Max Price (,1)<', ' data-i18n="market.max_price">Max Price (,1)<'),
        ('<span>Max Price', '<span data-i18n="market.max_price">Max Price'),
        ('>Need more quantity?<', ' data-i18n="market.need_more">Need more quantity?<'),
        ('>No single farmer has enough — combine listings to reach your goal.<', ' data-i18n="market.combine_desc">No single farmer has enough — combine listings to reach your goal.<'),
        ('>No single farmer has enough ?" combine listings to reach your goal.<', ' data-i18n="market.combine_desc">No single farmer has enough ?" combine listings to reach your goal.<'),
        ('>No listings found<', ' data-i18n="market.no_listings">No listings found<'),
        ('>Try adjusting your filters or search criteria.<', ' data-i18n="market.try_adjusting">Try adjusting your filters or search criteria.<'),
        ('>Filters<', ' data-i18n="market.filters">Filters<'),
        ('>Total Price<', ' data-i18n="market.total_price">Total Price<')
    ]
}

for filepath, replacements in files_to_patch.items():
    if not os.path.exists(filepath):
        print(f'{filepath} not found.')
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in replacements:
        if new in content: continue
        content = content.replace(old, new)
        
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Patched {filepath}')
    else:
        print(f'No changes for {filepath}')
