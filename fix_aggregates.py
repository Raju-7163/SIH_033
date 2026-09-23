import re

filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

bad_supply = """    supply_agg = db.listings.aggregate([
        {'': {'crop_name': crop, 'status': 'active'}},
        {'': {'_id': None, 'total': {'': ''}}}
    ])"""

good_supply = """    supply_agg = db.listings.aggregate([
        {'$match': {'crop_name': crop, 'status': 'active'}},
        {'$group': {'_id': None, 'total': {'$sum': '$quantity'}}}
    ])"""

bad_req = """    req_agg = db.requests.aggregate([
        {'': {'crop_name': crop, 'status': {'': ['pending', 'accepted']}}},
        {'': {'_id': None, 'total': {'': ''}}}
    ])"""

good_req = """    req_agg = db.requests.aggregate([
        {'$match': {'crop_name': crop, 'status': {'$in': ['pending', 'accepted']}}},
        {'$group': {'_id': None, 'total': {'$sum': '$quantity_requested'}}}
    ])"""

content = content.replace(bad_supply, good_supply)
content = content.replace(bad_req, good_req)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
