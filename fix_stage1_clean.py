filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will just replace the whole Stage 1 block since it got messed up.
# Let's find from "# --- STAGE 1" to "demand_level = "High Demand 🔥"" (or whatever it is now)
start_marker = "# --- STAGE 1: DEMAND FORECASTING ---"
end_marker = "ai_insights ="

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_stage1 = """# --- STAGE 1: DEMAND FORECASTING ---
    today_str = datetime.now().strftime("%Y-%m-%d")
    if avg_price > 0:
        db.price_history.update_one(
            {'crop_name': crop, 'state': state, 'date': today_str},
            {'$setOnInsert': {'crop_name': crop, 'state': state, 'price': avg_price, 'date': today_str}},
            upsert=True
        )
    
    history = list(db.price_history.find({'crop_name': crop, 'state': state}).sort('date', 1))
    
    trend_pct = 0.0
    trend_dir = "Stable →"
    trend_insight = "Prices are stable — no urgency to sell."
    
    if len(history) >= 2:
        oldest = history[0]['price']
        newest = history[-1]['price']
        if oldest > 0:
            trend_pct = ((newest - oldest) / oldest) * 100.0
            if trend_pct > 2.0:
                trend_dir = "Rising ↑"
                trend_insight = f"Prices have risen {trend_pct:.1f}% recently — consider listing now."
            elif trend_pct < -2.0:
                trend_dir = "Falling ↓"
                trend_insight = f"Prices have fallen {abs(trend_pct):.1f}% recently — you may want to wait."

    supply_agg = db.listings.aggregate([
        {'$match': {'crop_name': crop, 'status': 'active'}},
        {'$group': {'_id': None, 'total': {'$sum': '$quantity'}}}
    ])
    supply_total = list(supply_agg)
    supply_qty = supply_total[0]['total'] if supply_total else 0
    
    req_agg = db.requests.aggregate([
        {'$match': {'crop_name': crop, 'status': {'$in': ['pending', 'accepted']}}},
        {'$group': {'_id': None, 'total': {'$sum': '$quantity_requested'}}}
    ])
    req_total = list(req_agg)
    demand_qty = req_total[0]['total'] if req_total else 0
    
    demand_level = "Normal Demand"
    if supply_qty > 0 and (demand_qty / supply_qty) > 0.7:
        demand_level = "High Demand 🔥"
    elif supply_qty == 0 and demand_qty > 0:
        demand_level = "High Demand 🔥"
        
    """
    
    content = content[:start_idx] + new_stage1 + content[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed block")
