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
  .then(r => {
    // Always parse JSON — backend now always returns JSON, even on errors
    return r.json().then(data => ({ ok: r.ok, data }));
  })
  .then(({ ok, data }) => {
    if (ok && data.success) {
      showToast(`Request ${action} successfully!`, 'success');

      // Update the status badge in-place on the card
      const card = document.querySelector(`[data-request-card="${requestId}"]`);
      if (card) {
        // Find and update the status badge (inside .status-container)
        const statusContainer = card.querySelector('.status-container');
        if (statusContainer) {
          const isAccepted = action === 'accepted';
          statusContainer.innerHTML = isAccepted
            ? `<span class="badge bg-success-subtle text-success-emphasis rounded-pill px-3 py-2 border border-success-subtle fw-medium"><i class="bi bi-check-circle-fill me-1"></i>Accepted</span>`
            : `<span class="badge bg-danger-subtle text-danger-emphasis rounded-pill px-3 py-2 border border-danger-subtle fw-medium"><i class="bi bi-x-circle-fill me-1"></i>Rejected</span>`;
        }
        // Remove the accept/reject buttons
        const actionBtns = card.querySelector('.action-buttons');
        if (actionBtns) actionBtns.remove();
      }
    } else {
      const msg = (data && data.message) ? data.message : 'Action failed. Please try again.';
      showToast(msg, 'error');
      // Re-enable the button
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = action === 'accepted'
          ? '<i class="bi bi-check-lg me-1"></i> Accept'
          : '<i class="bi bi-x-lg me-1"></i> Reject';
      }
    }
  })
  .catch(err => {
    // Only fires on genuine network failures (offline, CORS, etc.)
    console.error('Request action network error:', err);
    showToast('Network error. Please check your connection.', 'error');
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = action === 'accepted'
        ? '<i class="bi bi-check-lg me-1"></i> Accept'
        : '<i class="bi bi-x-lg me-1"></i> Reject';
    }
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
