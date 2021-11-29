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
| name       | `str` | The plain name of the artist                |
| popularity | `int` | The popularity of the artist; from 0 to 100 |
| followers  | `int` | The number of followers the artist has      |

## Songs

The query model for the `/songs` route is defined as:

| Parameter  | Type        | Restrictions | Description                            |
| ---------- | ----------- | ------------ | -------------------------------------- |
| limit      | `int`       | 0 < limit    | The number of responses to return      |
| time_range | `TimeRange` | None         | The time period to request results for |

The response model for the route is defined as:

| Value | Type         | Description                           |
| ----- | ------------ | ------------------------------------- |
| items | `List[Song]` | A list of all songs retrieved         |
| count | `int`        | The number of items in the collection |

The model for an individual song is defined as:

| Value        | Type        | Description                                 |
| ------------ | ----------- | ------------------------------------------- |
| id           | `str`       | The Spotify ID of the artist                |
| name         | `str`       | The plain name of the artist                |
| artists      | `List[str]` | A list of artist names who perform the song |
| popularity   | `int`       | The popularity of the artist; from 0 to 100 |
| album        | `str`       | The name of the album the song is from      |
| release_date | `str`       | The date when the album was first released  |

## Genres

The query model for the `/genres` route is defined as:

| Parameter  | Type        | Restrictions | Description                                |
| ---------- | ----------- | ------------ | ------------------------------------------ |
| limit      | `int`       | 0 < limit    | The number of responses to return          |
| time_range | `TimeRange` | None         | The time period to request results for     |
| aggregate  | `bool`      | None         | Whether to group results into broader bins |

The response model for the route is defined as:

| Value | Type          | Description                           |
| ----- | ------------- | ------------------------------------- |
| items | `List[Genre]` | A list of all genres retrieved        |
| count | `int`         | The number of items in the collection |

The model for an individual genre is defined as:

| Value | Type  | Description                            |
| ----- | ----- | -------------------------------------- |
| name  | `str` | The name of the genre                  |
| count | `int` | The number of times the genre appeared |

## Recommendations

The query model for the `/recs` route is defined as:

| Parameter    | Type        | Restrictions                                      | Description                                                                     |
| ------------ | ----------- | ------------------------------------------------- | ------------------------------------------------------------------------------- |
| limit        | `int`       | 0 < limit                                         | The number of responses to return                                               |
| time_range   | `TimeRange` | None                                              | The time period to request results for                                          |
| seed_artists | `str`       | 0 < seed_artists + seed_genres + seed_tracks <= 5 | Comma-separated artist IDs used as seed values for the recommendation algorithm |
| seed_genres  | `str`       | 0 < seed_artists + seed_genres + seed_tracks <= 5 | Comma-separated genre IDs used as seed values for the recommendation algorithm  |
| seed_tracks  | `str`       | 0 < seed_artists + seed_genres + seed_tracks <= 5 | Comma-separated track IDs used as seed values for the recommendation algorithm  |

The response model for the route is defined as:

| Value | Type        | Description                             |
| ----- | ----------- | --------------------------------------- |
| items | `List[Rec]` | A list of all recommendations retrieved |
| count | `int`       | The number of items in the collection   |

The model for an individual recommendation is defined as:

| Value   | Type        | Description                              |
| ------- | ----------- | ---------------------------------------- |
| song    | `str`       | The name of the song                     |
| artists | `List[str]` | The list of artists who perform the song |
