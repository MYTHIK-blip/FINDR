from datetime import datetime
import yaml
from .schema import Opportunity, MatchResult

def load_rules(path="rules/scoring.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def score(op: Opportunity, rules) -> MatchResult:
    w = rules["weights"]; p = rules["params"]; kw = rules["keywords"]; acc = rules.get("access",{})
    text = " ".join([op.title or "", op.description or ""]).lower()

    def hit(keys): 
        return any(k.lower() in text for k in keys)

    skills = 1.0 if hit(kw["skills"]["include"]) and not hit(kw["skills"].get("exclude",[])) else 0.0

    pay_ok = 0.0
    if op.pay_unit and "hour" in op.pay_unit.lower():
        if (op.pay_min or 0) >= p["min_pay_hour"]:
            pay_ok = 1.0

    urgency = 0.0
    if op.close_at:
        days = (op.close_at - datetime.utcnow()).days
        urgency = 1.0 if days >= p["runway_min_days"] else 0.0

    access = 1.0 if any(t in (op.tags or []) for t in acc.get("friendly_tags",[])) else 0.0

    final = (w["skills"]*skills + w["pay"]*pay_ok + w["urgency"]*urgency + w["accessibility"]*access)
    explain = []
    explain += ["+skills"] if skills else []
    explain += ["+pay_floor"] if pay_ok else ["-pay_floor"]
    explain += ["+runway"] if urgency else ["-runway"]
    if access: explain += ["+access_friendly"]
    return MatchResult(op_id=op.op_id, score=round(final,3), explain=explain)
