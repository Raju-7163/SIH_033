import pymongo
from config import MONGO_URI
client = pymongo.MongoClient(MONGO_URI)
db = client.get_default_database()

print(db.listings.find_one({"state": None}))
