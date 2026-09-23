import os
import re

filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
if 'import math' not in content:
    content = content.replace('import config', 'import config\nimport math\nimport os')
if 'google.generativeai' not in content:
    content = content.replace('import config', 'import config\nimport google.generativeai as genai')

# Patch farmer_market_prices
old_farmer_market = '''@app.route('/farmer/market-prices')
@login_required(role='farmer')
def farmer_market_prices():
    """Fetch mandi prices and show bar chart with suggested fair price."""
    crop = request.args.get('crop', 'Wheat')
    state = request.args.get('state', session.get('state', 'Maharashtra'))
    market_data = get_market_data(crop, state)
    return render_template(
        'farmer/market_prices.html',
        market_data=market_data,
        suggested_price=market_data['avg_price'],
        crop=crop,
        state=state
    )'''

new_farmer_market = '''@app.route('/farmer/market-prices')
@login_required(role='farmer')
def farmer_market_prices():
    """Fetch mandi prices and show bar chart with suggested fair price."""
    crop = request.args.get('crop', 'Wheat')
    state = request.args.get('state', session.get('state', 'Maharashtra'))
    market_data = get_market_data(crop, state)
    avg_price = market_data['avg_price']

    # --- STAGE 1: DEMAND FORECASTING ---
    today_str = datetime.now().strftime("%Y-%m-%d")
    if avg_price > 0:
        db.price_history.update_one(
            {'crop_name': crop, 'state': state, 'date': today_str},
            {'': {'price': avg_price}},
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
        {'': {'crop_name': crop, 'status': 'active'}},
        {'': {'_id': None, 'total': {'': ''}}}
    ])
    supply_total = list(supply_agg)
    supply_qty = supply_total[0]['total'] if supply_total else 0
    
    req_agg = db.requests.aggregate([
        {'': {'crop_name': crop, 'status': {'': ['pending', 'accepted']}}},
        {'': {'_id': None, 'total': {'': ''}}}
    ])
    req_total = list(req_agg)
    demand_qty = req_total[0]['total'] if req_total else 0
    
    demand_level = "Normal Demand"
    if supply_qty > 0 and (demand_qty / supply_qty) > 0.7:
        demand_level = "High Demand 🔥"
    elif supply_qty == 0 and demand_qty > 0:
        demand_level = "High Demand 🔥"
        
    ai_insights = {
        'trend_dir': trend_dir,
        'trend_pct': round(trend_pct, 1),
        'insight': trend_insight,
        'demand_level': demand_level,
        'advisory': None
    }
    
    # --- STAGE 3: GEMINI AI ADVISORY ---
    api_key = os.environ.get("GEMINI_API_KEY")
    lang_cookie = request.cookies.get('lang', 'en')
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            lang_instruction = "Respond in Hindi." if lang_cookie == 'hi' else "Respond in English."
            prompt = f"You are an agricultural advisor. The crop '{crop}' has a price trend of {trend_pct:.1f}% ({trend_dir}), and the current demand level is '{demand_level}'. Write ONE short, simple, non-technical sentence of advice for a farmer deciding whether to sell now or wait. {lang_instruction}"
            
            response = model.generate_content(prompt, request_options={'timeout': 5.0})
            if response and response.text:
                ai_insights['advisory'] = response.text.strip().replace('\\n', '')
        except Exception as e:
            app.logger.error(f"Gemini AI advisory failed: {e}")
            pass

    return render_template(
        'farmer/market_prices.html',
        market_data=market_data,
        suggested_price=market_data['avg_price'],
        crop=crop,
        state=state,
        ai_insights=ai_insights
    )'''

content = content.replace(old_farmer_market, new_farmer_market)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched Stage 1 & 3 in app.py")
