from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel
from pydantic import condecimal
from models.track import CurrentlyPlaying


class Album(SQLModel, table=True):
    """The Album table schema"""

    id: str = Field(primary_key=True)
    name: str

    @classmethod
    def from_spotify(cls, item: CurrentlyPlaying):
        return Album(id=item.album_id, name=item.album_name)


class Artist(SQLModel, table=True):
    """The Artist table schema"""

    id: str = Field(primary_key=True)
    name: str

    @classmethod
    def from_spotify(cls, item: CurrentlyPlaying):
        return Artist(id=item.artist_id, name=item.artist_name)


class Track(SQLModel, table=True):
    """The Track table schema"""

    id: str = Field(primary_key=True)
    name: str
    artist_id: str = Field(foreign_key="artist.id")
    album_id: str = Field(foreign_key="album.id")
    popularity: int

    @classmethod
    def from_spotify(cls, item: CurrentlyPlaying):
        return Track(
            id=item.track_id,
            name=item.track_name,
            artist_id=item.artist_id,
            album_id=item.album_id,
            popularity=item.popularity,
        )


class TrackDetail(SQLModel, table=True):
    """The TrackDetail table schema"""

    id: str = Field(primary_key=True, foreign_key="track.id")
    acousticness: condecimal(max_digits=6, decimal_places=5)
    danceability: condecimal(max_digits=4, decimal_places=3)
    duration_ms: int
    energy: condecimal(max_digits=4, decimal_places=3)
    instrumentalness: condecimal(max_digits=6, decimal_places=5)
    loudness: condecimal(max_digits=6, decimal_places=3)
    speechiness: condecimal(max_digits=5, decimal_places=4)
    tempo: condecimal(max_digits=6, decimal_places=3)
    valence: condecimal(max_digits=4, decimal_places=3)


class PlayCount(SQLModel, table=True):
    """The PlayCount table schema"""

    id: str = Field(primary_key=True, foreign_key="track.id")
    last_played_timestamp: int = Field(sa_column=Column(BigInteger()))
    total_play_count: int
