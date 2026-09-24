import os
filepath = 'templates/auth/login.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Empowering farmers, serving buyers", "<span data-i18n='auth.slogan'>Empowering farmers, serving buyers</span>")
content = content.replace("Join the most trusted agricultural marketplace in India.", "<span data-i18n='auth.slogan_desc'>Join the most trusted agricultural marketplace in India.</span>")
content = content.replace("Direct farmer-to-buyer connection", "<span data-i18n='auth.feat1'>Direct farmer-to-buyer connection</span>")
content = content.replace("Live mandi price comparison", "<span data-i18n='auth.feat2'>Live mandi price comparison</span>")
content = content.replace("Zero commission platform", "<span data-i18n='auth.feat3'>Zero commission platform</span>")
content = content.replace("Welcome Back", "<span data-i18n='auth.welcome'>Welcome Back</span>")
content = content.replace("Sign in to your FarmLink AI account", "<span data-i18n='auth.sign_in_desc'>Sign in to your FarmLink AI account</span>")
content = content.replace("Remember me", "<span data-i18n='auth.remember'>Remember me</span>")
content = content.replace("Forgot password?", "<span data-i18n='auth.forgot'>Forgot password?</span>")
content = content.replace("Don't have an account?", "<span data-i18n='auth.no_account'>Don't have an account?</span>")
content = content.replace("Back to home", "<span data-i18n='auth.back'>Back to home</span>")
content = content.replace("Demo Credentials", "<span data-i18n='auth.demo'>Demo Credentials</span>")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

filepath = 'templates/auth/signup.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Empowering farmers, serving buyers", "<span data-i18n='auth.slogan'>Empowering farmers, serving buyers</span>")
content = content.replace("Join the most trusted agricultural marketplace in India.", "<span data-i18n='auth.slogan_desc'>Join the most trusted agricultural marketplace in India.</span>")
content = content.replace("Direct farmer-to-buyer connection", "<span data-i18n='auth.feat1'>Direct farmer-to-buyer connection</span>")
content = content.replace("Live mandi price comparison", "<span data-i18n='auth.feat2'>Live mandi price comparison</span>")
content = content.replace("Zero commission platform", "<span data-i18n='auth.feat3'>Zero commission platform</span>")
content = content.replace("Create an Account", "<span data-i18n='auth.create'>Create an Account</span>")
content = content.replace("Join FarmLink AI today", "<span data-i18n='auth.join_today'>Join FarmLink AI today</span>")
content = content.replace("Already have an account?", "<span data-i18n='auth.have_account'>Already have an account?</span>")
content = content.replace("Back to home", "<span data-i18n='auth.back'>Back to home</span>")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

tf = 'static/js/translations.js'
with open(tf, 'r', encoding='utf-8') as f:
    tcontent = f.read()

en_adds = """
    'auth.slogan': 'Empowering farmers, serving buyers',
    'auth.slogan_desc': 'Join the most trusted agricultural marketplace in India.',
    'auth.feat1': 'Direct farmer-to-buyer connection',
    'auth.feat2': 'Live mandi price comparison',
    'auth.feat3': 'Zero commission platform',
    'auth.welcome': 'Welcome Back',
    'auth.sign_in_desc': 'Sign in to your FarmLink AI account',
    'auth.remember': 'Remember me',
    'auth.forgot': 'Forgot password?',
    'auth.no_account': 'Don\\'t have an account?',
    'auth.create': 'Create an Account',
    'auth.join_today': 'Join FarmLink AI today',
    'auth.have_account': 'Already have an account?',
    'auth.back': 'Back to home',
    'auth.demo': 'Demo Credentials',
"""

hi_adds = """
    'auth.slogan': 'किसानों को सशक्त बनाना, खरीदारों की सेवा करना',
    'auth.slogan_desc': 'भारत के सबसे विश्वसनीय कृषि बाज़ार से जुड़ें।',
    'auth.feat1': 'सीधा किसान-से-खरीदार संपर्क',
    'auth.feat2': 'लाइव मंडी मूल्य तुलना',
    'auth.feat3': 'शून्य कमीशन मंच',
    'auth.welcome': 'वापसी पर स्वागत है',
    'auth.sign_in_desc': 'अपने एग्रीकनेक्ट खाते में साइन इन करें',
    'auth.remember': 'मुझे याद रखें',
    'auth.forgot': 'पासवर्ड भूल गए?',
    'auth.no_account': 'खाता नहीं है?',
    'auth.create': 'खाता बनाएं',
    'auth.join_today': 'आज ही एग्रीकनेक्ट से जुड़ें',
    'auth.have_account': 'क्या आपके पास पहले से एक खाता है?',
    'auth.back': 'होम पर वापस जाएं',
    'auth.demo': 'डेमो क्रेडेंशियल',
"""

tcontent = tcontent.replace("'general.date': 'Date',", "'general.date': 'Date',\n" + en_adds)
tcontent = tcontent.replace("'general.date': 'दिनांक',", "'general.date': 'दिनांक',\n" + hi_adds)

with open(tf, 'w', encoding='utf-8') as f:
    f.write(tcontent)

print('Updated auth strings')
