// ===== NOTIFICATION POLLING =====
// Poll /api/notifications every 30 seconds
function pollNotifications() {
  if (!document.getElementById('notification-dropdown')) return;
  
  fetch('/api/notifications')
    .then(r => r.json())
    .then(data => {
      const badge = document.getElementById('notif-badge');
      const list = document.getElementById('notif-list');
      
      if (data.unread_count > 0) {
        badge.textContent = data.unread_count;
        badge.style.display = 'inline-block';
      } else {
        badge.style.display = 'none';
      }
      
      // Render notification items
      list.innerHTML = data.notifications.map(n => `
        <div class="notification-item ${n.is_read ? '' : 'unread'} p-3">
          <div class="d-flex align-items-start gap-2">
            <i class="bi bi-bell-fill text-success mt-1"></i>
            <div>
              <div class="small">${n.message}</div>
              <div class="text-muted" style="font-size:0.7rem">${n.time_ago}</div>
            </div>
          </div>
        </div>
      `).join('');
    })
    .catch(() => {}); // Silently fail
}

// ===== SCROLL ANIMATIONS =====
// Intersection Observer for .animate-on-scroll elements
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

// ===== STAT COUNTER ANIMATION =====
// Counts up numbers when they scroll into view
function animateCounter(el) {
  const target = parseInt(el.getAttribute('data-target'));
  const duration = 2000;
  const step = target / (duration / 16);
  let current = 0;
  const timer = setInterval(() => {
    current += step;
    if (current >= target) {
      el.textContent = target.toLocaleString('en-IN');
      clearInterval(timer);
    } else {
      el.textContent = Math.floor(current).toLocaleString('en-IN');
    }
  }, 16);
}

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
      entry.target.classList.add('counted');
      animateCounter(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-counter').forEach(el => counterObserver.observe(el));

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast-notification toast-${type}`;
  toast.innerHTML = `
    <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
    ${message}
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add('show'), 100);
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ===== MOBILE SIDEBAR TOGGLE =====
// Sidebar toggle is handled in base.html

// ===== LANGUAGE TOGGLE =====
const langBtn = document.getElementById('lang-toggle-btn');
if (langBtn) {
  langBtn.addEventListener('click', () => {
    const newLang = currentLang === 'en' ? 'hi' : 'en';
    applyTranslations(newLang);
  });
}

// ===== FLASH MESSAGE AUTO-DISMISS =====
setTimeout(() => {
  document.querySelectorAll('.alert-dismissible').forEach(el => {
    el.style.transition = 'opacity 0.5s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  });
}, 4000);

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  // Start notification polling if user is logged in
  if (document.getElementById('notification-dropdown')) {
    pollNotifications();
    setInterval(pollNotifications, 30000);
  }
});

// ===== CART LOGIC =====
function updateCartBadge(count) {
    const badge = document.getElementById('cart-badge');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline-block' : 'none';
    }
    const sidebarBadge = document.getElementById('sidebar-cart-badge');
    if (sidebarBadge) {
        sidebarBadge.textContent = count;
        sidebarBadge.style.display = count > 0 ? 'inline-block' : 'none';
    }
}

function openCartModal() {
    fetch('/api/cart')
        .then(r => r.json())
        .then(data => {
            if (!data.success) return;
            const container = document.getElementById('cart-items-container');
            if (data.cart.length === 0) {
                container.innerHTML = '<div class="text-center py-4 text-muted">Your cart is empty.</div>';
                document.getElementById('cart-total-price').textContent = '₹0';
            } else {
                container.innerHTML = data.cart.map(item => `
                    <div class="d-flex align-items-center gap-3 mb-3 pb-3 border-bottom cart-item">
                        <img src="${item.photo_url}" class="rounded" style="width: 60px; height: 60px; object-fit: cover;" onerror="this.src='/static/images/default-crop.jpg'">
                        <div class="flex-grow-1">
                            <h6 class="mb-0 fw-bold">${item.crop_name}</h6>
                            <small class="text-muted">${item.farmer_name}</small>
                            <div class="text-success small">₹${item.price_per_unit} / ${item.unit}</div>
                        </div>
                        <div class="text-end">
                            <div class="input-group input-group-sm mb-1" style="width: 100px;">
                                <input type="number" class="form-control text-center" value="${item.quantity}" min="1" max="${item.max_quantity}" onchange="updateCartQuantity('${item.listing_id}', this.value, ${item.max_quantity})">
                            </div>
                            <div class="text-primary fw-bold">₹${item.cost}</div>
                        </div>
                        <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeFromCart('${item.listing_id}')">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                `).join('');
                document.getElementById('cart-total-price').textContent = '₹' + data.total;
            }
            updateCartBadge(data.cart.length);
            const modal = new bootstrap.Modal(document.getElementById('cartModal'));
            modal.show();
        });
}

function removeFromCart(listingId) {
    fetch('/buyer/cart/remove', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ listing_id: listingId })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_count);
            // Re-render modal
            fetch('/api/cart').then(r => r.json()).then(d => {
                if (d.success && d.cart.length === 0) {
                    bootstrap.Modal.getInstance(document.getElementById('cartModal')).hide();
                } else if (d.success) {
                    const modalEl = document.getElementById('cartModal');
                    if(modalEl.classList.contains('show')) {
                        bootstrap.Modal.getInstance(modalEl).hide();
                        setTimeout(openCartModal, 400);
                    }
                }
            });
        }
    });
}

function updateCartQuantity(listingId, quantity, maxQty) {
    let q = parseInt(quantity);
    if (isNaN(q) || q <= 0) q = 1;
    if (q > maxQty) q = maxQty;
    
    fetch('/buyer/cart/update', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ listing_id: listingId, quantity: q })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(data.cart_count);
            // Re-render modal to show updated prices
            const modalEl = document.getElementById('cartModal');
            if(modalEl.classList.contains('show')) {
                bootstrap.Modal.getInstance(modalEl).hide();
                setTimeout(openCartModal, 400);
            }
        }
    });
}

function checkoutCart() {
    const btn = document.querySelector('#cartModal .btn-primary');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
    
    fetch('/buyer/checkout-all', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            updateCartBadge(0);
            bootstrap.Modal.getInstance(document.getElementById('cartModal')).hide();
            
            let msg = data.message;
            if (data.errors && data.errors.length > 0) {
                msg += '\nErrors: ' + data.errors.join(', ');
            }
            alert(msg);
            
            window.location.href = '/buyer/my-requests';
        } else {
            alert(data.message || 'Error checking out.');
        }
    })
    .catch(err => {
        console.error(err);
        alert('Network error.');
    })
    .finally(() => {
        btn.disabled = false;
        btn.textContent = 'Checkout All';
    });
}

// Fetch initial cart count
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('cart-badge')) {
        fetch('/api/cart')
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    updateCartBadge(data.cart.length);
                }
            });
    }
});
