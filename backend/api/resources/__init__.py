"""The resources package contains all code related to API resources"""

from resources.artists import Artists
from resources.songs import Songs

# Holds a registry of all resources and their associated paths. The registry is
# defined as a dict[Resource, str], where the str is the resource path. The
# resource registry is sourced from the main server program which registers the
# resources with the flask API instance. To register a new resource with the API,
# simply add the appropriate mapping to the resource registry.
RESOURCE_REGISTRY: dict = {
    Artists: "/artists",
    Songs: "/songs",
}
