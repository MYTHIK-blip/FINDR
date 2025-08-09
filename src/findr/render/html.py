from jinja2 import Template

TEMPLATE = Template("""
<!doctype html><meta charset="utf-8">
<style>
body{font-family:system-ui,Segoe UI,Arial;margin:24px;line-height:1.35}
h1{margin-bottom:0} h2{margin-top:24px}
.card{border:1px solid #ddd;padding:12px;border-radius:8px;margin:8px 0}
.meta{color:#555;font-size:0.9em}
</style>
<h1>FINDR Report</h1>
<p class="meta">Generated locally</p>
{% for item in items %}
<div class="card">
  <h3>{{item.title}} — {{item.org or 'Unknown'}}</h3>
  <div class="meta">Source: <b>{{item.source}}</b> | Region: <b>{{item.region or 'NZ'}}</b> | Type: <b>{{item.type}}</b></div>
  <div class="meta">Pay: {{item.pay_min or '?' }}–{{item.pay_max or '?' }} {{item.pay_unit or ''}} |
      Deadline: {{item.close_at or 'n/a'}} | Score: <b>{{item.score}}</b> ({{item.explain}})</div>
  <div>{{item.description[:300] if item.description else ''}}</div>
</div>
{% endfor %}
""")

def render_html(items, out_path: str):
    html = TEMPLATE.render(items=items)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
