"""The main backend service driver"""

from flask import Flask
from flask_restful import Api

from resources.artists import Artists
from resources.songs import Songs

app = Flask(__name__)
api = Api(app)

api.add_resource(Artists, "/artists")
api.add_resource(Songs, "/songs")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
