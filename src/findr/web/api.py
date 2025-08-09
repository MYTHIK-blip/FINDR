from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from glob import glob
from ..config import GOLD, REPORTS
from ..pipeline import run_once

app = FastAPI(title="FINDR API", version="0.1")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/run")
def run(sources: str = "gets,trademe,sjs,nzdf,councils"):
    names = tuple(s.strip() for s in sources.split(",") if s.strip())
    out = run_once(names)
    return out

@app.get("/gold/latest")
def gold_latest():
    paths = sorted(glob(str(GOLD / "gold_*.jsonl")))
    if not paths:
        raise HTTPException(404, "No gold files yet")
    latest = paths[-1]
    return FileResponse(latest, media_type="application/json", filename=Path(latest).name)

@app.get("/report/latest")
def report_latest():
    paths = sorted(glob(str(REPORTS / "findr_*.pdf")))
    if not paths:
        raise HTTPException(404, "No reports yet")
    latest = paths[-1]
    return FileResponse(latest, media_type="application/pdf", filename=Path(latest).name)

@app.get("/gold/list")
def gold_list():
    files = [Path(p).name for p in sorted(glob(str(GOLD / "gold_*.jsonl")))]
    return JSONResponse(files)
