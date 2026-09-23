import os

filepath = 'templates/index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("data-i18n='hero.stat_farmers'><span data-i18n='hero.stat_farmers'>", "<span data-i18n='hero.stat_farmers'>")
content = content.replace("data-i18n='hero.stat_volume'><span data-i18n='hero.stat_volume'>", "<span data-i18n='hero.stat_volume'>")
content = content.replace("data-i18n='hero.stat_crops'><span data-i18n='hero.stat_crops'>", "<span data-i18n='hero.stat_crops'>")
content = content.replace("data-i18n='hero.stat_states'><span data-i18n='hero.stat_states'>", "<span data-i18n='hero.stat_states'>")

content = content.replace("data-i18n='how.step2_title'><span data-i18n='how.step2_title'>", "<span data-i18n='how.step2_title'>")
content = content.replace("data-i18n='how.step3_title'><span data-i18n='how.step3_title'>", "<span data-i18n='how.step3_title'>")

# Ensure step 1 title is translated
content = content.replace('<h5 class="fw-bold mb-3">Farmer Lists Produce</h5>', '<h5 class="fw-bold mb-3"><span data-i18n="how.step1_title">Farmer Lists Produce</span></h5>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
