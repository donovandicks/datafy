"""Setup config for the Artists microservice"""

from distutils.core import setup

setup(
    name="Artists",
    version="0.1.0",
    description="The artists microservice",
    author="Donovan Dicks",
    install_requires=["spotipy", "dynaconf", "flask", "flask-restful"],
    extras_require={
        "dev": ["black", "pylint"],
    },
)
