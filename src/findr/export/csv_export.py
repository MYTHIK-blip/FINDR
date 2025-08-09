import csv
from typing import List
from ..schema import Opportunity

def export_csv(rows: List[Opportunity], out_path: str):
    keys = ["op_id","source","title","org","category","region","type","pay_min","pay_max","pay_unit","close_at","url"]
    with open(out_path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            d=r.model_dump()
            d["close_at"]=d["close_at"].isoformat() if d["close_at"] else None
            w.writerow({k:d.get(k) for k in keys})
