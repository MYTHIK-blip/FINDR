from .gets import fetch as gets_fetch
from .trademe import fetch as trademe_fetch

SOURCES = {
    "gets": gets_fetch,
    "trademe": trademe_fetch,
}
