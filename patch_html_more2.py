import os
import re

files_to_patch = {
    'templates/buyer/marketplace.html': [
        ('>Cancel<', ' data-i18n="general.cancel">Cancel<'),
        ('> Send Request', '> <span data-i18n="market.send_req_btn">Send Request</span>'),
        ('> Confirm Purchase', '> <span data-i18n="market.confirm_purchase">Confirm Purchase</span>'),
        (">We couldn't find enough active listings to fully cover your requested quantity. Showing the best available combination.<", ' data-i18n="market.pooled_warning">We couldn\\'t find enough active listings to fully cover your requested quantity. Showing the best available combination.<'),
        ('> Send Pooled Request', '> <span data-i18n="market.send_pooled_req">Send Pooled Request</span>')
    ],
    'templates/buyer/my_requests.html': [
        ('>Complete Payment<', ' data-i18n="payment.title">Complete Payment<'),
        ('>Demo Payment - No real transaction<', ' data-i18n="payment.demo_desc">Demo Payment - No real transaction<'),
        ('>Payment Method<', ' data-i18n="payment.method">Payment Method<'),
        ('placeholder="e.g. yourname@upi or 4242 4242 4242 4242"', 'data-i18n="payment.upi" placeholder="e.g. yourname@upi or 4242 4242 4242 4242"'),
        ('>Any value accepted - this is a demo.<', ' data-i18n="payment.demo_note">Any value accepted - this is a demo.<')
    ]
}

for filepath, replacements in files_to_patch.items():
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    for old, new in replacements:
        if 'data-i18n' in old: continue
        content = content.replace(old, new)
        
    if 'my_requests.html' in filepath:
        content = content.replace('Deal accepted - contact the farmer to arrange payment and delivery.', '<span data-i18n="payment.deal_accepted">Deal accepted - contact the farmer to arrange payment and delivery.</span>')
        content = content.replace('Pay ₹{{ req.total_amount }} Now', '<span data-i18n="payment.pay_now">Pay</span> ₹{{ req.total_amount }} <span data-i18n="market.buy_now">Now</span>')
        content = content.replace('Pay <span id="pay-btn-amount">', '<span data-i18n="payment.pay_btn">Pay</span> <span id="pay-btn-amount">')

    if orig != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {filepath}")

