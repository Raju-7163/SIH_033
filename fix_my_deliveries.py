filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove the accidental Stage 2 block from logistics_available
bad_available_block = """    # --- STAGE 2: ROUTE OPTIMIZATION ---
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
            'saved_km': round(saved_km, 1),
            'orig_dist': round(orig_dist, 1),
            'opt_dist': round(total_opt_dist, 1)
        }"""
content = content.replace(bad_available_block, "")

# Now fix logistics_my_deliveries specifically
start_marker = "def logistics_my_deliveries():"
end_marker = "return render_template('logistics/my_deliveries.html'"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_my_deliveries = """def logistics_my_deliveries():
    \"\"\"Show all orders claimed by this logistics partner.\"\"\"
    partner_id = ObjectId(session['user_id'])
    orders = list(db.orders.find({"logistics_partner_id": partner_id}).sort("created_at", -1))
    enriched = []
    for idx, o in enumerate(orders):
        buyer  = db.users.find_one({"_id": o['buyer_id']})
        farmer = db.users.find_one({"_id": o['farmer_id']})
        
        # Ensure we have valid float coordinates. Fallback to Nashik area if missing/0
        f_lat = float(farmer.get('lat') or 0.0) if farmer else 0.0
        f_lng = float(farmer.get('lng') or 0.0) if farmer else 0.0
        b_lat = float(buyer.get('lat') or 0.0) if buyer else 0.0
        b_lng = float(buyer.get('lng') or 0.0) if buyer else 0.0
        
        if f_lat == 0.0: f_lat = 20.01 + (idx * 0.05)
        if f_lng == 0.0: f_lng = 73.78 + (idx * 0.05)
        if b_lat == 0.0: b_lat = 19.99 - (idx * 0.05)
        if b_lng == 0.0: b_lng = 73.80 - (idx * 0.05)
        
        enriched.append({
            "_id":             str(o['_id']),
            "crop_name":       o.get('crop_name', ''),
            "quantity":        o.get('quantity', 0),
            "total_amount":    o.get('total_amount', 0),
            "delivery_status": o.get('delivery_status', ''),
            "created_at":      o.get('created_at'),
            "pickup_district": farmer.get('district', '') if farmer else '',
            "pickup_state":    farmer.get('state', '')    if farmer else '',
            "pickup_lat":      f_lat,
            "pickup_lng":      f_lng,
            "drop_district":   buyer.get('district', '')  if buyer else '',
            "drop_state":      buyer.get('state', '')     if buyer else '',
            "drop_lat":        b_lat,
            "drop_lng":        b_lng,
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
            'saved_km': round(saved_km, 1),
            'orig_dist': round(orig_dist, 1),
            'opt_dist': round(total_opt_dist, 1)
        }

    """
    
    content = content[:start_idx] + new_my_deliveries + content[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched my_deliveries correctly!")
else:
    print("Could not find my_deliveries block")
