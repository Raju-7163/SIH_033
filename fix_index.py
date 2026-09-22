import os
filepath = 'templates/index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(" data-i18n='hero.cta_farmer'>I'm a Farmer", "I'm a Farmer")
content = content.replace(" data-i18n='hero.cta_buyer'>I'm a Buyer", "I'm a Buyer")
content = content.replace(" data-i18n='hero.stat_farmers'>Farmers Onboarded", "Farmers Onboarded")
content = content.replace(" data-i18n='hero.stat_volume'>Trade Volume (₹)", "Trade Volume (₹)")
content = content.replace(" data-i18n='hero.stat_crops'>Crop Varieties", "Crop Varieties")
content = content.replace(" data-i18n='hero.stat_states'>States Covered", "States Covered")
content = content.replace(" data-i18n='how.step1_title'>Farmer Lists Crops", "Farmer Lists Crops")
content = content.replace(" data-i18n='how.step1_desc'>Farmers list their produce with expected price, quality details, and location.", "Farmers list their produce with expected price, quality details, and location.")
content = content.replace(" data-i18n='how.step2_title'>Buyer Discovers", "Buyer Discovers")
content = content.replace(" data-i18n='how.step2_desc'>Buyers search, filter, and compare listings with live market prices.", "Buyers search, filter, and compare listings with live market prices.")
content = content.replace(" data-i18n='how.step3_title'>Direct Deal", "Direct Deal")
content = content.replace(" data-i18n='how.step3_desc'>Connect directly, negotiate, and transact — zero commission.", "Connect directly, negotiate, and transact — zero commission.")

# Now properly inject into the enclosing tags
# Actually, wait, it's easier to just put a span around the text!
content = content.replace("I'm a Farmer", "<span data-i18n='hero.cta_farmer'>I'm a Farmer</span>")
content = content.replace("I'm a Buyer", "<span data-i18n='hero.cta_buyer'>I'm a Buyer</span>")
content = content.replace("Farmers Onboarded", "<span data-i18n='hero.stat_farmers'>Farmers Onboarded</span>")
content = content.replace("Trade Volume (₹)", "<span data-i18n='hero.stat_volume'>Trade Volume (₹)</span>")
content = content.replace("Crop Varieties", "<span data-i18n='hero.stat_crops'>Crop Varieties</span>")
content = content.replace("States Covered", "<span data-i18n='hero.stat_states'>States Covered</span>")
content = content.replace("Farmer Lists Crops", "<span data-i18n='how.step1_title'>Farmer Lists Crops</span>")
content = content.replace("Farmers list their produce with expected price, quality details, and location.", "<span data-i18n='how.step1_desc'>Farmers list their produce with expected price, quality details, and location.</span>")
content = content.replace("Buyer Discovers", "<span data-i18n='how.step2_title'>Buyer Discovers</span>")
content = content.replace("Buyers search, filter, and compare listings with live market prices.", "<span data-i18n='how.step2_desc'>Buyers search, filter, and compare listings with live market prices.</span>")
content = content.replace("Direct Deal", "<span data-i18n='how.step3_title'>Direct Deal</span>")
content = content.replace("Connect directly, negotiate, and transact — zero commission.", "<span data-i18n='how.step3_desc'>Connect directly, negotiate, and transact — zero commission.</span>")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed index.html')
