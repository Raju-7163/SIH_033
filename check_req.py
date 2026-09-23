import pymongo
from config import MONGO_URI
client = pymongo.MongoClient(MONGO_URI)
db = client.get_default_database()
print("Requests:")
for r in db.requests.find().limit(5):
    print(r.get('crop_name'), r.get('quantity'), r.get('quantity_requested'))
