import os

tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

en_adds = '''
    'payment.title': 'Complete Payment',
    'payment.demo_desc': 'Demo Payment - No real transaction',
    'payment.method': 'Payment Method',
    'payment.upi': 'UPI ID or Card Number',
    'payment.demo_note': 'Any value accepted - this is a demo.',
    'payment.pay_btn': 'Pay',
    'payment.processing': 'Processing...',
    'payment.success': 'Payment Successful!',
    'payment.success_toast': 'Payment successful! Your order is confirmed.',
    'payment.retry': 'Retry Payment',
    'payment.network_error': 'Network error. Please try again.',
    'payment.failed': 'Payment failed. Try again.',
    'payment.deal_accepted': 'Deal accepted - contact the farmer to arrange payment and delivery.',
    'payment.pay_now': 'Pay',
    'market.send_req_btn': 'Send Request',
    'market.confirm_purchase': 'Confirm Purchase',
    'market.pooled_warning': 'We couldn\\'t find enough active listings to fully cover your requested quantity. Showing the best available combination.',
    'market.send_pooled_req': 'Send Pooled Request',
'''

hi_adds = '''
    'payment.title': 'पूरा भुगतान',
    'payment.demo_desc': 'डेमो भुगतान - कोई वास्तविक लेनदेन नहीं',
    'payment.method': 'भुगतान विधि',
    'payment.upi': 'यूपीआई आईडी या कार्ड नंबर',
    'payment.demo_note': 'कोई भी मान स्वीकार्य - यह एक डेमो है।',
    'payment.pay_btn': 'भुगतान करें',
    'payment.processing': 'प्रसंस्करण...',
    'payment.success': 'भुगतान सफल!',
    'payment.success_toast': 'भुगतान सफल! आपके आदेश की पुष्टि हो गई है।',
    'payment.retry': 'भुगतान पुनः प्रयास करें',
    'payment.network_error': 'नेटवर्क त्रुटि। कृपया पुनः प्रयास करें।',
    'payment.failed': 'भुगतान विफल। पुनः प्रयास करें।',
    'payment.deal_accepted': 'सौदा स्वीकार किया गया - भुगतान और वितरण की व्यवस्था करने के लिए किसान से संपर्क करें।',
    'payment.pay_now': 'भुगतान करें',
    'market.send_req_btn': 'अनुरोध भेजें',
    'market.confirm_purchase': 'खरीद की पुष्टि करें',
    'market.pooled_warning': 'हमें आपकी मांगी गई मात्रा को पूरी तरह से कवर करने के लिए पर्याप्त सक्रिय लिस्टिंग नहीं मिलीं। सबसे अच्छा उपलब्ध संयोजन दिखा रहा है।',
    'market.send_pooled_req': 'पूल किया गया अनुरोध भेजें',
'''

if "'payment.title'" not in tcontent:
    tcontent = tcontent.replace("'general.date': 'Date',", "'general.date': 'Date',\n" + en_adds)
    tcontent = tcontent.replace("'general.date': 'दिनांक',", "'general.date': 'दिनांक',\n" + hi_adds)
    with open(tf, 'w', encoding='utf-8') as f:
        f.write(tcontent)

print("Added payment and pooled translations.")
