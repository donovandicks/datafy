# Datafy

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A collection of systems for gathering and analyzing data from Spotify.

- [Datafy](#datafy)
  - [CLI](#cli)
  - [API](#api)
  - [PCLR](#pclr)
  - [Song Analyzer](#song-analyzer)
  - [Contributing](#contributing)
  - [Resources](#resources)

## CLI

The CLI can be used to access and visualize data from the terminal. View the
[README](./cli/README.md) for more information.

## API

The core API supports interacting with some Spotify endpoints to get data directly
from the platform. See the [README](./api/README.md) for more information.

## PCLR

PCLR is a long running service that keeps track of the user's listening activity.
See the [README](./pclr/README.md) for more information.

## Song Analyzer

The Song Analyzer service retrieves and stores detailed information about tracks
that the user has listened to. See the [README](./song-analyzer/README.md) for
more information.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) and the [Style Guide](style-guide.md)

## Resources

- [Spotify API Docs](https://developer.spotify.com/documentation/web-api/reference/#/)
