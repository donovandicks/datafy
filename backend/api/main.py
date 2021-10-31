"""The main backend service driver"""

from flask import Flask
from flask_restful import Api, Resource

from resources.registry import RESOURCE_REGISTRY


def init_flask_app() -> Flask:
    """Creates and configures the base Flask application

    Returns:
    - [Flask]: The Flask object instance
    """
    return Flask("datafy-api")


def register_resources(api: Api, resource_registry: dict[Resource, str]):
    """Registers API paths and resources on the Api instance

    Args:
    - api [Api]: The flask-restful Api object instance on which to register resources
    - resource_registry [dict]: A mapping from resource object to its api path
    """
    for resource, path in resource_registry.items():
        api.add_resource(resource, path)


def init_flask_api(app: Flask) -> Api:
    """Creates and configures the RESTful Flask API

    Args:
    - app [Flask]: The base Flask application object instance on which to build the API

    Returns:
    - [Api]: The flask-restful Api object instance
    """
    api = Api(app)
    register_resources(api, RESOURCE_REGISTRY)
    return api


def run_app():
    """Main program application"""
    app = init_flask_app()
    _ = init_flask_api(app)

    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    run_app()
