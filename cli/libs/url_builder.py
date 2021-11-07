from typing import Any


class URLBuilder:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.resource = None

    def with_resource(self, resource: str):
        if self.resource:
            raise AttributeError("Resource already set")

        self.resource = resource
        return self

    def with_param(self, key: str, value: Any):
        self.base_url + ""
        return self
