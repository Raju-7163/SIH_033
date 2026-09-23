filepath = 'app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_insights = '''    ai_insights = {
        'trend_dir': trend_dir,
        'trend_pct': round(trend_pct, 1),
        'insight': trend_insight,
        'demand_level': demand_level,
        'advisory': None
    }'''

new_insights = '''    ai_insights = {
        'trend_dir': trend_dir,
        'trend_pct': round(trend_pct, 1),
        'insight': trend_insight,
        'demand_level': demand_level,
        'demand_qty': demand_qty,
        'supply_qty': supply_qty,
        'advisory': None
    }'''

content = content.replace(old_insights, new_insights)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
