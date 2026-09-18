// ===== ACTIVITY LINE CHART =====
function initActivityChart(monthlyData) {
  const ctx = document.getElementById('activityChart');
  if (!ctx) return;
  
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: monthlyData.labels,
      datasets: [{
        label: 'Listings Created',
        data: monthlyData.listings,
        borderColor: '#2d6a4f',
        backgroundColor: 'rgba(45,106,79,0.1)',
        borderWidth: 3,
        pointBackgroundColor: '#2d6a4f',
        pointRadius: 6,
        fill: true,
        tension: 0.4
      }, {
        label: 'Requests Received',
        data: monthlyData.requests,
        borderColor: '#d4a373',
        backgroundColor: 'rgba(212,163,115,0.1)',
        borderWidth: 3,
        pointBackgroundColor: '#d4a373',
        pointRadius: 6,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' },
        tooltip: { mode: 'index', intersect: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(0,0,0,0.05)' },
          ticks: { stepSize: 1 }
        },
        x: { grid: { display: false } }
      }
    }
  });
}

// ===== MARKET PRICES BAR CHART =====
function initMarketChart(marketData) {
  const ctx = document.getElementById('marketChart');
  if (!ctx || !marketData) return;
  
  const suggestedPrice = marketData.avg_price;
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: marketData.labels,
      datasets: [{
        label: 'Modal Price (₹/quintal)',
        data: marketData.prices,
        backgroundColor: marketData.prices.map(p =>
          p >= suggestedPrice ? 'rgba(45,106,79,0.8)' : 'rgba(212,163,115,0.8)'
        ),
        borderColor: marketData.prices.map(p =>
          p >= suggestedPrice ? '#2d6a4f' : '#d4a373'
        ),
        borderWidth: 2,
        borderRadius: 8,
      }, {
        label: 'Average Price',
        data: new Array(marketData.labels.length).fill(suggestedPrice),
        type: 'line',
        borderColor: '#e63946',
        borderWidth: 2,
        borderDash: [5, 5],
        pointRadius: 0,
        fill: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top' },
        tooltip: {
          callbacks: {
            label: (ctx) => `₹${ctx.parsed.y}/quintal`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          grid: { color: 'rgba(0,0,0,0.05)' },
          ticks: { callback: v => '₹' + v }
        },
        x: { grid: { display: false } }
      }
    }
  });
}

// ===== REQUEST ACCEPT/REJECT =====
function handleRequestAction(requestId, action) {
  const btn = document.querySelector(`[data-request-id="${requestId}"][data-action="${action}"]`);
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
  }
  
  fetch('/farmer/request-action', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ request_id: requestId, action: action })
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      showToast(`Request ${action} successfully!`, 'success');
      // Update UI
      const card = document.querySelector(`[data-request-card="${requestId}"]`);
      if (card) {
        const badge = card.querySelector('.request-status-badge');
        badge.className = `badge request-status-badge bg-${action === 'accepted' ? 'success' : 'danger'}`;
        badge.textContent = action.charAt(0).toUpperCase() + action.slice(1);
        card.querySelectorAll('.action-btn').forEach(b => b.remove());
      }
    } else {
      showToast('Action failed. Please try again.', 'error');
      if (btn) { btn.disabled = false; btn.innerHTML = action === 'accepted' ? 'Accept' : 'Reject'; }
    }
  })
  .catch(() => {
    showToast('Network error. Please try again.', 'error');
    if (btn) { btn.disabled = false; }
  });
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  // Initialize charts if data is available
  if (window.monthlyData) initActivityChart(window.monthlyData);
  if (window.marketData) initMarketChart(window.marketData);
  
  // Attach request action handlers
  document.querySelectorAll('.action-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      handleRequestAction(btn.getAttribute('data-request-id'), btn.getAttribute('data-action'));
    });
  });
});
