from datetime import datetime, timedelta
from ..schema import Opportunity

def fetch(raw_dir):
    # TODO: replace with real GETS scraping
    return [Opportunity(
        op_id="gets:12345",
        source="gets",
        title="Data Platform & Dashboard Services",
        org="Sample NZ Agency",
        category="IT services",
        description="Seeking dashboards, ETL; resilience reporting.",
        region="NZ",
        type="tender",
        pay_min=30000.0, pay_max=120000.0, pay_unit="NZD",
        close_at=datetime.utcnow()+timedelta(days=14),
        tags=["AI","dashboard"]
    )]
