import pymongo
from config import MONGO_URI
client = pymongo.MongoClient(MONGO_URI)
db = client.get_default_database()
print("Users:")
for u in db.users.find().limit(5):
    print(u.get('role'), u.get('name'), u.get('lat'), u.get('lng'))
