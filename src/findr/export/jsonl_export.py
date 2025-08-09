import json
from typing import List
from ..schema import Opportunity

def export_jsonl(rows: List[Opportunity], out_path: str):
    with open(out_path,"w",encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r.model_dump(), default=str)+"\n")
