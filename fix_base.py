import os

filepath = 'templates/base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('<i class="bi bi-grid-1x2"></i> Dashboard', '<i class="bi bi-grid-1x2"></i> <span data-i18n="nav.logistics_dashboard">Dashboard</span>'),
    ('<i class="bi bi-box-seam"></i> Available Deliveries', '<i class="bi bi-box-seam"></i> <span data-i18n="nav.logistics_available">Available Deliveries</span>'),
    ('<i class="bi bi-truck"></i> My Deliveries', '<i class="bi bi-truck"></i> <span data-i18n="nav.logistics_my">My Deliveries</span>'),
    ('<i class="bi bi-person"></i> Profile', '<i class="bi bi-person"></i> <span data-i18n="logistics.profile">Profile</span>'),
    ('<i class="bi bi-box-arrow-right"></i> Logout', '<i class="bi bi-box-arrow-right"></i> <span data-i18n="nav.logout">Logout</span>')
]

for old, new in replacements:
    content = content.replace(old, new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
