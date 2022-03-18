from clients.postgres import PostgresClient
from models.db import FilterExpression
from models.track import Track

OBJECTS = ["artist", "track", "album", "play_count"]


def check_exists(
    client: PostgresClient,
    track: Track,
    item: str,
) -> bool:
    """Generic function to check item existence in the db"""
    if item not in OBJECTS:
        raise ValueError(f"Object {item} is not valid. Must be one of {OBJECTS}")

    filter_field = "track_id" if item == "play_count" else f"{item}_id"
    filter_value = (
        track.get_id(item="track") if item == "play_count" else track.get_id(item=item)
    )
    filter_expr = FilterExpression(
        filter_field=filter_field,
        filter_condition="=",
        filter_value=filter_value,
    )

    result = client.get_row(table=item, filter_expr=filter_expr)
    return bool(result)
