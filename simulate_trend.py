import pymongo
from datetime import datetime, timedelta
from config import MONGO_URI

client = pymongo.MongoClient(MONGO_URI)
db = client.get_default_database()

# Find the current price for Wheat in Rajasthan from the history
today_str = datetime.now().strftime("%Y-%m-%d")
recent = db.price_history.find_one({'crop_name': 'Wheat', 'state': 'Rajasthan', 'date': today_str})
current_price = recent['price'] if recent else 2000.0

# Insert a price 7 days ago that is 15% lower so the trend calculates as Rising
old_price = current_price * 0.85
old_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

db.price_history.update_one(
    {'crop_name': 'Wheat', 'state': 'Rajasthan', 'date': old_date},
    {'$set': {'crop_name': 'Wheat', 'state': 'Rajasthan', 'price': old_price, 'date': old_date}},
    upsert=True
)
print(f"Inserted old price for Wheat in Rajasthan: {old_price} on {old_date} (Current is {current_price})")
