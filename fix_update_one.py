filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """        db.price_history.update_one(
            {'crop_name': crop, 'state': state, 'date': today_str},
            {'': {'crop_name': crop, 'state': state, 'price': avg_price, 'date': today_str}},
            upsert=True
        )"""

new_code = """        db.price_history.update_one(
            {'crop_name': crop, 'state': state, 'date': today_str},
            {'$setOnInsert': {'crop_name': crop, 'state': state, 'price': avg_price, 'date': today_str}},
            upsert=True
        )"""

content = content.replace(old_code, new_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
