"""Resource Registry"""

from resources.artists import Artists
from resources.songs import Songs

RESOURCE_REGISTRY = {
    "artists": Artists,
    "songs": Songs,
}
