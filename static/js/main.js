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
const sidebarToggle = document.getElementById('sidebar-toggle');
if (sidebarToggle) {
  sidebarToggle.addEventListener('click', () => {
    document.querySelector('.sidebar').classList.toggle('open');
  });
}

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
