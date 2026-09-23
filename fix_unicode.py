filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Stable +\'', 'Stable \\u2192')
content = content.replace('Prices are stable ?"', 'Prices are stable \\u2014')
content = content.replace('Rising +`', 'Rising \\u2191')
content = content.replace('recently ?" consider', 'recently \\u2014 consider')
content = content.replace('Falling +""', 'Falling \\u2193')
content = content.replace('recently ?" you', 'recently \\u2014 you')
content = content.replace('High Demand dY""', 'High Demand \\U0001F525')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
