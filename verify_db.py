import pymongo
from config import MONGO_URI

client = pymongo.MongoClient(MONGO_URI)
db = client.get_default_database()

listings = db.listings.find().limit(5)
for l in listings:
    print(f"Crop: {l.get('crop_name')} | Photo URL: {l.get('photo_url')}")
