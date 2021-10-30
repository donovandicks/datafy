"""Common model definitions across API query models"""

from enum import Enum


class TimeRange(Enum):
    """The supported time ranges for the Spotify web API

    short_term = The last 4 weeks
    medium_term = The last 6 months
    long_term = The last several years
    """

    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"
