import bcrypt
from datetime import datetime
from pymongo import MongoClient
import certifi
import config

def seed_database():
    """Seeds the MongoDB database with initial farmers, buyers, listings, requests, and notifications.
    Idempotent — checks if data already exists before inserting anything."""
    print("Connecting to MongoDB for seeding...")
    client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
    try:
        db = client.get_default_database()   # Uses DB name from URI
    except Exception:
        db = client['agriconnect']           # Fallback

    # Check if database is already seeded (idempotent)
    if db.users.count_documents({}) > 0:
        print(f"Database '{db.name}' already seeded ({db.users.count_documents({})} users). Skipping.")
        return

    print(f"Seeding database '{db.name}' with demo data...")

    # Helper function to hash passwords
    def hash_pwd(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # --- Seed Users ---
    farmers_data = [
        {"name": "Ramesh Kumar", "email": "ramesh@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Maharashtra", "district": "Nashik", "phone": "9876543210"},
        {"name": "Santosh Patil", "email": "santosh@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Maharashtra", "district": "Nashik", "phone": "9876543333"},
        {"name": "Vijay Kale", "email": "vijay@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Maharashtra", "district": "Nashik", "phone": "9876543444"},
        {"name": "Gurpreet Singh", "email": "gurpreet@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Punjab", "district": "Ludhiana", "phone": "9876543211"},
        {"name": "Harjit Singh", "email": "harjit@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Punjab", "district": "Ludhiana", "phone": "9876543555"},
        {"name": "Balwinder Singh", "email": "balwinder@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Punjab", "district": "Ludhiana", "phone": "9876543666"},
        {"name": "Suresh Yadav", "email": "suresh@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Uttar Pradesh", "district": "Agra", "phone": "9876543212"},
        {"name": "Manjunath Reddy", "email": "manjunath@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Karnataka", "district": "Belgaum", "phone": "9876543213"},
        {"name": "Priya Sharma", "email": "priya@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Rajasthan", "district": "Jaipur", "phone": "9876543214"},
        {"name": "Mohan Das", "email": "mohan@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "West Bengal", "district": "Murshidabad", "phone": "9876543215"},
        {"name": "Kavitha Nair", "email": "kavitha@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Kerala", "district": "Thrissur", "phone": "9876543216"},
        {"name": "Amit Patel", "email": "amit@farmer.com", "password": hash_pwd("farmer123"), "role": "farmer", "state": "Gujarat", "district": "Surat", "phone": "9876543217"},
    ]
    
    buyers_data = [
        {"name": "FreshMart Delhi", "email": "buyer1@buyer.com", "password": hash_pwd("buyer123"), "role": "buyer", "state": "Delhi", "district": "New Delhi", "phone": "9876500001"},
        {"name": "Raj Wholesale", "email": "buyer2@buyer.com", "password": hash_pwd("buyer123"), "role": "buyer", "state": "Maharashtra", "district": "Mumbai", "phone": "9876500002"},
    ]

    logistics_data = [
        {"name": "Speedy Deliveries", "email": "truck1@logistics.com", "password": hash_pwd("truck123"), "role": "logistics", "state": "Maharashtra", "district": "Pune", "phone": "9876588881"},
        {"name": "Kisan Transport", "email": "truck2@logistics.com", "password": hash_pwd("truck123"), "role": "logistics", "state": "Punjab", "district": "Chandigarh", "phone": "9876588882"},
    ]

    farmer_ids = {}
    for f in farmers_data:
        res = db.users.insert_one(f)
        farmer_ids[f['name'].split()[0]] = res.inserted_id

    buyer_ids = {}
    for b in buyers_data:
        res = db.users.insert_one(b)
        buyer_ids[b['email'].split('@')[0]] = res.inserted_id

    for l in logistics_data:
        db.users.insert_one(l)

    # --- Seed Listings ---
    photos = {}
    try:
        with open('static/data/crop_images.json', 'r', encoding='utf-8') as f:
            photos = json.load(f)
    except Exception as e:
        print("Warning: Could not load crop_images.json", e)

    now = datetime.now()
    listings_data = [
        # Combinable Group 1: Tomato from Nashik (Ramesh, Santosh, Vijay)
        {"farmer": "Ramesh", "crop": "Tomato", "qty": 400, "unit": "kg", "price": 18, "state": "Maharashtra", "district": "Nashik", "lat": 20.0059, "lng": 73.7898},
        {"farmer": "Santosh", "crop": "Tomato", "qty": 650, "unit": "kg", "price": 17, "state": "Maharashtra", "district": "Nashik", "lat": 19.9975, "lng": 73.7898},
        {"farmer": "Vijay", "crop": "Tomato", "qty": 500, "unit": "kg", "price": 19, "state": "Maharashtra", "district": "Nashik", "lat": 20.0125, "lng": 73.8011},
        
        # Combinable Group 2: Wheat from Ludhiana (Gurpreet, Harjit, Balwinder)
        {"farmer": "Gurpreet", "crop": "Wheat", "qty": 700, "unit": "kg", "price": 22, "state": "Punjab", "district": "Ludhiana", "lat": 30.9010, "lng": 75.8573},
        {"farmer": "Harjit", "crop": "Wheat", "qty": 600, "unit": "kg", "price": 21, "state": "Punjab", "district": "Ludhiana", "lat": 30.9080, "lng": 75.8423},
        {"farmer": "Balwinder", "crop": "Wheat", "qty": 450, "unit": "kg", "price": 23, "state": "Punjab", "district": "Ludhiana", "lat": 30.8950, "lng": 75.8653},
        
        # Normal sparse listings
        {"farmer": "Ramesh", "crop": "Onion", "qty": 1000, "unit": "kg", "price": 14, "state": "Maharashtra", "district": "Nashik", "lat": 20.0059, "lng": 73.7898},
        {"farmer": "Gurpreet", "crop": "Rice", "qty": 1500, "unit": "kg", "price": 35, "state": "Punjab", "district": "Amritsar", "lat": 31.6340, "lng": 74.8723},
        {"farmer": "Suresh", "crop": "Potato", "qty": 800, "unit": "kg", "price": 12, "state": "Uttar Pradesh", "district": "Agra", "lat": 27.1767, "lng": 78.0081},
        {"farmer": "Suresh", "crop": "Sugarcane", "qty": 5000, "unit": "kg", "price": 4, "state": "Uttar Pradesh", "district": "Lucknow", "lat": 26.8467, "lng": 80.9462},
        {"farmer": "Manjunath", "crop": "Cotton", "qty": 600, "unit": "kg", "price": 58, "state": "Karnataka", "district": "Belgaum", "lat": 15.8497, "lng": 74.4977},
        {"farmer": "Priya", "crop": "Mustard", "qty": 400, "unit": "kg", "price": 48, "state": "Rajasthan", "district": "Jaipur", "lat": 26.9124, "lng": 75.7873},
        {"farmer": "Priya", "crop": "Mango", "qty": 300, "unit": "kg", "price": 65, "state": "Rajasthan", "district": "Jaipur", "lat": 26.9124, "lng": 75.7873},
        {"farmer": "Mohan", "crop": "Rice", "qty": 2000, "unit": "kg", "price": 32, "state": "West Bengal", "district": "Murshidabad", "lat": 24.1800, "lng": 88.2700},
        {"farmer": "Mohan", "crop": "Jute", "qty": 1200, "unit": "kg", "price": 28, "state": "West Bengal", "district": "Kolkata", "lat": 22.5726, "lng": 88.3639},
        {"farmer": "Kavitha", "crop": "Banana", "qty": 700, "unit": "kg", "price": 22, "state": "Kerala", "district": "Thrissur", "lat": 10.5276, "lng": 76.2144},
        {"farmer": "Kavitha", "crop": "Coconut", "qty": 2000, "unit": "pc", "price": 20, "state": "Kerala", "district": "Thrissur", "lat": 10.5276, "lng": 76.2144},
        {"farmer": "Amit", "crop": "Cotton", "qty": 900, "unit": "kg", "price": 55, "state": "Gujarat", "district": "Surat", "lat": 21.1702, "lng": 72.8311},
        {"farmer": "Amit", "crop": "Groundnut", "qty": 500, "unit": "kg", "price": 45, "state": "Gujarat", "district": "Rajkot", "lat": 22.3039, "lng": 70.8022},
        {"farmer": "Gurpreet", "crop": "Maize", "qty": 1800, "unit": "kg", "price": 20, "state": "Punjab", "district": "Ludhiana", "lat": 30.9010, "lng": 75.8573},
        {"farmer": "Suresh", "crop": "Wheat", "qty": 1000, "unit": "kg", "price": 21, "state": "Uttar Pradesh", "district": "Mathura", "lat": 27.4924, "lng": 77.6737},
        {"farmer": "Ramesh", "crop": "Soybean", "qty": 600, "unit": "kg", "price": 42, "state": "Maharashtra", "district": "Nashik", "lat": 20.0059, "lng": 73.7898},
    ]

    listing_ids = []
    for l in listings_data:
        listing = {
            "farmer_id": farmer_ids[l["farmer"]],
            "crop_name": l["crop"],
            "quantity": l["qty"],
            "unit": l["unit"],
            "price_per_unit": l["price"],
            "harvest_date": now,
            "state": l["state"],
            "district": l["district"],
            "lat": l["lat"],
            "lng": l["lng"],
            "photo_url": photos.get(l["crop"], "/static/images/no-image.svg"),
            "status": "active",
            "created_at": now
        }
        res = db.listings.insert_one(listing)
        listing_ids.append(res.inserted_id)

    # --- Seed Requests & Auto-Create Orders for Accepted Ones ---
    requests_data = [
        {"buyer": "buyer1", "listing_idx": 2, "qty": 500, "msg": "We need wheat for our bakery chain. Can you arrange weekly supply?", "status": "pending"},
        {"buyer": "buyer1", "listing_idx": 0, "qty": 200, "msg": "Fresh tomatoes needed for restaurant chain in Delhi.", "status": "pending"},
        {"buyer": "buyer2", "listing_idx": 6, "qty": 300, "msg": "Looking for high-quality cotton for textile unit.", "status": "accepted"},
        {"buyer": "buyer2", "listing_idx": 4, "qty": 400, "msg": "Bulk potato purchase for chips manufacturing plant.", "status": "pending"},
    ]

    for req in requests_data:
        l_id = listing_ids[req["listing_idx"]]
        listing = db.listings.find_one({"_id": l_id})
        request_doc = {
            "buyer_id": buyer_ids[req["buyer"]],
            "farmer_id": listing["farmer_id"],
            "listing_id": l_id,
            "quantity_requested": req["qty"],
            "message": req["msg"],
            "status": req["status"],
            "created_at": now
        }
        res = db.requests.insert_one(request_doc)
        
        # If accepted, create a matching order for logistics demo
        if req["status"] == "accepted":
            price = float(listing.get('price_per_unit', 0))
            total = round(price * req["qty"], 2)
            db.orders.insert_one({
                "request_id": res.inserted_id,
                "buyer_id": buyer_ids[req["buyer"]],
                "farmer_id": listing["farmer_id"],
                "listing_id": l_id,
                "crop_name": listing.get('crop_name', 'Crop'),
                "quantity": req["qty"],
                "total_amount": total,
                "payment_status": "paid",  # Seed as paid so logistics can see it immediately
                "delivery_status": "awaiting_pickup",
                "logistics_partner_id": None,
                "created_at": now
            })

    # --- Seed Notifications ---
    notifications_data = [
        {"user_id": buyer_ids["buyer1"], "message": "Your interest in Gurpreet's Wheat listing has been received.", "status": "unread"},
        {"user_id": buyer_ids["buyer1"], "message": "New crop listing: Mango from Rajasthan now available!", "status": "unread"},
        {"user_id": farmer_ids["Ramesh"], "message": "FreshMart Delhi sent a request for your Tomato listing.", "status": "unread"},
        {"user_id": farmer_ids["Gurpreet"], "message": "FreshMart Delhi sent a request for your Wheat listing.", "status": "unread"},
        {"user_id": farmer_ids["Ramesh"], "message": "Your listing 'Soybean 600kg' is live on the marketplace.", "status": "read"},
        {"user_id": buyer_ids["buyer2"], "message": "Your request for Manjunath's Cotton has been accepted!", "status": "unread"},
    ]

    for notif in notifications_data:
        notif["created_at"] = now
        db.notifications.insert_one(notif)

    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
