# API

The core Datafy API

## Running Locally

The API can be run containerized via `docker-compose`.

You can also run the service directly by running the appropriate `python` command
for your environment on the [main](./main.py) file, however, this requires you
have a MongoDB instance up and running as well.

The development server is exposed on port 8000 and is run with reload on, meaning
changes are automatically picked up during development.

__Note:__ To authenticate correctly, either a `.env` file must be present in the
`datafy/api` directory or the environment variables `CLIENT_ID` and
`CLIENT_SECRET` must be defined with the appropriate secrets.

Currently, the user is required to provide their own tokens for authentication.
You can retrieve tokens by going to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login)
and creating an app.

## Retrieving Data

For a well-formatted response and an ergonomic user interface, you can use the
[CLI](../cli/README.md) to interact with the API.

Any other tool that can send HTTP requests will also do. For example, with curl:

```console
foo@bar:~$ curl http://0.0.0.0:8000/artists?limit=5&time_range=medium_term

{"item_type":"Artist","items":[{"content":"Artist","id":"5K4W6rqBFWDnAN6FQUkS6x","name":"Kanye West","popularity":96,"followers":16811978,"genres":["chicago rap","rap"]},{"content":"Artist","id":"6yJ6QQ3Y5l0s0tn7b0arrO","name":"JPEGMAFIA","popularity":69,"followers":469973,"genres":["alternative hip hop","escape room","experimental hip hop","hip hop","industrial hip hop","rap","underground hip hop"]},{"content":"Artist","id":"3A5tHz1SfngyOZM2gItYKu","name":"Earl Sweatshirt","popularity":74,"followers":1732337,"genres":["alternative hip hop","experimental hip hop","hip hop","rap","underground hip hop"]},{"content":"Artist","id":"68kEuyFKyqrdQQLLsmiatm","name":"Vince Staples","popularity":73,"followers":1538467,"genres":["conscious hip hop","escape room","hip hop","rap","underground hip hop"]},{"content":"Artist","id":"1ybINI1qPiFbwDXamRtwxD","name":"Smino","popularity":73,"followers":624800,"genres":["alternative r&b","hip hop","rap","underground hip hop"]}],"item_headers":["Rank","Artist","Popularity","Followers","Genres","ID"],"count":5}
```

## Routes

The API documentation is automatically generated with SwaggerUI and can be viewed
interactively at `http://0.0.0.0:8000/docs`. You can also see the documentation
below for more information.

The following endpoints are supported and generally return data related to the
name of the route. For information on what query parameters the endpoint accepts
and what data to expect in the response, visit the data model links below.

| Endpoint   | Data Models                                           |
| ---------- | ----------------------------------------------------- |
| `/artists` | [Artists](./models/README.md#Artists)                 |
| `/genres`  | [Genres](./models/README.md#Genres)                   |
| `/songs`   | [Songs](./models/README.md#Songs)                     |
| `/recs`    | [Recommendations](./models/README.md#Recommendations) |
