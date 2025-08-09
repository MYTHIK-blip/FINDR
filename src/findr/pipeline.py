from pathlib import Path
from datetime import datetime
from .config import RAW, GOLD, REPORTS
from .harvest import SOURCES
from .schema import Opportunity
from .scoring import load_rules, score
from .summarize import summarize
from .render.pdf import render_pdf
from .render.html import render_html
from .export.csv_export import export_csv
from .export.jsonl_export import export_jsonl

def run_once(sources=("gets","trademe")):
    # harvest (mock)
    harvested: list[Opportunity] = []
    for s in sources:
        harvested += SOURCES[s](RAW)

    # score
    rules = load_rules()
    scores = {o.op_id: score(o, rules) for o in harvested}

    # persist gold (simple filesystem for now)
    ts = datetime.utcnow().isoformat().replace(":","-")
    gold_dir = GOLD; gold_dir.mkdir(parents=True, exist_ok=True)
    csv_path = gold_dir/f"gold_{ts}.csv"
    jsonl_path = gold_dir/f"gold_{ts}.jsonl"
    export_csv(harvested, str(csv_path))
    export_jsonl(harvested, str(jsonl_path))

    # summarize + render
    md = summarize(harvested, scores)
    REPORTS.mkdir(parents=True, exist_ok=True)
    pdf_path = REPORTS/f"findr_{ts}.pdf"
    html_path = REPORTS/f"findr_{ts}.html"
    render_pdf(md, str(pdf_path))
    # also write a simple HTML for quick viewing
    items = [{"title":o.title,"org":o.org,"source":o.source,"region":o.region,"type":o.type,
              "pay_min":o.pay_min,"pay_max":o.pay_max,"pay_unit":o.pay_unit,
              "close_at":o.close_at,"description":o.description,
              "score":scores[o.op_id].score, "explain":", ".join(scores[o.op_id].explain)} for o in harvested]
    render_html(items, str(html_path))
    return {"csv": str(csv_path), "jsonl": str(jsonl_path), "pdf": str(pdf_path), "html": str(html_path)}
