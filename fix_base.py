import os

filepath = 'templates/base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("© 2024 AgriConnect. All rights reserved.", "<span data-i18n='footer.copyright'>© 2024 AgriConnect. All rights reserved.</span>")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated base.html')
