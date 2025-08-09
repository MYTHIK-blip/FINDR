from src.findr.pipeline import run_once
def test_smoke():
    out = run_once(("gets","trademe"))
    assert "csv" in out and "pdf" in out
