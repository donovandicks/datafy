"""Defines the logic for handling requests to the `/recs` route"""

from dependencies.spotify import Client, SpotifyClient
from fastapi import APIRouter, Depends
from models.collection import Collection
from models.rec import Rec, RecQuery
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(  # type: ignore
    BatchSpanProcessor(ConsoleSpanExporter())
)
tracer = trace.get_tracer(__name__)

router = APIRouter(prefix="/recs", tags=["recommendations", "recs"])


def get_recs(client: SpotifyClient) -> Collection[Rec]:
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
    recs: Collection[Rec]
       a collection of `Rec` objects
    """
    items = [Rec.from_dict(item) for item in client.get_recommendations_from_spotify()]
    return Collection.from_list(items)


@router.get("", response_model=Collection[Rec])
async def get_recommendations(query: RecQuery = Depends()) -> Collection[Rec]:
    """
    Retrieves recommendations for the user based on their input parameters

    Params
    ------
    query: RecQuery
        the query object with seed data from the request url

    Returns
    -------
    recs: Collection[Rec]
        a collection of `Rec` objects
    """
    with tracer.start_as_current_span(
        name="Retrieving recommendations",
        attributes={
            "limit": str(query.limit),
            "seed_artists": str(query.seed_artists),
            "seed_genres": str(query.seed_genres),
            "seed_tracks": str(query.seed_tracks),
        },
    ):
        return get_recs(Client(query))
