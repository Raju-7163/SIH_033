filepath = 'requirements.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('google-generativeai==0.5.2', 'google-generativeai==0.8.3\nprotobuf==4.25.3')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
