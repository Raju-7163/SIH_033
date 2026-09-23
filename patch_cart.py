import os
import re

tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

en_adds = '''
    'market.shopping_cart': 'Shopping Cart',
    'market.proceed_checkout': 'Proceed to Checkout',
    'market.cart_total': 'Total:',
    'market.cart_empty': 'Your cart is empty.',
    'market.close': 'Close',
'''

hi_adds = '''
    'market.shopping_cart': 'शॉपिंग कार्ट',
    'market.proceed_checkout': 'चेकआउट के लिए आगे बढ़ें',
    'market.cart_total': 'कुल:',
    'market.cart_empty': 'आपकी कार्ट खाली है।',
    'market.close': 'बंद करें',
'''

if "'market.shopping_cart'" not in tcontent:
    tcontent = tcontent.replace("'general.date': 'Date',", "'general.date': 'Date',\n" + en_adds)
    tcontent = tcontent.replace("'general.date': 'दिनांक',", "'general.date': 'दिनांक',\n" + hi_adds)
    with open(tf, 'w', encoding='utf-8') as f:
        f.write(tcontent)

filepath = 'templates/base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<h5 class="modal-title fw-bold">Shopping Cart</h5>', '<h5 class="modal-title fw-bold" data-i18n="market.shopping_cart">Shopping Cart</h5>')
content = content.replace('<span class="fw-bold fs-5">Total:', '<span class="fw-bold fs-5"><span data-i18n="market.cart_total">Total:</span>')
content = content.replace('>Close<', ' data-i18n="market.close">Close<')
content = content.replace('>Proceed to Checkout<', ' data-i18n="market.proceed_checkout">Proceed to Checkout<')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

filepath_js = 'static/js/main.js'
with open(filepath_js, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Your cart is empty.', '<span data-i18n="market.cart_empty">Your cart is empty.</span>')

with open(filepath_js, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched cart stuff")
