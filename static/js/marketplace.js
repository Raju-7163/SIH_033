// All listings data injected from Flask template into window.allListings
// All market prices injected into window.marketPrices as flat {crop: avg_price_per_kg}

let filteredListings = [];
let map = null;
let markers = [];

// ===== FILTER LOGIC =====
function filterListings() {
  const searchVal = document.getElementById('search-input').value.toLowerCase().trim();
  const stateVal  = document.getElementById('state-filter').value;   // "all" or state name
  const cropVal   = document.getElementById('crop-filter').value;    // "all" or crop name
  const maxPrice  = parseInt(document.getElementById('price-range').value);
  const desiredQtyInput = document.getElementById('desired-qty');
  const desiredQty = desiredQtyInput && desiredQtyInput.value ? parseInt(desiredQtyInput.value) : 0;

  // Update the live price display label
  if (document.getElementById('price-display')) {
      document.getElementById('price-display').textContent = '₹' + maxPrice;
  }

  filteredListings = window.allListings.filter(l => {
    const matchSearch = !searchVal ||
      l.crop_name.toLowerCase().includes(searchVal) ||
      (l.district || '').toLowerCase().includes(searchVal) ||
      l.state.toLowerCase().includes(searchVal);
    // "all" means no filter applied
    const matchState  = stateVal === 'all' || !stateVal || l.state === stateVal;
    const matchCrop   = cropVal  === 'all' || !cropVal  || l.crop_name.toLowerCase() === cropVal.toLowerCase();
    const matchPrice  = l.price_per_unit <= maxPrice;
    return matchSearch && matchState && matchCrop && matchPrice;
  });

  // Check if we need to show the pooled order banner
  const banner = document.getElementById('pooled-order-banner');
  if (banner) {
    if (desiredQty > 0 && cropVal !== 'all') {
        const totalAvailable = filteredListings.reduce((sum, l) => sum + (l.quantity || 0), 0);
        const maxSingle = filteredListings.length > 0 ? Math.max(...filteredListings.map(l => l.quantity || 0)) : 0;
        
        // Show banner if desired qty is greater than what any single farmer has, 
        // AND there are actually other farmers to combine with (totalAvailable > maxSingle)
        if (desiredQty > maxSingle && totalAvailable > maxSingle) {
            banner.classList.remove('d-none');
            banner.setAttribute('data-crop', cropVal);
            banner.setAttribute('data-qty', desiredQty);
            banner.setAttribute('data-state', stateVal === 'all' ? '' : stateVal);
        } else {
            banner.classList.add('d-none');
        }
    } else {
        banner.classList.add('d-none');
    }
  }

  renderCards();
  if (map) renderMapPins();
  document.getElementById('results-count').textContent = filteredListings.length + ' listings found';
}


// ===== CARD RENDERER =====
function renderCards() {
  const grid = document.getElementById('listings-grid');
  
  if (filteredListings.length === 0) {
    grid.innerHTML = `
      <div class="col-12 text-center py-5">
        <i class="bi bi-search" style="font-size:3rem;color:#aaa"></i>
        <p class="mt-3 text-muted">No listings match your filters</p>
      </div>`;
    return;
  }
  
  grid.innerHTML = filteredListings.map(listing => {
    // Compare price to market average
    const marketKey = listing.crop_name.toLowerCase();
    const marketAvg = window.marketPrices[marketKey] || null;
    let badge = '';
    if (marketAvg) {
      const diff = ((listing.price_per_unit - marketAvg) / marketAvg * 100).toFixed(1);
      if (listing.price_per_unit <= marketAvg * 1.05) {
        badge = `<span class="badge badge-fair"><i class="bi bi-check-circle"></i> Fair Price (${diff > 0 ? '+' : ''}${diff}%)</span>`;
      } else {
        badge = `<span class="badge badge-overpriced"><i class="bi bi-arrow-up"></i> +${diff}% above market</span>`;
      }
    }
    
    return `
      <div class="col-md-6 col-lg-4 animate-on-scroll">
        <div class="listing-card card h-100">
          <div class="position-relative">
            <img src="${listing.photo_url}" class="card-img-top" alt="${listing.crop_name}"
              onerror="this.src='https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=400'">
            <span class="position-absolute top-0 end-0 m-2 badge bg-success">${listing.crop_name}</span>
          </div>
          <div class="card-body d-flex flex-column">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="card-title mb-0 fw-bold text-truncate pe-2" title="${listing.crop_name}">${listing.crop_name}</h5>
              <div class="flex-shrink-0">${badge}</div>
            </div>
            <div class="mb-2 text-truncate">
              <span class="fs-4 fw-bold text-success">₹${listing.price_per_unit}</span>
              <span class="text-muted">/${listing.unit}</span>
            </div>
            <div class="text-muted small mb-1 text-truncate" title="${listing.quantity} ${listing.unit} available"><i class="bi bi-boxes"></i> ${listing.quantity} ${listing.unit} available</div>
            <div class="text-muted small mb-1 text-truncate" title="${listing.district}, ${listing.state}"><i class="bi bi-geo-alt"></i> ${listing.district}, ${listing.state}</div>
            <div class="text-muted small mb-3 text-truncate" title="${listing.farmer_name}"><i class="bi bi-person"></i> ${listing.farmer_name}</div>
            <div class="mt-auto d-flex gap-2">
              <button class="btn btn-primary flex-grow-1" onclick="openBuyNowModal('${listing._id}', '${listing.crop_name}', ${listing.quantity}, '${listing.unit}', ${listing.price_per_unit})">
                <i class="bi bi-cart-check"></i> Buy Now
              </button>
              <button class="btn btn-outline-primary" title="Send Interest" onclick="openInterestModal('${listing._id}', '${listing.crop_name}', ${listing.quantity}, '${listing.unit}')">
                <i class="bi bi-send"></i>
              </button>
            </div>
          </div>
        </div>
      </div>`;
  }).join('');
  
  // Re-trigger scroll animations for newly rendered cards
  document.querySelectorAll('.animate-on-scroll:not(.visible)').forEach(el => {
    if (typeof observer !== 'undefined') observer.observe(el);
    else el.classList.add('visible'); // Fallback: show immediately
  });
}

// ===== MAP =====
function initMap() {
  if (map) return;
  map = L.map('map').setView([20.5937, 78.9629], 5); // India center
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);
  
  renderMapPins();
}

function renderMapPins() {
  markers.forEach(m => m.remove());
  markers = [];
  
  filteredListings.forEach(listing => {
    if (!listing.lat || !listing.lng) return;
    
    const marketKey = listing.crop_name.toLowerCase();
    const marketAvg = window.marketPrices[marketKey] || null;
    const isFair = !marketAvg || listing.price_per_unit <= marketAvg * 1.05;
    
    const icon = L.divIcon({
      html: `<div style="background:${isFair ? '#2d6a4f' : '#e63946'};width:36px;height:36px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);border:3px solid white;box-shadow:0 3px 10px rgba(0,0,0,0.3)"></div>`,
      iconSize: [36, 36],
      iconAnchor: [18, 36],
      className: ''
    });
    
    const marker = L.marker([listing.lat, listing.lng], { icon })
      .addTo(map)
      .bindPopup(`
        <div class="map-popup">
          <img src="${listing.photo_url}" alt="${listing.crop_name}"
            onerror="this.src='https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=400'">
          <h6 class="mt-2 mb-1">${listing.crop_name}</h6>
          <div><strong>₹${listing.price_per_unit}/${listing.unit}</strong></div>
          <div class="text-muted small">${listing.district}, ${listing.state}</div>
          <div class="text-muted small">${listing.quantity} ${listing.unit}</div>
          <button class="btn btn-sm btn-success mt-2 w-100" 
            onclick="openInterestModal('${listing._id}', '${listing.crop_name}', ${listing.quantity}, '${listing.unit}')">Send Interest</button>
        </div>
      `, { maxWidth: 200 });
    
    markers.push(marker);
  });
}

// ===== VIEW TOGGLE =====
function toggleView(view) {
  const gridView = document.getElementById('grid-view');
  const mapView = document.getElementById('map-view');
  const gridBtn = document.getElementById('btn-grid');
  const mapBtn = document.getElementById('btn-map');
  
  if (view === 'map') {
    gridView.classList.add('d-none');
    mapView.classList.remove('d-none');
    gridBtn.classList.remove('active');
    mapBtn.classList.add('active');
    setTimeout(initMap, 100); // Wait for div to be visible
  } else {
    mapView.classList.add('d-none');
    gridView.classList.remove('d-none');
    mapBtn.classList.remove('active');
    gridBtn.classList.add('active');
  }
}

// ===== INTEREST MODAL =====
function openInterestModal(listingId, cropName, maxQty, unit) {
  document.getElementById('modal-listing-id').value = listingId;
  document.getElementById('modal-crop-name').textContent = cropName;
  document.getElementById('modal-max-qty').textContent = maxQty + ' ' + unit;
  document.getElementById('modal-qty-input').max = maxQty;
  const modal = new bootstrap.Modal(document.getElementById('interestModal'));
  modal.show();
}

function submitInterest() {
  const listingId = document.getElementById('modal-listing-id').value;
  const qty = document.getElementById('modal-qty-input').value;
  const msg = document.getElementById('modal-message').value;
  const btn = document.getElementById('submit-interest-btn');
  
  if (!qty || !msg) {
    showToast('Please fill in all fields', 'error');
    return;
  }
  
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Sending...';
  
  fetch('/buyer/send-interest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ listing_id: listingId, quantity_requested: parseInt(qty), message: msg })
  })
  .then(r => r.json())
  .then(data => {
    bootstrap.Modal.getInstance(document.getElementById('interestModal')).hide();
    showToast(data.message || 'Interest sent successfully!', 'success');
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-send"></i> Send Interest';
  })
  .catch(() => {
    showToast('Failed to send interest. Please try again.', 'error');
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-send"></i> Send Interest';
  });
}

// ===== BUY NOW MODAL =====
function openBuyNowModal(listingId, cropName, maxQty, unit, pricePerUnit) {
  document.getElementById('buy-modal-listing-id').value = listingId;
  document.getElementById('buy-modal-crop-name').textContent = cropName;
  document.getElementById('buy-modal-max-qty').textContent = maxQty + ' ' + unit;
  document.getElementById('buy-modal-price').textContent = pricePerUnit;
  document.getElementById('buy-modal-price-hidden').value = pricePerUnit;
  document.getElementById('buy-modal-unit').textContent = unit;
  
  const qtyInput = document.getElementById('buy-modal-qty-input');
  qtyInput.max = maxQty;
  qtyInput.value = '';
  document.getElementById('buy-modal-total').textContent = '0';
  
  qtyInput.addEventListener('input', function() {
    let q = parseInt(this.value) || 0;
    if (q > maxQty) q = maxQty;
    document.getElementById('buy-modal-total').textContent = q * pricePerUnit;
  });

  const modal = new bootstrap.Modal(document.getElementById('buyNowModal'));
  modal.show();
}

function submitBuyNow() {
  const listingId = document.getElementById('buy-modal-listing-id').value;
  const qty = parseInt(document.getElementById('buy-modal-qty-input').value);
  const maxQty = parseInt(document.getElementById('buy-modal-qty-input').max);
  const btn = document.getElementById('submit-buynow-btn');
  
  if (!qty || qty <= 0) {
    showToast('Please enter a valid quantity.', 'error');
    return;
  }
  if (qty > maxQty) {
    showToast(`Quantity cannot exceed ${maxQty}.`, 'error');
    return;
  }
  
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
  
  fetch('/buyer/buy-now', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ listing_id: listingId, quantity: qty })
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      bootstrap.Modal.getInstance(document.getElementById('buyNowModal')).hide();
      showToast('Purchase confirmed! Redirecting...', 'success');
      setTimeout(() => {
        window.location.href = '/buyer/my-requests';
      }, 1500);
    } else {
      showToast(data.message || 'Failed to complete purchase.', 'error');
      btn.disabled = false;
      btn.innerHTML = '<i class="bi bi-cart-check me-2"></i> Confirm Purchase';
    }
  })
  .catch(() => {
    showToast('Network error. Please try again.', 'error');
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-cart-check me-2"></i> Confirm Purchase';
  });
}

// ===== COMBINE LISTINGS LOGIC =====
let currentPooledSelection = {
  crop_name: '',
  quantities: [],
  listing_ids: []
};

function openCombineModal() {
  const banner = document.getElementById('pooled-order-banner');
  const crop = banner.getAttribute('data-crop');
  const qty = banner.getAttribute('data-qty');
  const state = banner.getAttribute('data-state');
  
  document.getElementById('combine-crop-name').textContent = crop;
  document.getElementById('combine-target-qty').textContent = qty;
  document.getElementById('combine-listings-container').innerHTML = '<div class="text-center py-4"><span class="spinner-border"></span><p class="mt-2 text-muted">Finding best combination...</p></div>';
  
  const modal = new bootstrap.Modal(document.getElementById('combineListingsModal'));
  modal.show();

  fetch(`/api/find-combinable-listings?crop_name=${encodeURIComponent(crop)}&required_quantity=${qty}&state=${encodeURIComponent(state)}`)
    .then(r => r.json())
    .then(data => {
      if (!data.success) {
        document.getElementById('combine-listings-container').innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        return;
      }
      
      const warning = document.getElementById('combine-partial-warning');
      if (!data.fully_covered) {
        warning.classList.remove('d-none');
      } else {
        warning.classList.add('d-none');
      }
      
      document.getElementById('combine-total-cost').textContent = data.total_estimated_cost;
      document.getElementById('combine-farmer-count').textContent = data.selected.length;
      
      currentPooledSelection.crop_name = crop;
      currentPooledSelection.listing_ids = data.selected.map(s => s.listing_id);
      currentPooledSelection.quantities = data.selected.map(s => s.quantity_taken);
      
      const container = document.getElementById('combine-listings-container');
      container.innerHTML = data.selected.map(s => `
        <div class="card border-0 shadow-sm rounded-3 bg-white">
          <div class="card-body d-flex align-items-center">
            <div class="rounded-3 overflow-hidden me-3" style="width: 50px; height: 50px; background-color: #e9ecef;">
              <img src="${s.photo_url}" class="w-100 h-100 object-fit-cover" onerror="this.style.display='none'">
            </div>
            <div class="flex-grow-1">
              <h6 class="fw-bold mb-1">${s.farmer_name}</h6>
              <div class="small text-muted"><i class="bi bi-geo-alt"></i> ${s.district}, ${s.state}</div>
            </div>
            <div class="text-end">
              <div class="fw-bold text-dark">${s.quantity_taken} units</div>
              <div class="small text-muted">@ ₹${s.price_per_unit}/unit</div>
            </div>
          </div>
        </div>
      `).join('');
    })
    .catch(e => {
      document.getElementById('combine-listings-container').innerHTML = `<div class="alert alert-danger">Error fetching data.</div>`;
    });
}

function submitCombineRequest() {
  const btn = document.getElementById('submit-combine-btn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Sending...';
  
  fetch('/api/create-pooled-request', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      crop_name: currentPooledSelection.crop_name,
      listing_ids: currentPooledSelection.listing_ids,
      quantities: currentPooledSelection.quantities
    })
  })
  .then(r => r.json())
  .then(data => {
    bootstrap.Modal.getInstance(document.getElementById('combineListingsModal')).hide();
    showToast('Pooled order sent successfully!', 'success');
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-send me-2"></i> Send Pooled Request';
  })
  .catch(() => {
    showToast('Failed to send pooled order.', 'error');
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-send me-2"></i> Send Pooled Request';
  });
}

// ===== EVENT LISTENERS =====
document.addEventListener('DOMContentLoaded', () => {
  filteredListings = window.allListings || [];

  // Initialize price display to match slider default
  const priceSlider = document.getElementById('price-range');
  if (priceSlider) {
    document.getElementById('price-display').textContent = '₹' + priceSlider.value;
  }

  renderCards();

  document.getElementById('search-input').addEventListener('input', filterListings);
  document.getElementById('state-filter').addEventListener('change', filterListings);
  document.getElementById('crop-filter').addEventListener('change', filterListings);
  document.getElementById('price-range').addEventListener('input', filterListings);
  
  const desiredQtyInput = document.getElementById('desired-qty');
  if (desiredQtyInput) {
    desiredQtyInput.addEventListener('input', filterListings);
  }
  
  const combineBannerBtn = document.getElementById('btn-open-combine-modal');
  if (combineBannerBtn) {
    combineBannerBtn.addEventListener('click', openCombineModal);
  }
  
  const submitCombineBtn = document.getElementById('submit-combine-btn');
  if (submitCombineBtn) {
    submitCombineBtn.addEventListener('click', submitCombineRequest);
  }
  
  document.getElementById('btn-map').addEventListener('click', () => toggleView('map'));
  document.getElementById('btn-grid').addEventListener('click', () => toggleView('grid'));
  document.getElementById('submit-interest-btn').addEventListener('click', submitInterest);

  // Reset all filters
  const resetBtn = document.getElementById('reset-filters');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      document.getElementById('search-input').value = '';
      document.getElementById('state-filter').value = 'all';
      document.getElementById('crop-filter').value = 'all';
      document.getElementById('price-range').value = document.getElementById('price-range').max;
      if (document.getElementById('desired-qty')) {
        document.getElementById('desired-qty').value = '';
      }
      filterListings();
    });
  }

  document.getElementById('results-count').textContent = filteredListings.length + ' listings found';
});

