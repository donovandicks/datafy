# Models

All the data definitions for the values sent to and received from the API routes
are defined here.

## Common

The `TimeRange` enum defines a common resource for working with time ranges that
are expected by the Spotify API. Acceptable values are:

- short_term
- medium_term
- long_term

## Artists

The query model for the `/artists` route is defined as:

| Parameter  | Type        | Restrictions | Description                            |
| ---------- | ----------- | ------------ | -------------------------------------- |
| limit      | `int`       | 0 < limit    | The number of responses to return      |
| time_range | `TimeRange` | None         | The time period to request results for |

The response model for the route is defined as:

| Value | Type           | Description                     |
| ----- | -------------- | ------------------------------- |
| items | `List[Artist]` | A list of all artists retrieved |

The model for an individual artist is defined as:

| Value      | Type  | Description                                 |
| ---------- | ----- | ------------------------------------------- |
| id         | `str` | The Spotify ID of the artist                |
| name       | str   | The plain name of the artist                |
| popularity | int   | The popularity of the artist; from 0 to 100 |
| followers  | int   | The number of followers the artist has      |
