import os
filepath = 'templates/buyer/marketplace.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('>Discover Marketplace<', ' data-i18n="market.title">Discover Marketplace<'),
    ('placeholder="Search crops..."', 'data-i18n="market.search" placeholder="Search crops..."'),
    ('>Filter by State<', ' data-i18n="market.filter_state">Filter by State<'),
    ('>Price Range (₹/unit)<', ' data-i18n="market.price_range">Price Range (₹/unit)<'),
    ('>Map View<', ' data-i18n="market.map_view">Map View<'),
    ('>Grid View<', ' data-i18n="market.grid_view">Grid View<'),
    ('>Send Interest<', ' data-i18n="market.send_interest">Send Interest<'),
    ('>vs Market<', ' data-i18n="market.vs_market">vs Market<'),
    ('>Fair Price<', ' data-i18n="market.fair">Fair Price<'),
    ('>Above Market<', ' data-i18n="market.overpriced">Above Market<')
]

for old, new in replacements:
    if new not in content:
        content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched marketplace.html')
