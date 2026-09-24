import pymongo
from config import MONGO_URI
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
try:
    client.server_info()
    print("Connection Successful!")
except Exception as e:
    print(f"Connection Failed: {e}")
