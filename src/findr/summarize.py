from typing import List, Dict
from .schema import Opportunity, MatchResult

def summarize(ops: List[Opportunity], scores: Dict[str, MatchResult]) -> str:
    """Return a simple Markdown summary used by the PDF/HTML renderer."""
    lines = ["# FINDR Report", "", "## Top Opportunities", ""]
    top = sorted(ops, key=lambda o: scores[o.op_id].score if o.op_id in scores else 0, reverse=True)[:15]
    for o in top:
        s = scores.get(o.op_id)
        lines += [
            f"### {o.title} — {o.org or 'Unknown'}",
            f"- Source: **{o.source}** | Region: **{o.region or 'NZ'}** | Type: **{o.type}**",
            f"- Pay: {o.pay_min or '?'}–{o.pay_max or '?'} {o.pay_unit or ''} | Deadline: {o.close_at or 'n/a'}",
            f"- Score: **{s.score if s else 0}** | Explain: {', '.join(s.explain) if s else 'n/a'}",
            f"- URL: {o.url or 'n/a'}",
            f"- Summary: {(o.description or '')[:200]}",
            ""
        ]
    return "\n".join(lines)
