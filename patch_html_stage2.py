import os

filepath = 'templates/logistics/my_deliveries.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

opt_ui = '''{% if optimized_route %}
<!-- STAGE 2: Route Optimization UI -->
<div class="card border-0 shadow-sm rounded-4 mb-4 border-start border-4 border-warning">
    <div class="card-body p-4 bg-warning-subtle rounded-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="fw-bold text-dark mb-0"><i class="bi bi-magic text-warning fs-4 me-2"></i>AI Route Optimization</h5>
            <button class="btn btn-warning rounded-pill fw-medium" type="button" data-bs-toggle="collapse" data-bs-target="#optimizedRouteMap">
                View Optimized Route
            </button>
        </div>
        <p class="mb-0 text-dark">Estimated distance saved: <strong>{{ optimized_route.saved_km }} km</strong> (Original: {{ optimized_route.orig_dist }} km, Optimized: {{ optimized_route.opt_dist }} km)</p>
        
        <div class="collapse mt-3" id="optimizedRouteMap">
            <div class="row g-4">
                <div class="col-md-5">
                    <ol class="list-group list-group-numbered list-group-flush bg-transparent">
                        {% for stop in optimized_route.stops %}
                        <li class="list-group-item bg-transparent border-bottom border-warning-subtle py-2">
                            <span class="fw-medium">{{ stop.name }}</span>
                            <span class="badge {% if stop.type == 'pickup' %}bg-warning text-dark{% else %}bg-success{% endif %} float-end rounded-pill">{{ stop.type | title }}</span>
                        </li>
                        {% endfor %}
                    </ol>
                </div>
                <div class="col-md-7">
                    <div id="ai-opt-map" class="border border-warning rounded-3" style="height: 300px;"></div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}
'''

if 'AI Route Optimization' not in content:
    content = content.replace('{% if orders %}\n<div class="d-flex flex-column gap-4">', '{% if orders %}\n' + opt_ui + '\n<div class="d-flex flex-column gap-4">')

opt_js = '''
{% if optimized_route %}
    const optCollapse = document.getElementById('optimizedRouteMap');
    if (optCollapse) {
        optCollapse.addEventListener('shown.bs.collapse', function () {
            if (window.optMapInitialized) return;
            window.optMapInitialized = true;
            
            const map = L.map('ai-opt-map');
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
            
            const stops = {{ optimized_route.stops | tojson | safe }};
            const latlngs = [];
            const bounds = L.latLngBounds();
            
            stops.forEach((stop, i) => {
                const pt = [stop.lat, stop.lng];
                latlngs.push(pt);
                bounds.extend(pt);
                const marker = L.marker(pt).addTo(map);
                marker.bindPopup('<b>Stop ' + (i+1) + ':</b> ' + stop.name);
            });
            
            L.polyline(latlngs, {color: '#d97706', weight: 4}).addTo(map);
            if(stops.length > 0) {
                map.fitBounds(bounds, {padding: [20, 20]});
            }
        });
    }
{% endif %}
'''

if 'optMapInitialized' not in content:
    content = content.replace('document.addEventListener(\'DOMContentLoaded\', () => {', 'document.addEventListener(\'DOMContentLoaded\', () => {\n' + opt_js)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched my_deliveries.html for Stage 2")
