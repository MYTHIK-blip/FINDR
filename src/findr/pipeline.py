from pathlib import Path
from datetime import datetime
import json, duckdb
from typing import Iterable, Tuple
from .config import RAW, BRONZE, SILVER, GOLD, REPORTS
from .harvest import SOURCES
from .schema import Opportunity
from .scoring import load_rules, score
from .summarize import summarize
from .render.pdf import render_pdf
from .render.html import render_html
from .export.csv_export import export_csv
from .export.jsonl_export import export_jsonl
from .coach.cv_builder import build_cv_markdown
from .coach.cover_letters import build_cover_markdown

def _ensure_dirs():
    for d in (RAW, BRONZE, SILVER, GOLD, REPORTS):
        Path(d).mkdir(parents=True, exist_ok=True)

def _to_rows(ops: Iterable[Opportunity]):
    for o in ops:
        d = o.model_dump()
        d["close_at"] = d["close_at"].isoformat() if d["close_at"] else None
        yield d

def run_once(sources: Tuple[str, ...] = ("gets","trademe"), profile_path: str | None = None):
    _ensure_dirs()

    # 1) harvest
    harvested: list[Opportunity] = []
    for s in sources:
        harvested += SOURCES[s](RAW)

    # 2) bronze (normalized)
    ts = datetime.utcnow().isoformat().replace(":","-")
    bronze_parquet = BRONZE / f"bronze_{ts}.parquet"
    con = duckdb.connect()
    con.execute("""
        create table bronze as
        select * from (select * from read_json_auto(?))
    """, [json.dumps(list(_to_rows(harvested)))])
    con.execute("copy bronze to ? (format parquet)", [str(bronze_parquet)])

    # 3) silver (dedupe by op_id, latest wins)
    silver_parquet = SILVER / f"silver_{ts}.parquet"
    con.execute("""
        create table silver as
        select * from (
            select *, row_number() over (partition by op_id order by op_id) rn
            from bronze
        ) where rn=1
    """)
    con.execute("copy silver to ? (format parquet)", [str(silver_parquet)])

    # 4) score (gold)
    rows = con.execute("select * from silver").fetchall()
    cols = [c[0] for c in con.description]
    rules = load_rules()

    scored = []
    ops_by_id = {}
    for r in rows:
        d = dict(zip(cols, r))
        # reconstruct Opportunity safely
        o = Opportunity(
            op_id=d["op_id"], source=d["source"], title=d["title"], org=d.get("org"),
            category=d.get("category"), description=d.get("description"),
            url=d.get("url"), region=d.get("region"), type=d.get("type") or "job",
            pay_min=d.get("pay_min"), pay_max=d.get("pay_max"), pay_unit=d.get("pay_unit"),
            close_at=None, requirements=d.get("requirements") or [], tags=d.get("tags") or [],
            raw_path=d.get("raw_path")
        )
        ops_by_id[o.op_id] = o
        s = score(o, rules)
        scored.append({"op": o, "score": s.score, "explain": s.explain})

    # persist gold
    gold_ts = datetime.utcnow().isoformat().replace(":","-")
    csv_path = GOLD / f"gold_{gold_ts}.csv"
    jsonl_path = GOLD / f"gold_{gold_ts}.jsonl"
    export_csv([x["op"] for x in scored], str(csv_path))
    # add scores to jsonl records
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for x in scored:
            rec = x["op"].model_dump()
            rec["score"] = x["score"]
            rec["explain"] = x["explain"]
            f.write(json.dumps(rec, default=str) + "\n")

    # 5) human report (markdown → PDF/HTML)
    score_map = {x["op"].op_id: x["score"] for x in scored}
    md = summarize([x["op"] for x in scored], {k: type("S", (), {"score": v, "explain": []}) for k, v in score_map.items()})
    pdf_path = REPORTS / f"findr_{gold_ts}.pdf"
    html_path = REPORTS / f"findr_{gold_ts}.html"
    render_pdf(md, str(pdf_path))
    render_html(
        [
            {
                "title": x["op"].title, "org": x["op"].org, "source": x["op"].source,
                "region": x["op"].region, "type": x["op"].type, "pay_min": x["op"].pay_min,
                "pay_max": x["op"].pay_max, "pay_unit": x["op"].pay_unit,
                "close_at": x["op"].close_at, "description": x["op"].description,
                "score": x["score"], "explain": ", ".join(x["explain"])
            } for x in scored
        ],
        str(html_path)
    )

    # 6) optional: generate tailored CV/cover pack for first/top item
    pack_paths = {}
    if profile_path:
        try:
            top = max(scored, key=lambda x: x["score"])["op"]
            cv_md = build_cv_markdown(profile_path, top)
            cv_out = REPORTS / f"cv_{top.op_id}.md"
            cv_out.write_text(cv_md, encoding="utf-8")

            cover_md = build_cover_markdown(profile_path, top)
            cover_out = REPORTS / f"cover_{top.op_id}.md"
            cover_out.write_text(cover_md, encoding="utf-8")
            pack_paths = {"cv_md": str(cv_out), "cover_md": str(cover_out)}
        except Exception as e:
            # keep pipeline resilient
            pass

    con.close()
    return {
        "bronze": str(bronze_parquet),
        "silver": str(silver_parquet),
        "csv": str(csv_path),
        "jsonl": str(jsonl_path),
        "pdf": str(pdf_path),
        "html": str(html_path),
        **pack_paths
    }
