from pymongo import MongoClient
import config
try:
    db = MongoClient(config.MONGO_URI).get_database('agriconnect')
    for l in db.listings.find({}, {'crop_name': 1, 'photo_url': 1}):
        print(f"{l.get('crop_name')}: {l.get('photo_url')}")
except Exception as e:
    print(e)

