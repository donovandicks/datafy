# Datafy

A web application to view Spotify data

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) and the [Style Guide](style-guide.md)

If you are using VSCode, it is recommended to use the Microsoft [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
extension and the [Error Lens](https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens) extension

## Roadmap

### Overall

- [ ] Decide on storage technology (SQL vs NoSQL, which specifically of either)
- [ ] Implement storage (installation, setup, config, Dockerize)
- [ ] Decide on cache technology (probably Redis)
- [ ] Implement cache (installation, setup, config, Dockerize)
- [ ] Mature logging practices across application
- [X] Migrate python pacakges to 3.10

### Backend

- [X] Retrieve top artists and songs from Spotify
- [X] Retrieve genre breakdown of top artists/songs
- [X] Aggregate genres
- [ ] Cache responses from Spotify Web API
- [ ] Store Spotify data in long term storage
  - Ideally with enough data could circumvent spotify's time range limitations
- [ ] Enrich Spotify data in the long term storage
  - Play counts
  - Last played on
- [ ] Interact with the player SDK (actually controlling the spotify player)
  - Regular ping to get current playing, update stored data
  - Better shuffle randomization
- [ ] Enhanced recommendation service
- [ ] Parameterized Playlist/Queue generation
- [ ] Investigate Django & Django-restful for a possible conversion from Flask

### CLI

- [X] Get and display top artists and songs from the backend
- [X] Support genres resource
- [ ] Access enriched data from the backend
- [ ] Access spotify player through the backend

### Frontend

- [X] Charts with top played artists and songs
- [ ] Display genre breakdown
- [ ] Unified time range control
- [ ] Display changes in songs/artists over time (e.g. Rank +2 / Rank -1)
- [ ] Support drilldown into genres
- [ ] Look for Spotify-esque styling/themes
