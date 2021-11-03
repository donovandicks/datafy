# Datafy

A web application to view Spotify data

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md)

## Roadmap

### Backend

- [X] Retrieve top artists and songs from Spotify
- [ ] Retrieve genre breakdown of top artists/songs
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

### CLI

- [X] Get and display top artists and songs from the backend
- [ ] Access enriched data from the backend
- [ ] Access spotify player through the backend

### Frontend

- [X] Charts with top played artists and songs
- [ ] Display genre breakdown
- [ ] Unified time range control
- [ ] Display changes in songs/artists over time (e.g. Rank +2 / Rank -1)
