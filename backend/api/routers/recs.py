"""Defines the logic for handling requests to the `/recs` route"""

from typing import Callable, Dict, List

from dependencies.spotify import CLIENT
from fastapi import APIRouter, Depends, HTTPException
from models.rec import Rec, RecQuery, RecResponse

router = APIRouter(prefix="/recs", tags=["recommendations", "recs"])


def parse_rec(item: Dict) -> Rec:
    """
    Parses an object into a `Rec`

    Params
    ------
    item: Dict
        a recommendation object retrieved from the api

    Returns
    -------
    rec: Rec
        a `Rec` object with the recommendation data
    """
    return Rec.from_dict(item)


def get_recommendations_from_spotify(query: RecQuery, client=CLIENT) -> List[Dict]:
    """
    Retrieves recommendations from spotify

    Params
    ------
    query: RecQuery
        the query object containing seed data for the recommendation api
    client: [Spotify]
        the api client object used to interact with Spotify

    Returns
    -------
    tracks: List[Dict]
        a list of tracks returned from the API
    """
    recommendations = client.recommendations(
        seed_artists=query.seed_artists_list,
        seed_genres=query.seed_genres_list,
        seed_tracks=query.seed_tracks_list,
        limit=query.limit,
    )

    if not recommendations:
        raise HTTPException(404, "Recommendations not found")

    return recommendations["tracks"]


def get_recs(query: RecQuery, retriever: Callable[[RecQuery], List[Dict]]) -> List[Rec]:
    """
    Parses recommendations into a list of `Rec`s

    Params
    ------
    query: RecQuery
        the query object containing seed data for the recommendation api
    retriever: Callable[[RecQuery], List[Dict]]
        a function that takes a `RecQuery` and returns a list of recommendation
        objects

    Returns
    -------
    recs: List[Rec]
        a list of `Rec`s
    """
    return [parse_rec(item) for item in retriever(query)]


@router.get("", response_model=RecResponse)
async def get_recommendations(query: RecQuery = Depends()) -> RecResponse:
    """
    Retrieves recommendations for the user based on their input parameters

    Params
    ------
    query: RecQuery
        the query object with seed data from the request url

    Returns
    -------
    recs: RecResponse
        a recommendation response object containing a list of `Rec`s
    """
    return RecResponse(items=get_recs(query, get_recommendations_from_spotify))
