"""Resource Registry"""

from flask_restful import Resource

from resources.artists import Artists
from resources.songs import Songs

RESOURCE_REGISTRY: dict[Resource, str] = {
    Artists: "/artists",
    Songs: "/songs",
}
