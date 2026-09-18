"""
AgriConnect - Farmer to Buyer Marketplace
Main Flask application with all routes, authentication, and API endpoints.
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os
import bcrypt
import requests as http_requests
import json
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from functools import wraps
import config

# ── App Initialization ──────────────────────────────────────────────────────
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.jinja_env.globals.update(zip=zip)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ── MongoDB Connection ───────────────────────────────────────────────────────
try:
    client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Verify connection works
    try:
        db = client.get_default_database()
    except Exception:
        db = client['agriconnect']
    print("[OK] Connected to MongoDB -- database: " + db.name)
except Exception as conn_err:
    print("[ERROR] MongoDB connection failed: " + str(conn_err))
    db = None

# ── Auto-seed on first run ───────────────────────────────────────────────────
try:
    if db is not None:
        from seed import seed_database
        seed_database()
except Exception as seed_err:
    print("[WARN] Seeder error (non-fatal): " + str(seed_err))


# ── Helper Functions ─────────────────────────────────────────────────────────

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def login_required(role=None):
    """Decorator that enforces login and optionally a specific role."""
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash("Please log in to access this page.", "error")
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash("Unauthorized access.", "error")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated
    return wrapper


def get_market_data(crop, state):
    """
    Try the live Agmarknet API, fall back to bundled JSON, then hardcoded defaults.
    Always returns a dict: {labels: [...], prices: [...], avg_price: float}
    """
    labels = []
    prices = []

    # Step 1 -- Live API
    try:
        api_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        params = {
            "api-key": config.DATA_GOV_API_KEY,
            "format": "json",
            "filters[commodity]": crop,
            "filters[state]": state,
            "limit": 20
        }
        resp = http_requests.get(api_url, params=params, timeout=5)
        if resp.status_code == 200:
            for r in resp.json().get('records', []):
                labels.append(r.get('market', 'Unknown'))
                prices.append(float(r.get('modal_price', 0)))
    except Exception:
        pass  # Fall through to local JSON

    # Step 2 -- Bundled fallback JSON
    if not labels:
        try:
            json_path = os.path.join('static', 'data', 'mandi_prices.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                fallback = json.load(f)
            crop_key = crop.lower()
            for m in fallback.get('crops', {}).get(crop_key, {}).get('markets', []):
                labels.append(m['market'])
                prices.append(float(m['modal_price']))
        except Exception:
            pass

    # Step 3 -- Hard-coded last resort so the chart always renders
    if not labels:
        labels = ["Market A", "Market B", "Market C", "Market D"]
        prices = [2100.0, 2200.0, 1950.0, 2050.0]

    avg_price = round(sum(prices) / len(prices), 2) if prices else 0
    return {"labels": labels, "prices": prices, "avg_price": avg_price}


# ── Context processor: inject notifications into every template ──────────────
@app.context_processor
def inject_notifications():
    if 'user_id' in session and db is not None:
        notifs = list(
            db.notifications
              .find({"user_id": ObjectId(session['user_id'])})
              .sort("created_at", -1)
              .limit(10)
        )
        unread = sum(1 for n in notifs if n.get('status') == 'unread')
        return dict(notifications=notifs, unread_notifications_count=unread)
    return dict(notifications=[], unread_notifications_count=0)


# ── Public Routes ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Landing page."""
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Register a new farmer or buyer account."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'farmer')
        phone = request.form.get('phone', '').strip()
        state = request.form.get('state', '').strip()
        district = request.form.get('district', '').strip()

        if db.users.find_one({"email": email}):
            flash("Email already registered.", "error")
            return redirect(url_for('signup'))

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_pw,
            "role": role,
            "phone": phone,
            "state": state,
            "district": district,
            "created_at": datetime.now()
        })
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('auth/signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate user and create session."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = db.users.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = str(user['_id'])
            session['name'] = user['name']
            session['role'] = user['role']
            session['state'] = user.get('state', '')
            session['district'] = user.get('district', '')
            flash("Welcome back, " + user['name'] + "!", "success")
            if user['role'] == 'farmer':
                return redirect(url_for('farmer_dashboard'))
            return redirect(url_for('buyer_dashboard'))
        flash("Invalid email or password.", "error")

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    """Clear session and redirect to landing page."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))


# ── Farmer Routes ─────────────────────────────────────────────────────────────

@app.route('/farmer/dashboard')
@login_required(role='farmer')
def farmer_dashboard():
    """Farmer overview: stats, activity chart, recent requests."""
    user_id = ObjectId(session['user_id'])
    now = datetime.now()

    total_listings = db.listings.count_documents({"farmer_id": user_id})
    active_listings = db.listings.count_documents({"farmer_id": user_id, "status": "active"})
    requests_received = db.requests.count_documents({"farmer_id": user_id})

    # Estimated revenue: sum(price_per_unit * quantity) for active listings
    pipeline = [
        {"$match": {"farmer_id": user_id, "status": "active"}},
        {"$group": {"_id": None, "total": {"$sum": {"$multiply": ["$price_per_unit", "$quantity"]}}}}
    ]
    rev_result = list(db.listings.aggregate(pipeline))
    est_revenue = int(rev_result[0]['total']) if rev_result else 0

    # Build month-by-month arrays for the Chart.js line graph
    labels = []
    listing_counts = []
    request_counts = []

    for i in range(5, -1, -1):
        month_start = (now.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        date_filter = {"$gte": month_start, "$lt": next_month}

        lc = db.listings.count_documents({"farmer_id": user_id, "created_at": date_filter})
        rc = db.requests.count_documents({"farmer_id": user_id, "created_at": date_filter})
        labels.append(month_start.strftime("%b %Y"))
        listing_counts.append(lc)
        request_counts.append(rc)

    monthly_data = {"labels": labels, "listings": listing_counts, "requests": request_counts}

    # Recent requests for the dashboard widget
    recent_reqs = list(
        db.requests.find({"farmer_id": user_id}).sort("created_at", -1).limit(5)
    )
    for req in recent_reqs:
        buyer = db.users.find_one({"_id": req['buyer_id']})
        listing = db.listings.find_one({"_id": req['listing_id']})
        req['buyer_name'] = buyer['name'] if buyer else 'Unknown'
        req['crop_name'] = listing['crop_name'] if listing else 'Unknown'
        req['quantity'] = req.get('quantity_requested', 0)
        req['_id'] = str(req['_id'])

    analytics = {
        "total_listings": total_listings,
        "active_listings": active_listings,
        "requests_received": requests_received,
        "est_revenue": "{:,}".format(est_revenue),
        "monthly_data": monthly_data,
        "recent_requests": recent_reqs
    }
    return render_template(
        'farmer/dashboard.html',
        analytics=analytics,
        current_date=now.strftime("%A, %d %B %Y")
    )


@app.route('/farmer/listings')
@login_required(role='farmer')
def farmer_listings():
    """Show all of the logged-in farmer's listings."""
    listings = list(
        db.listings
          .find({"farmer_id": ObjectId(session['user_id'])})
          .sort("created_at", -1)
    )
    return render_template('farmer/listings.html', listings=listings)


@app.route('/farmer/add-listing', methods=['GET', 'POST'])
@login_required(role='farmer')
def farmer_add_listing():
    """Create a new produce listing with optional photo upload."""
    if request.method == 'POST':
        crop_name = request.form.get('crop_name', '')
        quantity = float(request.form.get('quantity') or 0)
        unit = request.form.get('unit', 'kg')
        price_per_unit = float(request.form.get('price_per_unit') or 0)
        harvest_date_str = request.form.get('harvest_date', '')
        state = request.form.get('state', session.get('state', ''))
        district = request.form.get('district', session.get('district', ''))
        lat = float(request.form.get('lat') or 0.0)
        lng = float(request.form.get('lng') or 0.0)

        try:
            harvest_date = datetime.strptime(harvest_date_str, "%Y-%m-%d")
        except ValueError:
            harvest_date = datetime.now()

        # Handle optional photo upload
        photo_url = "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=400"
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ts = datetime.now().strftime('%Y%m%d%H%M%S')
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], ts + '_' + filename)
                file.save(save_path)
                photo_url = '/' + save_path.replace('\\', '/')

        listing = {
            "farmer_id": ObjectId(session['user_id']),
            "crop_name": crop_name,
            "quantity": quantity,
            "unit": unit,
            "price_per_unit": price_per_unit,
            "harvest_date": harvest_date,
            "state": state,
            "district": district,
            "lat": lat,
            "lng": lng,
            "photo_url": photo_url,
            "status": "active",
            "created_at": datetime.now()
        }
        db.listings.insert_one(listing)

        # Notify all buyers about the new listing
        for buyer in db.users.find({"role": "buyer"}):
            db.notifications.insert_one({
                "user_id": buyer['_id'],
                "message": "New crop listing: " + crop_name + " from " + state + " now available!",
                "status": "unread",
                "created_at": datetime.now()
            })

        flash("Listing added successfully!", "success")
        return redirect(url_for('farmer_listings'))

    return render_template('farmer/add_listing.html')


@app.route('/farmer/market-prices')
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
    )


@app.route('/farmer/requests')
@login_required(role='farmer')
def farmer_requests():
    """List all incoming buyer requests for this farmer."""
    farmer_id = ObjectId(session['user_id'])
    reqs = list(db.requests.find({"farmer_id": farmer_id}).sort("created_at", -1))
    for req in reqs:
        buyer = db.users.find_one({"_id": req['buyer_id']})
        listing = db.listings.find_one({"_id": req['listing_id']})
        req['buyer_name'] = buyer['name'] if buyer else 'Unknown Buyer'
        req['buyer_phone'] = buyer.get('phone', 'N/A') if buyer else 'N/A'
        req['crop_name'] = listing['crop_name'] if listing else 'Unknown Crop'
        req['listing_state'] = listing.get('state', '') if listing else ''
        req['_id'] = str(req['_id'])
    return render_template('farmer/requests.html', requests=reqs)


@app.route('/farmer/request-action', methods=['POST'])
@login_required(role='farmer')
def farmer_request_action():
    """Accept or reject a buyer request (AJAX endpoint)."""
    data = request.get_json()
    req_id = data.get('request_id')
    action = data.get('action')  # 'accepted' or 'rejected'

    req_obj = db.requests.find_one({"_id": ObjectId(req_id)})
    if req_obj and str(req_obj['farmer_id']) == session['user_id']:
        db.requests.update_one({"_id": ObjectId(req_id)}, {"$set": {"status": action}})
        db.notifications.insert_one({
            "user_id": req_obj['buyer_id'],
            "message": "Your request for " + session.get('name', 'the farmer') + "'s listing has been " + action + "!",
            "status": "unread",
            "created_at": datetime.now()
        })
        return jsonify({"success": True})

    return jsonify({"success": False}), 403


@app.route('/farmer/profile', methods=['GET', 'POST'])
@login_required(role='farmer')
def farmer_profile():
    """View and update farmer profile details."""
    user_id = ObjectId(session['user_id'])
    if request.method == 'POST':
        updates = {
            "name": request.form.get('name', ''),
            "phone": request.form.get('phone', ''),
            "state": request.form.get('state', ''),
            "district": request.form.get('district', '')
        }
        db.users.update_one({"_id": user_id}, {"$set": updates})
        session['name'] = updates['name']
        session['state'] = updates['state']
        session['district'] = updates['district']
        flash("Profile updated successfully.", "success")
        return redirect(url_for('farmer_profile'))
    user = db.users.find_one({"_id": user_id})
    return render_template('farmer/profile.html', user=user)


# ── Buyer Routes ──────────────────────────────────────────────────────────────

@app.route('/buyer/dashboard')
@login_required(role='buyer')
def buyer_dashboard():
    """Buyer overview: request counts and recent activity."""
    buyer_id = ObjectId(session['user_id'])
    total_requests = db.requests.count_documents({"buyer_id": buyer_id})
    recent_reqs = list(db.requests.find({"buyer_id": buyer_id}).sort("created_at", -1).limit(5))
    for req in recent_reqs:
        listing = db.listings.find_one({"_id": req['listing_id']})
        farmer = db.users.find_one({"_id": req['farmer_id']})
        req['crop_name'] = listing['crop_name'] if listing else 'Unknown'
        req['farmer_name'] = farmer['name'] if farmer else 'Unknown'
        req['_id'] = str(req['_id'])

    analytics = {
        "requests_sent": total_requests,
        "saved_listings": 3,
        "active_deals": 0
    }

    return render_template(
        'buyer/dashboard.html',
        analytics=analytics,
        recent_requests=recent_reqs
    )


@app.route('/buyer/marketplace')
@login_required(role='buyer')
def buyer_marketplace():
    """Browse all active listings with farmer info, ready for client-side filtering."""
    listings = list(db.listings.find({"status": "active"}).sort("created_at", -1))

    import time
    cache_buster = str(int(time.time()))
    
    # Enrich listings with farmer name and serialise ObjectIds / dates for JSON
    serialisable = []
    for l in listings:
        farmer = db.users.find_one({"_id": l['farmer_id']})
        hd = l.get('harvest_date')
        
        # Append cache buster to the photo URL so the browser downloads the new photos
        p_url = l.get('photo_url', '')
        if p_url and '?' in p_url:
            p_url += f"&cb={cache_buster}"
        elif p_url:
            p_url += f"?cb={cache_buster}"

        serialisable.append({
            "_id": str(l['_id']),
            "farmer_id": str(l['farmer_id']),
            "farmer_name": farmer['name'] if farmer else 'Unknown',
            "crop_name": l.get('crop_name', ''),
            "quantity": l.get('quantity', 0),
            "unit": l.get('unit', 'kg'),
            "price_per_unit": l.get('price_per_unit', 0),
            "state": l.get('state', ''),
            "district": l.get('district', ''),
            "lat": l.get('lat', 0.0),
            "lng": l.get('lng', 0.0),
            "photo_url": p_url,
            "harvest_date": hd.strftime("%Y-%m-%d") if isinstance(hd, datetime) else '',
            "status": l.get('status', 'active')
        })

    listings_json = json.dumps(serialisable)

    # Build flat {crop_name_lower: avg_price_per_kg} for "vs market" badge in JS
    flat_prices = {}
    try:
        json_path = os.path.join('static', 'data', 'mandi_prices.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            fallback = json.load(f)
        for crop_key, crop_data in fallback.get('crops', {}).items():
            flat_prices[crop_key] = crop_data.get('avg_price_per_kg', 0)
    except Exception:
        pass

    market_prices_json = json.dumps(flat_prices)

    return render_template(
        'buyer/marketplace.html',
        listings=serialisable,
        listings_json=listings_json,
        market_prices_json=market_prices_json
    )


@app.route('/buyer/send-interest', methods=['POST'])
@login_required(role='buyer')
def buyer_send_interest():
    """Record buyer's interest in a listing and notify the farmer (AJAX)."""
    data = request.get_json()
    listing_id = ObjectId(data.get('listing_id'))
    qty = float(data.get('quantity_requested', 0))
    message = data.get('message', '')

    listing = db.listings.find_one({"_id": listing_id})
    if not listing:
        return jsonify({"success": False, "message": "Listing not found"}), 404

    db.requests.insert_one({
        "buyer_id": ObjectId(session['user_id']),
        "farmer_id": listing['farmer_id'],
        "listing_id": listing_id,
        "quantity_requested": qty,
        "message": message,
        "status": "pending",
        "created_at": datetime.now()
    })

    buyer_name = session.get('name', 'A buyer')
    # Notify farmer
    db.notifications.insert_one({
        "user_id": listing['farmer_id'],
        "message": buyer_name + " sent a request for your " + listing['crop_name'] + " listing.",
        "status": "unread",
        "created_at": datetime.now()
    })
    # Confirm to buyer
    db.notifications.insert_one({
        "user_id": ObjectId(session['user_id']),
        "message": "Your interest in " + listing['crop_name'] + " has been sent to the farmer.",
        "status": "unread",
        "created_at": datetime.now()
    })

    return jsonify({"success": True, "message": "Interest sent successfully!"})


@app.route('/buyer/my-requests')
@login_required(role='buyer')
def buyer_my_requests():
    """Show all requests this buyer has made."""
    buyer_id = ObjectId(session['user_id'])
    reqs = list(db.requests.find({"buyer_id": buyer_id}).sort("created_at", -1))
    for req in reqs:
        listing = db.listings.find_one({"_id": req['listing_id']})
        farmer = db.users.find_one({"_id": req['farmer_id']})
        req['crop_name'] = listing['crop_name'] if listing else 'Unknown'
        req['state'] = listing.get('state', '') if listing else ''
        req['photo_url'] = listing.get('photo_url', '') if listing else ''
        req['farmer_name'] = farmer['name'] if farmer else 'Unknown'
        req['_id'] = str(req['_id'])
    return render_template('buyer/my_requests.html', requests=reqs)


@app.route('/buyer/saved')
@login_required(role='buyer')
def buyer_saved():
    """Show saved listings (demo: 3 random active listings)."""
    pipeline = [{"$match": {"status": "active"}}, {"$sample": {"size": 3}}]
    saved = list(db.listings.aggregate(pipeline))
    for l in saved:
        farmer = db.users.find_one({"_id": l['farmer_id']})
        l['farmer_name'] = farmer['name'] if farmer else 'Unknown'
        l['_id'] = str(l['_id'])
    return render_template('buyer/saved.html', listings=saved)


@app.route('/buyer/profile', methods=['GET', 'POST'])
@login_required(role='buyer')
def buyer_profile():
    """View and update buyer profile details."""
    user_id = ObjectId(session['user_id'])
    if request.method == 'POST':
        updates = {
            "name": request.form.get('name', ''),
            "phone": request.form.get('phone', ''),
            "state": request.form.get('state', ''),
            "district": request.form.get('district', '')
        }
        db.users.update_one({"_id": user_id}, {"$set": updates})
        session['name'] = updates['name']
        session['state'] = updates['state']
        session['district'] = updates['district']
        flash("Profile updated successfully.", "success")
        return redirect(url_for('buyer_profile'))
    user = db.users.find_one({"_id": user_id})
    return render_template('buyer/profile.html', user=user)


# ── API Endpoints ─────────────────────────────────────────────────────────────

@app.route('/api/listings')
def api_listings():
    """JSON feed of all active listings (used by Leaflet map)."""
    listings = list(db.listings.find({"status": "active"}))
    result = []
    for l in listings:
        farmer = db.users.find_one({"_id": l['farmer_id']})
        result.append({
            "_id": str(l['_id']),
            "crop_name": l.get('crop_name', ''),
            "quantity": l.get('quantity', 0),
            "unit": l.get('unit', 'kg'),
            "price_per_unit": l.get('price_per_unit', 0),
            "state": l.get('state', ''),
            "district": l.get('district', ''),
            "lat": l.get('lat', 0.0),
            "lng": l.get('lng', 0.0),
            "photo_url": l.get('photo_url', ''),
            "farmer_name": farmer['name'] if farmer else 'Unknown'
        })
    return jsonify(result)


@app.route('/api/notifications')
@login_required()
def api_notifications():
    """Poll endpoint for notification bell. Returns recent 10 and marks them read."""
    user_id = ObjectId(session['user_id'])
    notifs = list(
        db.notifications.find({"user_id": user_id}).sort("created_at", -1).limit(10)
    )
    unread_count = sum(1 for n in notifs if n.get('status') == 'unread')

    formatted = []
    for n in notifs:
        created = n.get('created_at', datetime.now())
        diff = datetime.now() - created
        if diff.total_seconds() < 3600:
            time_ago = str(int(diff.total_seconds() / 60)) + " min ago"
        elif diff.days == 0:
            time_ago = str(int(diff.total_seconds() / 3600)) + " hr ago"
        else:
            time_ago = str(diff.days) + " day(s) ago"

        formatted.append({
            "_id": str(n['_id']),
            "message": n.get('message', ''),
            "is_read": n.get('status') == 'read',
            "time_ago": time_ago
        })

    # Mark all as read after delivering
    db.notifications.update_many(
        {"user_id": user_id, "status": "unread"},
        {"$set": {"status": "read"}}
    )

    return jsonify({"notifications": formatted, "unread_count": unread_count})


@app.route('/api/market-prices')
def api_market_prices():
    """JSON endpoint for market prices (same logic as farmer tab)."""
    crop = request.args.get('crop', 'Wheat')
    state = request.args.get('state', 'Maharashtra')
    data = get_market_data(crop, state)
    return jsonify(data)


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Use the 'stat' reloader -- avoids WinError 10038 watchdog socket bug on Windows
    app.run(debug=True, port=5000, reloader_type='stat')
