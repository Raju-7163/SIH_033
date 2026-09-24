from app import app, db
import json

with app.test_client() as c:
    with c.session_transaction() as sess:
        sess['user_id'] = str(db.users.find_one({'role': 'buyer'})['_id'])
        sess['role'] = 'buyer'
    
    resp = c.get('/api/find-combinable-listings?crop_name=Rice&required_quantity=100&state=Maharashtra')
    print("Status:", resp.status_code)
    try:
        print("JSON:", resp.get_json())
    except Exception as e:
        print("HTML:", resp.get_data(as_text=True)[:200])
