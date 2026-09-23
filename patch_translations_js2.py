import os

tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

en_adds = '''
    'market.contact_revealed': 'Farmer Contact (Revealed)',
    'market.contact_reveal_msg': 'Farmer contact revealed after acceptance.',
    'market.contact_reveal_short': 'Contact revealed on accept',
'''

hi_adds = '''
    'market.contact_revealed': 'किसान संपर्क (प्रकट)',
    'market.contact_reveal_msg': 'स्वीकृति के बाद किसान का संपर्क प्रकट किया गया।',
    'market.contact_reveal_short': 'स्वीकार करने पर संपर्क प्रकट',
'''

if "'market.contact_revealed'" not in tcontent:
    tcontent = tcontent.replace("'general.date': 'Date',", "'general.date': 'Date',\n" + en_adds)
    tcontent = tcontent.replace("'general.date': 'दिनांक',", "'general.date': 'दिनांक',\n" + hi_adds)
    with open(tf, 'w', encoding='utf-8') as f:
        f.write(tcontent)
    print("Updated translations.js for contacts")
