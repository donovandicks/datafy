"""Route related resources"""
from typing import Dict, Type

from fastapi import APIRouter

from .artists import router as artists_router
from .genres import router as genres_router
from .recs import router as recs_router
from .songs import router as songs_router

ROUTE_REGISTRY: list[APIRouter] = [
    artists_router,
    genres_router,
    recs_router,
    songs_router,
]
