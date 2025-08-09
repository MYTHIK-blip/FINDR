from __future__ import annotations
import time, logging
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse
from urllib import robotparser
import requests

UA = "FINDR/0.1 (+local; respectful; contact: ops@localhost)"
logger = logging.getLogger("findr.http")

@dataclass
class HttpConfig:
    timeout: int = 20
    max_retries: int = 3
    backoff: float = 1.5
    respect_robots: bool = True
    user_agent: str = UA

_rp_cache: dict[str, robotparser.RobotFileParser] = {}

def _robots_allowed(url: str, ua: str) -> bool:
    try:
        parts = urlparse(url)
        base = f"{parts.scheme}://{parts.netloc}"
        if base not in _rp_cache:
            rp = robotparser.RobotFileParser()
            rp.set_url(f"{base}/robots.txt")
            rp.read()
            _rp_cache[base] = rp
        return _rp_cache[base].can_fetch(ua, url)
    except Exception:
        # If robots fails, err on the safe side: disallow.
        return False

def http_get(url: str, cfg: Optional[HttpConfig] = None) -> requests.Response:
    cfg = cfg or HttpConfig()
    if cfg.respect_robots and not _robots_allowed(url, cfg.user_agent):
        raise PermissionError(f"robots.txt disallows GET {url}")

    headers = {"User-Agent": cfg.user_agent}
    last_exc = None
    for attempt in range(1, cfg.max_retries + 1):
        try:
            r = requests.get(url, headers=headers, timeout=cfg.timeout)
            r.raise_for_status()
            return r
        except Exception as e:
            last_exc = e
            logger.warning("GET failed; retrying", extra={"attempt": attempt, "url": url})
            if attempt == cfg.max_retries:
                break
            time.sleep(cfg.backoff ** attempt)
    # Exhausted
    raise last_exc  # type: ignore[misc]
