import json
import pymongo
from config import MONGO_URI

def migrate_images():
    print('Connecting to MongoDB...')
    client = pymongo.MongoClient(MONGO_URI)
    db = client.get_default_database()
    
    print('Loading crop_images.json...')
    with open('static/data/crop_images.json', 'r', encoding='utf-8') as f:
        crop_images = json.load(f)
        
    listings = db.listings.find()
    updates = 0
    
    for l in listings:
        crop = l.get('crop_name')
        old_url = l.get('photo_url')
        
        if crop in crop_images:
            new_url = crop_images[crop]
            if old_url != new_url:
                db.listings.update_one({'_id': l['_id']}, {'$set': {'photo_url': new_url}})
                print(f"Updated {crop}: {old_url} -> {new_url}")
                updates += 1
                
    print(f"Migration complete. Updated {updates} listings.")

if __name__ == '__main__':
    migrate_images()
