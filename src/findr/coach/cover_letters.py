from __future__ import annotations
import json
from datetime import date
from ..schema import Opportunity

TEMPLATE = """{today}

Hiring Team — {org}

Re: {title}

Kia ora,

I’m writing to express interest in the {title} opportunity ({source}). My background includes:
{highlights}

I’m available {availability} and can start {start}. I value clear communication, safety, and results.
Thank you for your consideration.

Ngā mihi,
{name}
{email} · {phone}
"""

def build_cover_markdown(profile_path: str, op: Opportunity) -> str:
    prof = json.loads(open(profile_path,"r",encoding="utf-8").read())
    highlights = "\n".join([f"- {h}" for h in prof.get("highlights", prof.get("skills", [])[:5])])
    return TEMPLATE.format(
        today=str(date.today()),
        org=op.org or "the team",
        title=op.title,
        source=op.source,
        highlights=highlights or "- Fast learner; reliable; safety-first.",
        availability=prof.get("availability","weekdays"),
        start=prof.get("start","immediately"),
        name=prof.get("name","Your Name"),
        email=prof.get("contact",{}).get("email","you@example.com"),
        phone=prof.get("contact",{}).get("phone","+64-xxx"),
    )
