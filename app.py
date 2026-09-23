"""
AgriConnect - Farmer to Buyer Marketplace
Main Flask application with all routes, authentication, and API endpoints.
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os
import json, bcrypt, requests as http_requests, json, uuid
import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from bson.json_util import dumps
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from functools import wraps
import config
from seed import seed_database

# ── App Initialization ──────────────────────────────────────────────────────

# Load crop images mapping
crop_images_map = {}
try:
    with open('static/data/crop_images.json', 'r', encoding='utf-8') as f:
        crop_images_map = json.load(f)
except Exception as e:
    print("Warning: Could not load crop_images.json", e)

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.jinja_env.globals.update(zip=zip)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ── MongoDB Connection ───────────────────────────────────────────────────────
try:
    client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000, tls=True, tlsAllowInvalidCertificates=True)
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
    """Register a new farmer, buyer, or logistics partner account."""
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role     = request.form.get('role', 'farmer')
        phone    = request.form.get('phone', '').strip()
        state    = request.form.get('state', '').strip()
        district = request.form.get('district', '').strip()
        aadhaar  = request.form.get('aadhaar', '').strip()
        
        try:
            lat = float(request.form.get('lat') or 0.0)
            lng = float(request.form.get('lng') or 0.0)
        except ValueError:
            lat, lng = 0.0, 0.0

        if db.users.find_one({"email": email}):
            flash("Email already registered.", "error")
            return redirect(url_for('signup'))

        # --- Aadhaar KYC handling ---
        # Validate: must be exactly 12 digits
        aadhaar_last4 = None
        aadhaar_hash  = None
        if aadhaar:
            if not aadhaar.isdigit() or len(aadhaar) != 12:
                flash("Aadhaar must be exactly 12 digits.", "error")
                return redirect(url_for('signup'))
            # Store only last 4 digits in plain text for display
            aadhaar_last4 = aadhaar[-4:]
            # Hash the full number — never stored or logged in raw form
            aadhaar_hash = bcrypt.hashpw(aadhaar.encode('utf-8'), bcrypt.gensalt())
        else:
            flash("Aadhaar number is required for registration.", "error")
            return redirect(url_for('signup'))

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.users.insert_one({
            "name":          name,
            "email":         email,
            "password":      hashed_pw,
            "role":          role,
            "phone":         phone,
            "state":         state,
            "district":      district,
            "lat":           lat,
            "lng":           lng,
            "aadhaar_last4": aadhaar_last4,   # for masked display (e.g. XXXX-XXXX-1234)
            "aadhaar_hash":  aadhaar_hash,    # full-number hash for future verification
            "created_at":    datetime.now()
        })
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('auth/signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate user and create session. Supports farmer, buyer, and logistics roles."""
    if request.method == 'POST':
        if db is None:
            flash("Database connection error: Please whitelist your IP in MongoDB Atlas.", "error")
            return render_template('auth/login.html')
            
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = db.users.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id']  = str(user['_id'])
            session['name']     = user['name']
            session['role']     = user['role']
            session['state']    = user.get('state', '')
            session['district'] = user.get('district', '')
            flash("Welcome back, " + user['name'] + "!", "success")
            # Route to the correct dashboard based on role
            if user['role'] == 'farmer':
                return redirect(url_for('farmer_dashboard'))
            elif user['role'] == 'logistics':
                return redirect(url_for('logistics_dashboard'))
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
    for l in listings:
        l['has_orders'] = db.orders.count_documents({"listing_id": l['_id']}) > 0

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
        photo_url = crop_images_map.get(crop_name, "/static/images/no-image.svg")
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


@app.route('/farmer/update-listing/<listing_id>', methods=['POST'])
@login_required(role='farmer')
def farmer_update_listing(listing_id):
    """Update an existing listing (quantity, price, unit, harvest_date)."""
    try:
        quantity = float(request.form.get('quantity') or 0)
        price_per_unit = float(request.form.get('price_per_unit') or 0)
        unit = request.form.get('unit', 'kg')
        harvest_date_str = request.form.get('harvest_date', '')
        
        try:
            harvest_date = datetime.strptime(harvest_date_str, "%Y-%m-%d")
        except ValueError:
            harvest_date = datetime.now()

        updates = {
            "quantity": quantity,
            "price_per_unit": price_per_unit,
            "unit": unit,
            "harvest_date": harvest_date
        }
        
        # If quantity > 0, set active. If <= 0, set sold.
        updates["status"] = "active" if quantity > 0 else "sold"

        result = db.listings.update_one(
            {"_id": ObjectId(listing_id), "farmer_id": ObjectId(session['user_id'])},
            {"$set": updates}
        )

        if result.modified_count > 0:
            flash("Listing updated successfully!", "success")
        else:
            flash("No changes made or listing not found.", "info")

    except Exception as e:
        app.logger.error(f"Error updating listing: {e}")
        flash("Failed to update listing.", "error")
        
    return redirect(url_for('farmer_listings'))


@app.route('/farmer/delete-listing/<listing_id>', methods=['POST'])
@login_required(role='farmer')
def farmer_delete_listing(listing_id):
    """Delete an existing listing (if owned by farmer)."""
    try:
        result = db.listings.delete_one({
            "_id": ObjectId(listing_id),
            "farmer_id": ObjectId(session['user_id'])
        })
        
        if result.deleted_count > 0:
            # Also optionally delete any pending requests for this listing so buyers don't get stuck
            db.requests.delete_many({"listing_id": ObjectId(listing_id), "status": "pending"})
            flash("Listing deleted successfully!", "success")
        else:
            flash("Listing not found or unauthorized.", "error")
            
    except Exception as e:
        app.logger.error(f"Error deleting listing: {e}")
        flash("Failed to delete listing.", "error")

    return redirect(url_for('farmer_listings'))



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
        # Contact reveal — only expose phone after acceptance (privacy guard)
        req['buyer_phone'] = buyer.get('phone', 'N/A') if (buyer and req.get('status') == 'accepted') else None
        req['crop_name'] = listing['crop_name'] if listing else 'Unknown Crop'
        req['listing_state'] = listing.get('state', '') if listing else ''
        req['quantity'] = req.get('quantity_requested', 0)
        req['unit'] = listing.get('unit', 'kg') if listing else 'kg'
        req['_id'] = str(req['_id'])
    return render_template('farmer/requests.html', requests=reqs)


@app.route('/farmer/request-action', methods=['POST'])
@login_required(role='farmer')
def farmer_request_action():
    """Accept or reject a buyer request (AJAX endpoint).
    On accept: also auto-creates a matching order document."""
    try:
        data = request.get_json()
        req_id = data.get('request_id')
        action = data.get('action')  # 'accepted' or 'rejected'

        if not req_id or action not in ('accepted', 'rejected'):
            return jsonify({"success": False, "message": "Invalid request data."}), 400

        req_obj = db.requests.find_one({"_id": ObjectId(req_id)})
        if not req_obj or str(req_obj['farmer_id']) != session['user_id']:
            return jsonify({"success": False, "message": "Request not found or unauthorized."}), 403

        # Update the request status
        db.requests.update_one({"_id": ObjectId(req_id)}, {"$set": {"status": action}})

        # --- Auto-create order on acceptance and deduct inventory ---
        # Wrapped separately so order creation failure doesn't block the status update
        if action == 'accepted':
            try:
                # Only create an order if one doesn't already exist for this request
                if not db.orders.find_one({"request_id": ObjectId(req_id)}):
                    listing = db.listings.find_one({"_id": req_obj['listing_id']})
                    price   = float(listing.get('price_per_unit', 0)) if listing else 0
                    qty     = float(req_obj.get('quantity_requested', 0))
                    total   = round(price * qty, 2)
                    crop    = listing['crop_name'] if listing else 'Unknown'
                    db.orders.insert_one({
                        "request_id":         ObjectId(req_id),
                        "buyer_id":           req_obj['buyer_id'],
                        "farmer_id":          req_obj['farmer_id'],
                        "listing_id":         req_obj['listing_id'],
                        "crop_name":          crop,
                        "quantity":           qty,
                        "total_amount":       total,
                        "payment_status":     "pending",     # buyer must pay to unlock logistics
                        "delivery_status":    "awaiting_payment",
                        "logistics_partner_id": None,
                        "created_at":         datetime.now()
                    })
                    
                    # Deduct inventory
                    if listing:
                        new_quantity = max(0, float(listing.get('quantity', 0)) - qty)
                        new_status = "active" if new_quantity > 0 else "sold"
                        db.listings.update_one(
                            {"_id": listing["_id"]},
                            {"$set": {"quantity": new_quantity, "status": new_status}}
                        )
            except Exception as order_err:
                app.logger.warning(f"Order auto-creation/inventory deduction failed for request {req_id}: {order_err}")

        # Notify the buyer — non-fatal if it fails
        try:
            listing = db.listings.find_one({"_id": req_obj['listing_id']})
            crop = listing['crop_name'] if listing else 'your crop'
            db.notifications.insert_one({
                "user_id":    req_obj['buyer_id'],
                "message":    f"Your request for {crop} has been {action} by {session.get('name', 'the farmer')}!",
                "status":     "unread",
                "created_at": datetime.now()
            })
        except Exception as notif_err:
            app.logger.warning(f"Notification insert failed for request {req_id}: {notif_err}")

        return jsonify({"success": True, "action": action})

    except Exception as e:
        app.logger.error(f"farmer_request_action error: {e}")
        return jsonify({"success": False, "message": "Server error. Please try again."}), 500


@app.route('/farmer/profile', methods=['GET', 'POST'])
@login_required(role='farmer')
def farmer_profile():
    """View and update farmer profile details."""
    user_id = ObjectId(session['user_id'])
    if request.method == 'POST':
        try:
            lat = float(request.form.get('lat') or 0.0)
            lng = float(request.form.get('lng') or 0.0)
        except ValueError:
            lat, lng = 0.0, 0.0

        updates = {
            "name": request.form.get('name', ''),
            "phone": request.form.get('phone', ''),
            "state": request.form.get('state', ''),
            "district": request.form.get('district', ''),
            "lat": lat,
            "lng": lng
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


from pymongo import ReturnDocument

@app.route('/buyer/cart/add', methods=['POST'])
@login_required(role='buyer')
def buyer_add_to_cart():
    """Add item to shopping cart in session."""
    data = request.get_json()
    listing_id = data.get('listing_id')
    quantity = int(data.get('quantity', 0))

    if not listing_id or quantity <= 0:
        return jsonify({"success": False, "message": "Invalid input data."}), 400

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    cart[listing_id] = cart.get(listing_id, 0) + quantity
    session.modified = True

    return jsonify({"success": True, "cart_count": len(cart)})

@app.route('/api/cart', methods=['GET'])
@login_required(role='buyer')
def api_get_cart():
    """Get all items currently in cart."""
    cart = session.get('cart', {})
    items = []
    total = 0
    for l_id, qty in list(cart.items()):
        listing = db.listings.find_one({"_id": ObjectId(l_id)})
        if not listing or listing['status'] != 'active' or listing['quantity'] <= 0:
            continue
            
        farmer = db.users.find_one({"_id": listing['farmer_id']})
        actual_qty = min(qty, listing.get('quantity', 0))
        cost = actual_qty * listing.get('price_per_unit', 0)
        total += cost
        
        items.append({
            "listing_id": l_id,
            "crop_name": listing.get('crop_name', ''),
            "quantity": actual_qty,
            "max_quantity": listing.get('quantity', 0),
            "unit": listing.get('unit', 'kg'),
            "price_per_unit": listing.get('price_per_unit', 0),
            "cost": cost,
            "photo_url": listing.get('photo_url', ''),
            "farmer_name": farmer['name'] if farmer else 'Unknown'
        })

    return jsonify({"success": True, "cart": items, "total": total})

@app.route('/buyer/cart/remove', methods=['POST'])
@login_required(role='buyer')
def buyer_remove_from_cart():
    data = request.get_json()
    listing_id = data.get('listing_id')
    cart = session.get('cart', {})
    if listing_id in cart:
        del cart[listing_id]
        session.modified = True
    return jsonify({"success": True, "cart_count": len(cart)})

@app.route('/buyer/cart/update', methods=['POST'])
@login_required(role='buyer')
def buyer_update_cart():
    data = request.get_json()
    listing_id = data.get('listing_id')
    quantity = int(data.get('quantity', 0))
    if not listing_id or quantity <= 0:
        return jsonify({"success": False, "message": "Invalid input."})
    
    cart = session.get('cart', {})
    if listing_id in cart:
        cart[listing_id] = quantity
        session.modified = True
    return jsonify({"success": True, "cart_count": len(cart)})

@app.route('/buyer/checkout-all', methods=['POST'])
@login_required(role='buyer')
def buyer_checkout_all():
    buyer_id = ObjectId(session['user_id'])
    cart = session.get('cart', {})
    if not cart:
        return jsonify({"success": False, "message": "Cart is empty."})
        
    success_count = 0
    errors = []
    
    for listing_id, quantity in list(cart.items()):
        try:
            updated_listing = db.listings.find_one_and_update(
                {"_id": ObjectId(listing_id), "quantity": {"$gte": quantity}, "status": "active"},
                {"$inc": {"quantity": -quantity}},
                return_document=ReturnDocument.AFTER
            )
            
            if not updated_listing:
                errors.append(f"Item unavailable or insufficient quantity for {listing_id}")
                continue
                
            if updated_listing['quantity'] <= 0:
                db.listings.update_one({"_id": ObjectId(listing_id)}, {"$set": {"status": "sold"}})
                
            req_result = db.requests.insert_one({
                "buyer_id": buyer_id,
                "farmer_id": updated_listing['farmer_id'],
                "listing_id": updated_listing['_id'],
                "quantity_requested": quantity,
                "message": "Cart Checkout",
                "status": "accepted",
                "created_at": datetime.now()
            })
            
            total_amount = quantity * updated_listing.get('price_per_unit', 0)
            db.orders.insert_one({
                "request_id": req_result.inserted_id,
                "buyer_id": buyer_id,
                "farmer_id": updated_listing['farmer_id'],
                "listing_id": updated_listing['_id'],
                "crop_name": updated_listing.get('crop_name', ''),
                "quantity": quantity,
                "total_amount": total_amount,
                "payment_status": "pending",
                "delivery_status": "awaiting_payment",
                "logistics_partner_id": None,
                "created_at": datetime.now()
            })
            
            db.notifications.insert_one({
                "user_id": updated_listing['farmer_id'],
                "message": f"Your {updated_listing.get('crop_name')} listing was just purchased — {quantity} {updated_listing.get('unit', 'kg')} via Checkout!",
                "status": "unread",
                "created_at": datetime.now()
            })
            
            success_count += 1
            del cart[listing_id]
        except Exception as e:
            errors.append(str(e))
            
    session.modified = True
    
    return jsonify({
        "success": True, 
        "message": f"Successfully checked out {success_count} items.", 
        "errors": errors,
        "cart_count": len(cart)
    })

@app.route('/buyer/buy-now', methods=['POST'])
@login_required(role='buyer')
def buyer_buy_now():
    """Instantly purchase a specific quantity from a single listing."""
    buyer_id = ObjectId(session['user_id'])
    data = request.get_json()
    listing_id = data.get('listing_id')
    quantity = int(data.get('quantity', 0))

    if not listing_id or quantity <= 0:
        return jsonify({"success": False, "message": "Invalid input data."}), 400

    try:
        # Atomic find and update: decrement quantity if enough is available and it's active
        updated_listing = db.listings.find_one_and_update(
            {"_id": ObjectId(listing_id), "quantity": {"$gte": quantity}, "status": "active"},
            {"$inc": {"quantity": -quantity}},
            return_document=ReturnDocument.AFTER
        )

        if not updated_listing:
            return jsonify({"success": False, "message": "Not enough inventory available, or listing sold out."}), 400

        # Mark sold if empty
        if updated_listing['quantity'] <= 0:
            db.listings.update_one({"_id": ObjectId(listing_id)}, {"$set": {"status": "sold"}})

        # Create 'accepted' request automatically
        req_doc = {
            "buyer_id": buyer_id,
            "farmer_id": updated_listing['farmer_id'],
            "listing_id": updated_listing['_id'],
            "quantity_requested": quantity,
            "message": "Instant Purchase (Buy Now)",
            "status": "accepted",
            "created_at": datetime.now()
        }
        req_result = db.requests.insert_one(req_doc)
        req_id = req_result.inserted_id

        # Auto-create order
        total_amount = quantity * updated_listing.get('price_per_unit', 0)
        db.orders.insert_one({
            "request_id": req_id,
            "buyer_id": buyer_id,
            "farmer_id": updated_listing['farmer_id'],
            "listing_id": updated_listing['_id'],
            "crop_name": updated_listing.get('crop_name', ''),
            "quantity": quantity,
            "total_amount": total_amount,
            "payment_status": "pending",
            "delivery_status": "awaiting_payment",
            "logistics_partner_id": None,
            "created_at": datetime.now()
        })

        # Notification
        db.notifications.insert_one({
            "user_id": updated_listing['farmer_id'],
            "message": f"Your {updated_listing.get('crop_name')} listing was just purchased — {quantity} {updated_listing.get('unit', 'kg')} by {session.get('name', 'a buyer')}!",
            "status": "unread",
            "created_at": datetime.now()
        })

        return jsonify({"success": True})

    except Exception as e:
        app.logger.error(f"buyer_buy_now error: {e}")
        return jsonify({"success": False, "message": "Server error. Please try again."}), 500


@app.route('/api/find-combinable-listings', methods=['GET'])
@login_required(role='buyer')
def find_combinable_listings():
    """Find a combination of listings that sums up to the required quantity."""
    crop_name = request.args.get('crop_name', '')
    req_qty = float(request.args.get('required_quantity', 0))
    state = request.args.get('state', '')

    # Fetch all active listings for this crop
    listings = list(db.listings.find({
        "crop_name": {"$regex": f"^{crop_name}$", "$options": "i"},
        "status": "active"
    }))

    if not listings:
        return jsonify({"success": False, "message": "No active listings found for this crop."})

    # Sort listings: prefer matching state first, then lowest price
    def sort_key(l):
        is_same_state = 0 if l.get('state', '').lower() == state.lower() else 1
        return (is_same_state, l.get('price_per_unit', float('inf')))

    listings.sort(key=sort_key)

    selected = []
    accumulated_qty = 0
    total_cost = 0

    for l in listings:
        if accumulated_qty >= req_qty:
            break
        
        farmer = db.users.find_one({"_id": l['farmer_id']})
        qty_available = l.get('quantity', 0)
        
        # Calculate how much we take from this listing
        qty_needed = req_qty - accumulated_qty
        qty_taken = min(qty_needed, qty_available)
        
        accumulated_qty += qty_taken
        cost = qty_taken * l.get('price_per_unit', 0)
        total_cost += cost
        
        selected.append({
            "listing_id": str(l['_id']),
            "farmer_name": farmer['name'] if farmer else 'Unknown',
            "quantity_taken": qty_taken,
            "total_quantity_available": qty_available,
            "price_per_unit": l.get('price_per_unit', 0),
            "district": l.get('district', ''),
            "state": l.get('state', ''),
            "photo_url": l.get('photo_url', '')
        })

    return jsonify({
        "success": True,
        "selected": selected,
        "total_quantity_covered": accumulated_qty,
        "total_estimated_cost": total_cost,
        "fully_covered": accumulated_qty >= req_qty
    })


@app.route('/api/create-pooled-request', methods=['POST'])
@login_required(role='buyer')
def create_pooled_request():
    """Create requests for a pooled order."""
    data = request.get_json()
    crop_name = data.get('crop_name', '')
    listing_ids = data.get('listing_ids', [])
    qty_taken_list = data.get('quantities', []) # Parallel array to listing_ids

    if not listing_ids:
        return jsonify({"success": False, "message": "No listings selected."}), 400

    pool_id = str(uuid.uuid4())
    buyer_id = ObjectId(session['user_id'])
    buyer_name = session.get('name', 'A buyer')
    
    total_qty = sum(qty_taken_list)

    for idx, l_id_str in enumerate(listing_ids):
        listing = db.listings.find_one({"_id": ObjectId(l_id_str)})
        if not listing:
            continue
            
        qty = float(qty_taken_list[idx])
        
        db.requests.insert_one({
            "pool_id": pool_id,
            "buyer_id": buyer_id,
            "farmer_id": listing['farmer_id'],
            "listing_id": listing['_id'],
            "quantity_requested": qty,
            "message": f"Part of a pooled order for {total_qty} units total.",
            "status": "pending",
            "created_at": datetime.now()
        })

        db.notifications.insert_one({
            "user_id": listing['farmer_id'],
            "message": f"{buyer_name} included your {listing['crop_name']} in a Pooled Order request.",
            "status": "unread",
            "created_at": datetime.now()
        })

    # Notify buyer
    db.notifications.insert_one({
        "user_id": buyer_id,
        "message": f"Your pooled order for {crop_name} has been sent to {len(listing_ids)} farmers.",
        "status": "unread",
        "created_at": datetime.now()
    })

    return jsonify({"success": True, "pool_id": pool_id})


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
    """Show all requests this buyer has made.
    Enriches each request with farmer contact (revealed on accept) and order/payment data."""
    buyer_id = ObjectId(session['user_id'])
    reqs = list(db.requests.find({"buyer_id": buyer_id}).sort("created_at", -1))

    standalone_requests = []
    pooled_requests_map = {}

    for req in reqs:
        listing = db.listings.find_one({"_id": req['listing_id']})
        farmer  = db.users.find_one({"_id": req['farmer_id']})
        req['crop_name']   = listing['crop_name'] if listing else 'Unknown'
        req['state']       = listing.get('state', '') if listing else ''
        req['photo_url']   = listing.get('photo_url', '') if listing else ''
        req['farmer_name'] = farmer['name'] if farmer else 'Unknown'
        # Contact reveal — only expose phone after acceptance (privacy guard)
        req['farmer_phone'] = farmer.get('phone', 'N/A') if (farmer and req.get('status') == 'accepted') else None
        req['_id'] = str(req['_id'])

        # Attach order/payment info if the request has been accepted
        # Graceful: requests with no matching order (e.g. pre-feature) skip payment UI
        order = db.orders.find_one({"request_id": ObjectId(req['_id'])}) if req.get('status') == 'accepted' else None
        if order:
            req['order_id']       = str(order['_id'])
            req['payment_status'] = order.get('payment_status', 'pending')
            req['total_amount']   = order.get('total_amount', 0)
            req['delivery_status'] = order.get('delivery_status', '')
        else:
            req['order_id']       = None
            req['payment_status'] = None
            req['total_amount']   = None

        pool_id = req.get('pool_id')
        if pool_id:
            if pool_id not in pooled_requests_map:
                pooled_requests_map[pool_id] = {
                    "pool_id": pool_id,
                    "crop_name": req['crop_name'],
                    "created_at": req['created_at'],
                    "total_quantity": 0,
                    "sub_requests": []
                }
            pooled_requests_map[pool_id]['total_quantity'] += req.get('quantity_requested', 0)
            pooled_requests_map[pool_id]['sub_requests'].append(req)
        else:
            standalone_requests.append(req)

    # Sort pooled requests by created_at descending
    pooled_requests = list(pooled_requests_map.values())
    pooled_requests.sort(key=lambda x: x['created_at'], reverse=True)

    return render_template('buyer/my_requests.html', requests=standalone_requests, pooled_requests=pooled_requests)


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
        try:
            lat = float(request.form.get('lat') or 0.0)
            lng = float(request.form.get('lng') or 0.0)
        except ValueError:
            lat, lng = 0.0, 0.0

        updates = {
            "name": request.form.get('name', ''),
            "phone": request.form.get('phone', ''),
            "state": request.form.get('state', ''),
            "district": request.form.get('district', ''),
            "lat": lat,
            "lng": lng
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

# ── Demo Payment API ──────────────────────────────────────────────────────────

@app.route('/api/pay-order', methods=['POST'])
@login_required(role='buyer')
def api_pay_order():
    """Demo payment endpoint — marks an order as paid.
    No real payment gateway. For hackathon demo only."""
    try:
        data     = request.get_json()
        order_id = data.get('order_id')
        if not order_id:
            return jsonify({"success": False, "message": "order_id required"}), 400

        order = db.orders.find_one({"_id": ObjectId(order_id)})
        if not order or str(order['buyer_id']) != session['user_id']:
            return jsonify({"success": False, "message": "Order not found or unauthorized"}), 403
        if order.get('payment_status') == 'paid':
            return jsonify({"success": True, "message": "Already paid"})

        # Mark as paid — now visible to logistics partners
        db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"payment_status": "paid", "delivery_status": "awaiting_pickup"}}
        )
        # Notify the farmer
        try:
            db.notifications.insert_one({
                "user_id":    order['farmer_id'],
                "message":    f"Payment received for your {order.get('crop_name', 'crop')} order! A logistics partner will be assigned soon.",
                "status":     "unread",
                "created_at": datetime.now()
            })
        except Exception:
            pass
        return jsonify({"success": True, "message": "Payment successful!"})
    except Exception as e:
        app.logger.error(f"api_pay_order error: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500


# ── Logistics Routes ──────────────────────────────────────────────────────────

@app.route('/logistics/dashboard')
@login_required(role='logistics')
def logistics_dashboard():
    """Logistics partner dashboard with summary stats."""
    partner_id = ObjectId(session['user_id'])
    total_available  = db.orders.count_documents({"payment_status": "paid", "logistics_partner_id": None})
    my_orders        = list(db.orders.find({"logistics_partner_id": partner_id}))
    in_transit_count = sum(1 for o in my_orders if o.get('delivery_status') == 'in_transit')
    delivered_count  = sum(1 for o in my_orders if o.get('delivery_status') == 'delivered')
    return render_template('logistics/dashboard.html',
                           total_available=total_available,
                           my_total=len(my_orders),
                           in_transit=in_transit_count,
                           delivered=delivered_count)


@app.route('/logistics/available-deliveries')
@login_required(role='logistics')
def logistics_available():
    """Show all paid orders without a logistics partner — available for pickup."""
    orders = list(db.orders.find({"payment_status": "paid", "logistics_partner_id": None}).sort("created_at", -1))
    enriched = []
    for o in orders:
        buyer  = db.users.find_one({"_id": o['buyer_id']})
        farmer = db.users.find_one({"_id": o['farmer_id']})
        enriched.append({
            "_id":            str(o['_id']),
            "crop_name":      o.get('crop_name', ''),
            "quantity":       o.get('quantity', 0),
            "total_amount":   o.get('total_amount', 0),
            "created_at":     o.get('created_at'),
            # Pickup = farmer location; Drop = buyer location
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
    return render_template('logistics/available_deliveries.html', orders=enriched)


@app.route('/logistics/accept-delivery', methods=['POST'])
@login_required(role='logistics')
def logistics_accept_delivery():
    """Logistics partner claims an available order."""
    try:
        data     = request.get_json()
        order_id = data.get('order_id')
        if not order_id:
            return jsonify({"success": False, "message": "order_id required"}), 400

        order = db.orders.find_one({"_id": ObjectId(order_id)})
        if not order:
            return jsonify({"success": False, "message": "Order not found"}), 404
        if order.get('logistics_partner_id'):
            return jsonify({"success": False, "message": "Already claimed by another partner"}), 409

        partner_id = ObjectId(session['user_id'])
        db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"logistics_partner_id": partner_id, "delivery_status": "picked_up"}}
        )
        # Notify buyer and farmer
        msg = f"Your {order.get('crop_name', 'crop')} order has been picked up by a logistics partner!"
        for uid in [order['buyer_id'], order['farmer_id']]:
            try:
                db.notifications.insert_one({"user_id": uid, "message": msg, "status": "unread", "created_at": datetime.now()})
            except Exception:
                pass
        return jsonify({"success": True})
    except Exception as e:
        app.logger.error(f"logistics_accept_delivery error: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500


@app.route('/logistics/my-deliveries')
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
    return render_template('logistics/my_deliveries.html', orders=enriched)


@app.route('/logistics/update-delivery-status', methods=['POST'])
@login_required(role='logistics')
def logistics_update_status():
    """Update delivery status for an order this partner has claimed."""
    try:
        data     = request.get_json()
        order_id = data.get('order_id')
        status   = data.get('status')  # 'in_transit' or 'delivered'
        valid_statuses = ('picked_up', 'in_transit', 'delivered')
        if not order_id or status not in valid_statuses:
            return jsonify({"success": False, "message": "Invalid data"}), 400

        partner_id = ObjectId(session['user_id'])
        order = db.orders.find_one({"_id": ObjectId(order_id), "logistics_partner_id": partner_id})
        if not order:
            return jsonify({"success": False, "message": "Order not found or not yours"}), 403

        db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"delivery_status": status}})

        # Notify buyer and farmer of status change
        status_label = {"picked_up": "Picked Up", "in_transit": "In Transit", "delivered": "Delivered"}[status]
        msg = f"Your {order.get('crop_name','crop')} order is now: {status_label}!"
        for uid in [order['buyer_id'], order['farmer_id']]:
            try:
                db.notifications.insert_one({"user_id": uid, "message": msg, "status": "unread", "created_at": datetime.now()})
            except Exception:
                pass
        return jsonify({"success": True})
    except Exception as e:
        app.logger.error(f"logistics_update_status error: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500


@app.route('/logistics/profile', methods=['GET', 'POST'])
@login_required(role='logistics')
def logistics_profile():
    """View and update logistics partner profile."""
    user_id = ObjectId(session['user_id'])
    if request.method == 'POST':
        updates = {
            "name":     request.form.get('name', ''),
            "phone":    request.form.get('phone', ''),
            "state":    request.form.get('state', ''),
            "district": request.form.get('district', '')
        }
        db.users.update_one({"_id": user_id}, {"$set": updates})
        session['name']     = updates['name']
        session['state']    = updates['state']
        session['district'] = updates['district']
        flash("Profile updated successfully.", "success")
        return redirect(url_for('logistics_profile'))
    user = db.users.find_one({"_id": user_id})
    return render_template('logistics/profile.html', user=user)


if __name__ == '__main__':
    # Use the 'stat' reloader -- avoids WinError 10038 watchdog socket bug on Windows
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, reloader_type='stat')

