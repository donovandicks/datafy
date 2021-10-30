"""The main backend service driver"""

from flask import Flask
from flask_restful import Api

from resources.registry import RESOURCE_REGISTRY

app = Flask(__name__)
api = Api(app)

for resource, path in RESOURCE_REGISTRY.items():
    api.add_resource(resource, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
