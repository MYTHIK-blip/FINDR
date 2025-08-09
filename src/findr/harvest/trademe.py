from datetime import datetime, timedelta
from ..schema import Opportunity

def fetch(raw_dir):
    # TODO: replace with real Trade Me Jobs adapter
    return [Opportunity(
        op_id="trademe:abc",
        source="trademe",
        title="Junior Python Developer",
        org="Local SME",
        category="Software",
        description="Entry-level role; Docker, FastAPI nice-to-have.",
        region="Auckland",
        type="job",
        pay_min=28.0, pay_max=40.0, pay_unit="NZD/hour",
        close_at=datetime.utcnow()+timedelta(days=10),
        tags=["python","docker","fastapi"]
    )]
