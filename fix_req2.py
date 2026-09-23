import os

reqs = '''Flask==3.0.3
pymongo==4.7.2
bcrypt==4.1.3
python-dotenv==1.0.1
Werkzeug==3.0.3
requests==2.32.3
dnspython==2.6.1
certifi==2025.8.3
gunicorn==22.0.0
google-generativeai==0.8.3
protobuf==4.25.3
'''

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(reqs)
