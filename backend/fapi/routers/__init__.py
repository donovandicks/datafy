"""Route related resources"""
from typing import Dict, Type

from fastapi import APIRouter

from .artists import router as artists_router
from .genres import router as genre_router
from .songs import router as songs_router

ROUTE_REGISTRY: list[APIRouter] = [
    artists_router,
    genre_router,
    songs_router,
]
