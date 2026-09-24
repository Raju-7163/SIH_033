filepath = 'templates/buyer/marketplace.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_str = '<h6 class="fw-bold mb-3" data-i18n="market.selected_farmers">Selected Farmers (<span id="combine-farmer-count">0</span>)</h6>'
new_str = '<h6 class="fw-bold mb-3"><span data-i18n="market.selected_farmers">Selected Farmers</span> (<span id="combine-farmer-count">0</span>)</h6>'

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find the target string. Maybe it's formatted differently?")
