import pymongo
from config import MONGO_URI
client = pymongo.MongoClient(MONGO_URI)
db = client.get_default_database()

for l in db.listings.find().limit(5):
    print(l.get('state'))
