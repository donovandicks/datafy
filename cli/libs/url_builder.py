"""Defines a URL Builder class"""

from typing import Any


class URLBuilder:
    """Builds an API endpoint URL"""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.resource = None
        self.params = []

    def with_resource(self, resource: str):
        """Adds an API resource to the URL

        Params
        ------
        resource: str
            the name of the API resource to include in the URL, e.g. 'artists'
        """
        if self.resource:
            raise AttributeError("Resource already set")

        self.resource = resource
        return self

    def with_param(self, key: str, value: Any):
        """Adds a query parameter to the URL

        Ex:
        ```
        limit=20
        ```
        where 'limit' is the key and 20 is the value

        Params
        ------
        key: str
            the query key to include in the URL
        value: Any
            the value to query on against the key
        """
        self.params.append(f"{key}={value}")
        return self

    def build(self) -> str:
        """Creates an endpoint URL with all configurations

        Returns
        -------
        URL
            the fully constructed URL with resource and any query parameters
        """
        return f"{self.base_url}/{self.resource}?" + "&".join(self.params)
