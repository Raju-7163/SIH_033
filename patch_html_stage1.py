import os

filepath = 'templates/farmer/market_prices.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

ai_insights_html = '''
    {% if ai_insights %}
    <!-- STAGE 1 & 3: AI-Powered Market Insights -->
    <div class="card border-0 shadow-sm rounded-4 mb-4 border-start border-4 border-info">
        <div class="card-body p-4 bg-info-subtle rounded-4">
            <h5 class="fw-bold text-dark mb-3"><i class="bi bi-robot text-info fs-4 me-2"></i>AI-Powered Market Insights</h5>
            <div class="row g-4">
                <div class="col-md-4">
                    <h6 class="text-muted fw-bold mb-1">Price Trend</h6>
                    <p class="fs-5 fw-bold mb-0 {% if ai_insights.trend_pct > 0 %}text-success{% elif ai_insights.trend_pct < 0 %}text-danger{% else %}text-secondary{% endif %}">
                        {{ ai_insights.trend_dir }} 
                        {% if ai_insights.trend_pct != 0 %}({{ ai_insights.trend_pct }}%){% endif %}
                    </p>
                    <small class="text-dark">{{ ai_insights.insight }}</small>
                </div>
                <div class="col-md-4">
                    <h6 class="text-muted fw-bold mb-1">Demand Level</h6>
                    <p class="fs-5 fw-bold mb-0 {% if 'High' in ai_insights.demand_level %}text-danger{% else %}text-primary{% endif %}">
                        {{ ai_insights.demand_level }}
                    </p>
                    <small class="text-dark">Requested: {{ ai_insights.demand_qty }} kg | Available: {{ ai_insights.supply_qty }} kg</small>
                </div>
                <div class="col-md-4">
                    <h6 class="text-muted fw-bold mb-1">Gemini AI Advisory</h6>
                    {% if ai_insights.advisory %}
                        <p class="mb-0 text-dark fst-italic">"{{ ai_insights.advisory }}"</p>
                    {% else %}
                        <p class="mb-0 text-dark fst-italic">"{{ ai_insights.insight }}"</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    {% endif %}
'''

if 'AI-Powered Market Insights' not in content:
    content = content.replace('<div class="row g-4 justify-content-center">', ai_insights_html + '\n    <div class="row g-4 justify-content-center">')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched market_prices.html")
