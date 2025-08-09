from __future__ import annotations
from datetime import datetime, timedelta
from pathlib import Path
import re, hashlib, requests
from selectolax.parser import HTMLParser
from ..schema import Opportunity

BASE = "https://www.trademe.co.nz/a/jobs/search?sort_order=expiry_desc"  # public listing page

def _hash(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]

def fetch(raw_dir: Path) -> list[Opportunity]:
    r = requests.get(BASE, timeout=20, headers={"User-Agent":"FINDR/0.1"})
    r.raise_for_status()
    raw_dir = Path(raw_dir) / "trademe"; raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"listing_{int(datetime.utcnow().timestamp())}.html"
    raw_path.write_text(r.text, encoding="utf-8")

    doc = HTMLParser(r.text)
    cards = doc.css("[data-automation-id='jobCard']") or doc.css("tm-job-card, article")
    out = []
    for c in cards[:50]:
        title = (c.css_first("a") or c.css_first("h3")).text(strip=True) if c.css_first("a") else c.text(strip=True)[:80]
        href = c.css_first("a").attributes.get("href") if c.css_first("a") else None
        detail_url = href if (href and href.startswith("http")) else (f"https://www.trademe.co.nz{href}" if href else None)
        meta = c.text(separator=" ", strip=True)
        region = _extract_region(meta)
        pay_min, pay_max, unit = _extract_pay(meta)

        op_id = f"trademe:{_hash(detail_url or title)}"
        out.append(Opportunity(
            op_id=op_id,
            source="trademe",
            title=title or "Untitled",
            org=None,
            category=None,
            description=None,
            url=detail_url,
            region=region,
            type="job",
            pay_min=pay_min, pay_max=pay_max, pay_unit=unit,
            close_at=datetime.utcnow() + timedelta(days=10),
            raw_path=str(raw_path),
            tags=[]
        ))
    return out

def _extract_region(text: str) -> str|None:
    for r in ("Auckland","Wellington","Canterbury","Otago","Waikato","Bay of Plenty","Hawke's Bay","Northland","NZ"):
        if r.lower() in text.lower(): return r
    return None

def _extract_pay(text: str):
    m = re.search(r"\$([\d,]+)(?:\s*-\s*\$([\d,]+))?\s*(per hour|hour|hr|per annum|pa|salary|year)", text, re.I)
    if not m: return None, None, None
    p1 = float(m.group(1).replace(",",""))
    p2 = float(m.group(2).replace(",","")) if m.group(2) else p1
    unit = m.group(3).lower().replace("per ","")
    return p1, p2, unit
