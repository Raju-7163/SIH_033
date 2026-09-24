# FarmLink AI Improvements Implementation Plan

## Goal Description
Fix existing UI/UX bugs in the Farmer dashboard (My Listings buttons and Market Prices graph) and Buyer marketplace (Card layouts). Add dynamic inventory deduction upon order acceptance. Extend the logistics data model and UI to capture and display precise GPS coordinates (lat/lng) using Leaflet.js maps.

## User Review Required
> [!IMPORTANT]
> The exact location feature (Task 5) introduces a map picker on the `signup.html` page. New users will be required to click on a map to drop a pin for their location. Existing users will not have this data unless they update their profile (which will also get a map picker). Do you want existing users without lat/lng coordinates to default to a rough state/district center if they don't update their profile, or should we leave it blank? My plan defaults to district/state string if lat/lng is missing, preventing crashes.

## Proposed Changes

### Farmer Listings (UI & Logic)
- **Backend (`app.py`)**:
  - [NEW] Add route `POST /farmer/delete-listing/<id>` to remove a listing.
  - [NEW] Add route `POST /farmer/update-listing/<id>` to update listing fields.
- **Frontend (`templates/farmer/listings.html`)**:
  - [MODIFY] Wire the Edit and Delete buttons to Bootstrap modals/forms that call the new backend routes. Add confirmation prompts and proper POST/DELETE fetch handling.

### Market Prices Display
- **Frontend (`templates/farmer/market_prices.html`)**:
  - [MODIFY] Remove the `Chart.js` graph logic completely.
  - [MODIFY] Add a clear, accessible 3-column pricing card or table showing the selected crop's modal price per `1 kg`, `1 quintal (100 kg)`, and `1 tonne (1000 kg)`. Values will be extrapolated from the base `price_per_unit` (assuming the fetched API defaults to ₹/Quintal, which is typical for Agmarknet, I will normalize the math).

### Card Layout Refinements
- **Frontend (`static/js/marketplace.js` & `templates/farmer/listings.html`)**:
  - [MODIFY] Apply Bootstrap 5 layout classes (`text-truncate`, `object-fit-cover`, `flex-shrink-0`) to prevent text overflow when crop names or farmer names are excessively long. 
  - Ensure uniform image heights and proper badge positioning.

### Inventory Tracking on Order Acceptance
- **Backend (`app.py` - `farmer_request_action`)**:
  - [MODIFY] When `action == 'accepted'`, retrieve the original listing and deduct `quantity_requested`.
  - [MODIFY] If the remaining quantity <= 0, update the listing status to `sold`. 
- **Backend (`app.py` - `buyer_marketplace` / `api/listings`)**:
  - [MODIFY] Filter out `sold` listings from active queries so buyers cannot request them.
- **Frontend (`templates/farmer/listings.html`)**:
  - [MODIFY] Ensure the "Sold Out" badge styling works correctly and prevents edits on sold-out items.

### Precise Locations for Logistics
- **Frontend (`templates/auth/signup.html`, `templates/farmer/profile.html`, `templates/buyer/profile.html`)**:
  - [MODIFY] Add hidden `lat` and `lng` inputs.
  - [MODIFY] Include a Leaflet map where the user can drop a pin (or click "Use My Location").
- **Backend (`app.py` - `signup`, `farmer_profile`, `buyer_profile`)**:
  - [MODIFY] Parse and store `lat` and `lng` as floats in the `users` collection.
- **Frontend (`templates/logistics/available_deliveries.html`, `my_deliveries.html`)**:
  - [MODIFY] Instead of just text districts, embed a mini Leaflet map in each order card showing a marker for Pickup (`farmer_lat`, `farmer_lng`) and Drop (`buyer_lat`, `buyer_lng`) using `L.polyline`.

## Verification Plan
### Automated Tests
- Syntax check on `app.py`.

### Manual Verification
- Test Farmer deleting and editing a listing.
- View Market prices for clarity and accurate math.
- Test accepting a buyer request and verifying that the listing's quantity drops and status changes if depleted.
- Test signing up with a new user, picking a location, placing an order, and viewing that exact map pin on the logistics dashboard.

