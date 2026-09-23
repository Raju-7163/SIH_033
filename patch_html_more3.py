import os
import re

filepath = 'templates/buyer/marketplace.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('>Cancel<', ' data-i18n="general.cancel">Cancel<')
content = content.replace('> Send Request', '> <span data-i18n="market.send_req_btn">Send Request</span>')
content = content.replace('> Confirm Purchase', '> <span data-i18n="market.confirm_purchase">Confirm Purchase</span>')
content = content.replace('We couldn\\'t find enough active listings to fully cover your requested quantity. Showing the best available combination.', '<span data-i18n="market.pooled_warning">We couldn\\'t find enough active listings to fully cover your requested quantity. Showing the best available combination.</span>')
content = content.replace('> Send Pooled Request', '> <span data-i18n="market.send_pooled_req">Send Pooled Request</span>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)


filepath = 'templates/buyer/my_requests.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('>Complete Payment<', ' data-i18n="payment.title">Complete Payment<')
content = content.replace('>Demo Payment - No real transaction<', ' data-i18n="payment.demo_desc">Demo Payment - No real transaction<')
content = content.replace('>Payment Method<', ' data-i18n="payment.method">Payment Method<')
content = content.replace('placeholder="e.g. yourname@upi or 4242 4242 4242 4242"', 'data-i18n="payment.upi" placeholder="e.g. yourname@upi or 4242 4242 4242 4242"')
content = content.replace('>Any value accepted - this is a demo.<', ' data-i18n="payment.demo_note">Any value accepted - this is a demo.<')
content = content.replace('Deal accepted - contact the farmer to arrange payment and delivery.', '<span data-i18n="payment.deal_accepted">Deal accepted - contact the farmer to arrange payment and delivery.</span>')
content = content.replace('Pay ₹{{ req.total_amount }} Now', '<span data-i18n="payment.pay_now">Pay</span> ₹{{ req.total_amount }} <span data-i18n="market.buy_now">Now</span>')
content = content.replace('Pay <span id="pay-btn-amount">', '<span data-i18n="payment.pay_btn">Pay</span> <span id="pay-btn-amount">')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched completely.")
