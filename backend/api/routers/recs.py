"""Defines the logic for handling requests to the `/recs` route"""

from dependencies.spotify import Client, SpotifyClient
from fastapi import APIRouter, Depends
from models.rec import Rec, RecCollection, RecQuery

router = APIRouter(prefix="/recs", tags=["recommendations", "recs"])


def get_recs(client: SpotifyClient) -> RecCollection:
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
    items = [Rec.from_dict(item) for item in client.get_recommendations_from_spotify()]
    return RecCollection(
        items=items,
        count=len(items),
    )


@router.get("", response_model=RecCollection)
async def get_recommendations(query: RecQuery = Depends()) -> RecCollection:
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
    client = Client(query)
    return get_recs(client)
