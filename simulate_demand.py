import pymongo
from config import MONGO_URI
client = pymongo.MongoClient(MONGO_URI)
db = client.get_default_database()

crop = 'Wheat'
active_listings = list(db.listings.find({'crop_name': crop, 'status': 'active'}))
supply_qty = sum(l.get('quantity', 0) for l in active_listings)
print(f"Current Wheat Supply: {supply_qty} kg")

if active_listings:
    listing_id = active_listings[0]['_id']
    farmer_id = active_listings[0]['farmer_id']
    
    # insert dummy buyer request to spike demand
    db.requests.insert_one({
        "buyer_id": farmer_id, # doesn't matter for this
        "farmer_id": farmer_id,
        "listing_id": listing_id,
        "quantity_requested": supply_qty + 500,  # Ensure demand > 70% of supply
        "message": "Fake high demand request for testing",
        "status": "pending"
    })
    print("Inserted high demand request!")
else:
    print("No active wheat listings found.")
