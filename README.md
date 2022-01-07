# Datafy

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A web application to view Spotify data

- [Datafy](#datafy)
  - [CLI](#cli)
  - [Backend](#backend)
    - [API](#api)
    - [Play Counter](#play-counter)
  - [Contributing](#contributing)
  - [Resources](#resources)

## CLI

Data can be accessed and visualized via the terminal as well by using the [CLI](./cli/README.md).

## Backend

### API

The core [API](./backend/api/README.md) is responsible for interacting with Spotify.

### Play Counter

The [Play Counter](./backend/play_counter/README.md) is a scheduled function that counts plays
per track for the user.

### Newsletter

The [Newsletter](./backend/newsletter/README.md) is a scheduled function that sends a report
to the user about their play counts over the past week.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) and the [Style Guide](style-guide.md)

## Resources

- [Spotify API Docs](https://developer.spotify.com/documentation/web-api/reference/#/)
