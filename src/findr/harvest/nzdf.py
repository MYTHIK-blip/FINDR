from __future__ import annotations
from pathlib import Path
from datetime import datetime, timedelta
import hashlib, requests, re
from selectolax.parser import HTMLParser
from ..schema import Opportunity

BASE = "https://www.defencecareers.mil.nz"  # NZDF Careers site

def _hash(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]

def fetch(raw_dir: Path) -> list[Opportunity]:
    """
    Pulls visible listings from NZDF careers search results.
    If structure changes, narrow selectors accordingly.
    """
    url = f"{BASE}/jobs/search/?location=new-zealand"
    r = requests.get(url, timeout=25, headers={"User-Agent":"FINDR/0.1"})
    r.raise_for_status()

    raw_dir = Path(raw_dir) / "nzdf"; raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"listing_{int(datetime.utcnow().timestamp())}.html"
    raw_path.write_text(r.text, encoding="utf-8")

    doc = HTMLParser(r.text)
    cards = doc.css("a[href*='/jobs/'], article a")
    out = []
    for a in cards[:80]:
        title = a.text(strip=True)
        href = a.attributes.get("href","")
        detail_url = href if href.startswith("http") else f"{BASE}{href}"

        meta_node = a.parent
        meta_text = meta_node.text(separator=" ", strip=True) if meta_node else ""
        region = _pick_region(meta_text)
        category = _pick_branch(meta_text)

        op_id = f"nzdf:{_hash(detail_url or title)}"
        out.append(Opportunity(
            op_id=op_id,
            source="nzdf",
            title=title or "Untitled",
            org="NZ Defence Force",
            category=category,
            description=None,
            url=detail_url,
            region=region,
            type="job",
            pay_unit="NZD",
            close_at=datetime.utcnow()+timedelta(days=21),
            raw_path=str(raw_path),
            tags=["security-clearance"] if "clearance" in meta_text.lower() else []
        ))
    return out

def _pick_region(text: str) -> str | None:
    for r in ("Auckland","Wellington","Canterbury","Manawatū","Otago","Bay of Plenty","NZ"):
        if r.lower() in text.lower(): return r
    return "NZ"

def _pick_branch(text: str) -> str | None:
    for b in ("Army","Navy","Air Force"):
        if b.lower() in text.lower(): return b
    return "Defence"
