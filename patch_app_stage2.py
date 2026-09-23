import os
import re

filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Helper haversine function
haversine_func = '''def haversine(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2): return 0
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

'''

if 'def haversine' not in content:
    content = content.replace('def get_market_data', haversine_func + 'def get_market_data')

# Find logistics_my_deliveries
old_logistics = '''@app.route('/logistics/my-deliveries')
@login_required(role='logistics')
def logistics_my_deliveries():
    """Show all orders claimed by this logistics partner."""
    partner_id = ObjectId(session['user_id'])
    orders = list(db.orders.find({"logistics_partner_id": partner_id}).sort("created_at", -1))
    enriched = []
    for o in orders:
        buyer  = db.users.find_one({"_id": o['buyer_id']})
        farmer = db.users.find_one({"_id": o['farmer_id']})
        enriched.append({
            "_id":             str(o['_id']),
            "crop_name":       o.get('crop_name', ''),
            "quantity":        o.get('quantity', 0),
            "total_amount":    o.get('total_amount', 0),
            "delivery_status": o.get('delivery_status', ''),
            "created_at":      o.get('created_at'),
            "pickup_district": farmer.get('district', '') if farmer else '',
            "pickup_state":    farmer.get('state', '')    if farmer else '',
            "pickup_lat":      farmer.get('lat', None)    if farmer else None,
            "pickup_lng":      farmer.get('lng', None)    if farmer else None,
            "drop_district":   buyer.get('district', '')  if buyer else '',
            "drop_state":      buyer.get('state', '')     if buyer else '',
            "drop_lat":        buyer.get('lat', None)     if buyer else None,
            "drop_lng":        buyer.get('lng', None)     if buyer else None,
            "farmer_name":     farmer['name']             if farmer else 'Unknown',
            "farmer_phone":    farmer.get('phone', 'N/A') if farmer else 'N/A',
            "buyer_name":      buyer['name']              if buyer else 'Unknown',
            "buyer_phone":     buyer.get('phone', 'N/A')  if buyer else 'N/A',
        })
    return render_template('logistics/my_deliveries.html', orders=enriched)'''

new_logistics = '''@app.route('/logistics/my-deliveries')
@login_required(role='logistics')
def logistics_my_deliveries():
    """Show all orders claimed by this logistics partner."""
    partner_id = ObjectId(session['user_id'])
    orders = list(db.orders.find({"logistics_partner_id": partner_id}).sort("created_at", -1))
    enriched = []
    for o in orders:
        buyer  = db.users.find_one({"_id": o['buyer_id']})
        farmer = db.users.find_one({"_id": o['farmer_id']})
        enriched.append({
            "_id":             str(o['_id']),
            "crop_name":       o.get('crop_name', ''),
            "quantity":        o.get('quantity', 0),
            "total_amount":    o.get('total_amount', 0),
            "delivery_status": o.get('delivery_status', ''),
            "created_at":      o.get('created_at'),
            "pickup_district": farmer.get('district', '') if farmer else '',
            "pickup_state":    farmer.get('state', '')    if farmer else '',
            "pickup_lat":      farmer.get('lat', 0.0)    if farmer else 0.0,
            "pickup_lng":      farmer.get('lng', 0.0)    if farmer else 0.0,
            "drop_district":   buyer.get('district', '')  if buyer else '',
            "drop_state":      buyer.get('state', '')     if buyer else '',
            "drop_lat":        buyer.get('lat', 0.0)     if buyer else 0.0,
            "drop_lng":        buyer.get('lng', 0.0)     if buyer else 0.0,
            "farmer_name":     farmer['name']             if farmer else 'Unknown',
            "farmer_phone":    farmer.get('phone', 'N/A') if farmer else 'N/A',
            "buyer_name":      buyer['name']              if buyer else 'Unknown',
            "buyer_phone":     buyer.get('phone', 'N/A')  if buyer else 'N/A',
        })

    # --- STAGE 2: ROUTE OPTIMIZATION ---
    optimized_route = None
    if len(enriched) >= 2:
        unvisited = []
        for idx, o in enumerate(enriched):
            unvisited.append({'id': f"P_{idx}", 'type': 'pickup', 'lat': o['pickup_lat'], 'lng': o['pickup_lng'], 'idx': idx, 'name': f"Pickup from {o['farmer_name']} ({o['crop_name']})"})
            unvisited.append({'id': f"D_{idx}", 'type': 'drop', 'lat': o['drop_lat'], 'lng': o['drop_lng'], 'idx': idx, 'name': f"Dropoff to {o['buyer_name']} ({o['crop_name']})"})
            
        start_point = (enriched[0]['pickup_lat'], enriched[0]['pickup_lng'])
        current_lat, current_lng = start_point
        visited = []
        total_opt_dist = 0.0
        
        while unvisited:
            best_dist = float('inf')
            best_stop = None
            best_idx = -1
            
            for i, stop in enumerate(unvisited):
                if stop['type'] == 'drop':
                    pickup_id = f"P_{stop['idx']}"
                    if any(u['id'] == pickup_id for u in unvisited):
                        continue
                        
                dist = haversine(current_lat, current_lng, stop['lat'], stop['lng'])
                if dist < best_dist:
                    best_dist = dist
                    best_stop = stop
                    best_idx = i
                    
            if best_stop:
                visited.append(best_stop)
                total_opt_dist += best_dist
                current_lat, current_lng = best_stop['lat'], best_stop['lng']
                unvisited.pop(best_idx)
            else:
                break
                
        orig_dist = 0.0
        if len(enriched) > 0:
            c_lat, c_lng = enriched[0]['pickup_lat'], enriched[0]['pickup_lng']
            for o in enriched:
                orig_dist += haversine(c_lat, c_lng, o['pickup_lat'], o['pickup_lng'])
                c_lat, c_lng = o['pickup_lat'], o['pickup_lng']
                orig_dist += haversine(c_lat, c_lng, o['drop_lat'], o['drop_lng'])
                c_lat, c_lng = o['drop_lat'], o['drop_lng']
                
        saved_km = max(0, orig_dist - total_opt_dist)
        
        optimized_route = {
            'stops': visited,
            'saved_km': round(saved_km, 1)
        }

    return render_template('logistics/my_deliveries.html', orders=enriched, optimized_route=optimized_route)'''

content = content.replace(old_logistics, new_logistics)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched Stage 2 in app.py")
