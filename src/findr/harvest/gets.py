from __future__ import annotations
from datetime import datetime, timedelta
from pathlib import Path
import re, hashlib, requests
from selectolax.parser import HTMLParser
from ..schema import Opportunity

BASE = "https://www.gets.govt.nz"  # page HTML is public; respect robots and ToS

def _hash(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]

def fetch(raw_dir: Path) -> list[Opportunity]:
    # NOTE: keep requests simple; if blocked, switch to cached snapshots or API if available.
    url = f"{BASE}/ExternalSearch.aspx?type=advanced&status=Open"
    r = requests.get(url, timeout=20, headers={"User-Agent":"FINDR/0.1"})
    r.raise_for_status()
    raw_dir = Path(raw_dir) / "gets"; raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"listing_{int(datetime.utcnow().timestamp())}.html"
    raw_path.write_text(r.text, encoding="utf-8")

    doc = HTMLParser(r.text)
    rows = doc.css("table tr")  # GETS uses tabular search results; adjust if structure shifts
    out: list[Opportunity] = []
    for tr in rows[1:]:
        tds = tr.css("td")
        if len(tds) < 4: 
            continue
        title_a = tds[0].css_first("a")
        title = title_a.text(strip=True) if title_a else tds[0].text(strip=True)
        href = title_a.attributes.get("href") if title_a else None
        detail_url = f"{BASE}/{href}" if href and not href.startswith("http") else href
        buyer = tds[1].text(strip=True)
        close_txt = tds[-1].text(strip=True)
        close_at = _parse_date(close_txt)

        op_id = f"gets:{_hash(detail_url or title)}"
        out.append(Opportunity(
            op_id=op_id,
            source="gets",
            title=title or "Untitled",
            org=buyer or None,
            category="Government",
            description=None,
            url=detail_url,
            region="NZ",
            type="tender",
            pay_unit="NZD",
            close_at=close_at,
            raw_path=str(raw_path),
            tags=[]
        ))
    return out

def _parse_date(s: str):
    # GETS often uses DD/MM/YYYY or ‘dd Mon yyyy’; be tolerant
    s = s.strip()
    for fmt in ("%d/%m/%Y", "%d %b %Y", "%d %B %Y"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass
    return datetime.utcnow() + timedelta(days=14)
