from __future__ import annotations
from pathlib import Path
from datetime import datetime, timedelta
import hashlib, requests, re
from selectolax.parser import HTMLParser
from ..schema import Opportunity

BASE = "https://www.sjs.co.nz"

def _hash(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]

def fetch(raw_dir: Path) -> list[Opportunity]:
    """
    Scrapes SJS public listings page (no login). Structure can shift;
    this parser targets common card/list patterns. Respect robots/TOS.
    """
    url = f"{BASE}/jobs"
    r = requests.get(url, timeout=20, headers={"User-Agent":"FINDR/0.1"})
    r.raise_for_status()

    raw_dir = Path(raw_dir) / "sjs"; raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"listing_{int(datetime.utcnow().timestamp())}.html"
    raw_path.write_text(r.text, encoding="utf-8")

    doc = HTMLParser(r.text)
    cards = doc.css("[data-job-id], .job-card, article, li a[href*='/job/']")
    out = []
    for c in cards[:80]:
        a = c.css_first("a")
        if not a:
            continue
        title = a.text(strip=True)
        href = a.attributes.get("href") or ""
        detail_url = href if href.startswith("http") else f"{BASE}{href}"

        meta_text = c.text(separator=" ", strip=True)
        region = _pick_region(meta_text)
        pay_min, pay_max, unit = _extract_pay(meta_text)
        close_at = datetime.utcnow() + timedelta(days=7)

        op_id = f"sjs:{_hash(detail_url or title)}"
        out.append(Opportunity(
            op_id=op_id,
            source="sjs",
            title=title or "Untitled",
            org=None,
            category="Student/Casual",
            description=None,
            url=detail_url,
            region=region,
            type="job",
            pay_min=pay_min, pay_max=pay_max, pay_unit=unit,
            close_at=close_at,
            raw_path=str(raw_path),
            tags=["youth","student"]
        ))
    return out

def _pick_region(text: str) -> str | None:
    regions = ["Auckland","Wellington","Canterbury","Otago","Waikato","Bay of Plenty","Hawke's Bay","Manawatū","Taranaki","Nelson","Tasman","NZ"]
    t = text.lower()
    for r in regions:
        if r.lower() in t: return r
    return "NZ"

def _extract_pay(text: str):
    m = re.search(r"\$([\d,]+)(?:\s*-\s*\$([\d,]+))?\s*(per hour|hour|hr|weekly|week|pa|per annum|year)", text, re.I)
    if not m: return None, None, None
    p1 = float(m.group(1).replace(",",""))
    p2 = float(m.group(2).replace(",","")) if m.group(2) else p1
    return p1, p2, m.group(3).lower().replace("per ","")
