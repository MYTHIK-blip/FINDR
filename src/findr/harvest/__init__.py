from .gets import fetch as gets_fetch
from .trademe import fetch as trademe_fetch
from .sjs import fetch as sjs_fetch
from .nzdf import fetch as nzdf_fetch
from .councils import fetch as councils_fetch

SOURCES = {
    "gets": gets_fetch,
    "trademe": trademe_fetch,
    "sjs": sjs_fetch,
    "nzdf": nzdf_fetch,
    "councils": councils_fetch,
}
