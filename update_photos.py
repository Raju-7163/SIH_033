from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
try:
    db = client.get_default_database()
except:
    db = client['agriconnect']

photos = {
    'Tomato': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400',
    'Onion': 'https://images.unsplash.com/photo-1620574387735-3624d75b2dbc?w=400',
    'Wheat': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400',
    'Rice': 'https://images.unsplash.com/photo-1586201375761-83865001e8ac?w=400',
    'Potato': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400',
    'Cotton': 'https://images.unsplash.com/photo-1592153594892-0b44585141e9?w=400',
    'Sugarcane': 'https://images.unsplash.com/photo-1631584024344-93ff53906a29?w=400',
    'Mango': 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=400',
    'Maize': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400',
    'Soybean': 'https://images.unsplash.com/photo-1601646271927-4a001fb33f78?w=400',
    'Mustard': 'https://images.unsplash.com/photo-1508595165502-3e2652e5a405?w=400',
    'Jute': 'https://images.unsplash.com/photo-1533604017686-3534b07fb884?w=400',
    'Banana': 'https://images.unsplash.com/photo-1571501679680-a94f6f264be4?w=400',
    'Coconut': 'https://images.unsplash.com/photo-1526614180703-827d23e7c8f2?w=400',
    'Groundnut': 'https://images.unsplash.com/photo-1588667623910-53cc8f5379dd?w=400'
}

count = 0
for crop, url in photos.items():
    res = db.listings.update_many({'crop_name': crop}, {'$set': {'photo_url': url}})
    count += res.modified_count
print(f'Updated {count} listings with correct photos.')
