from __future__ import annotations
from pathlib import Path
from datetime import datetime, timedelta
import hashlib, requests, re, feedparser
from selectolax.parser import HTMLParser
from ..schema import Opportunity

# Add council feeds or listing pages here
COUNCIL_SOURCES = [
    # Prefer RSS/Atom feeds if available
    {"name":"Auckland Council (tenders)", "type":"rss", "url":"https://www.aucklandcouncil.govt.nz/Lists/tenders/allitems.aspx?RSS=true"},
    # Fallback: HTML listing page (example placeholder; replace with real)
    {"name":"Wellington City (procurement)", "type":"html", "url":"https://wellington.govt.nz/your-council/suppliers/procurement"},
]

def _hash(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]

def fetch(raw_dir: Path) -> list[Opportunity]:
    out = []
    base_dir = Path(raw_dir) / "councils"
    base_dir.mkdir(parents=True, exist_ok=True)

    for src in COUNCIL_SOURCES:
        if src["type"] == "rss":
            out.extend(_fetch_rss(src, base_dir))
        elif src["type"] == "html":
            out.extend(_fetch_html(src, base_dir))
    return out

def _fetch_rss(src: dict, base_dir: Path):
    fp = feedparser.parse(src["url"])
    raw_path = base_dir / f"rss_{_hash(src['url'])}_{int(datetime.utcnow().timestamp())}.xml"
    if fp.get("feed"):  # write raw for audit
        raw_path.write_text(fp["feed"].get("title","") + "\n", encoding="utf-8")
    items = []
    for e in fp.entries[:100]:
        title = e.get("title","").strip()
        link = e.get("link")
        desc = (e.get("summary") or e.get("description") or "").strip()
        op_id = f"council:{_hash(link or title)}"
        items.append(Opportunity(
            op_id=op_id, source="council", title=title or "Untitled",
            org=src["name"], category="Local Government", description=desc,
            url=link, region="NZ", type="tender", pay_unit="NZD",
            close_at=datetime.utcnow()+timedelta(days=14), raw_path=str(raw_path)))
    return items

def _fetch_html(src: dict, base_dir: Path):
    r = requests.get(src["url"], timeout=20, headers={"User-Agent":"FINDR/0.1"})
    r.raise_for_status()
    raw_path = base_dir / f"html_{_hash(src['url'])}_{int(datetime.utcnow().timestamp())}.html"
    raw_path.write_text(r.text, encoding="utf-8")

    doc = HTMLParser(r.text)
    links = doc.css("a[href]")  # loose parse; refine selectors per site later
    items = []
    for a in links:
        href = a.attributes.get("href","")
        text = a.text(strip=True)
        if not text: 
            continue
        # Heuristic: include only tender/procurement-looking links
        if re.search(r"(tender|procure|contract|rfp|rft|rfq)", text, re.I):
            url = href if href.startswith("http") else _join(src["url"], href)
            op_id = f"council:{_hash(url)}"
            items.append(Opportunity(
                op_id=op_id, source="council", title=text,
                org=src["name"], category="Local Government",
                description=None, url=url, region="NZ", type="tender",
                pay_unit="NZD", close_at=datetime.utcnow()+timedelta(days=21),
                raw_path=str(raw_path)))
    return items

def _join(base: str, href: str) -> str:
    if href.startswith("/"):
        # simple host join
        from urllib.parse import urlparse
        p = urlparse(base)
        return f"{p.scheme}://{p.netloc}{href}"
    return href
