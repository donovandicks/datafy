from typing import List, TypeGuard

from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class PlayCount(SQLModel, table=True, inherit_cache=True):
    """The PlayCount table schema"""

    track_id: str = Field(primary_key=True)
    last_played_timestamp: int = Field(sa_column=Column(BigInteger()))
    total_play_count: int


def is_playcount_list(val: List) -> TypeGuard[List[PlayCount]]:
    return all(isinstance(item, PlayCount) for item in val)
