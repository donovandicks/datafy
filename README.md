# Datafy

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A web application to view Spotify data

- [Datafy](#datafy)
  - [REWRITE DESIGN](#rewrite-design)
  - [CLI](#cli)
  - [Backend](#backend)
    - [API](#api)
    - [Play Counter](#play-counter)
    - [Newsletter](#newsletter)
  - [Contributing](#contributing)
  - [Resources](#resources)

## REWRITE DESIGN

New Design:

- Play Tracker
  - Long running service that queries spotify for currently playing song
  - Emits events containing the track data to a queue
- Play Counter
  - Event driven service that reads track data from queue
  - Stores and updates track data in a database
- Vibe Check
  - Scheduled task to track listening patterns on a weekly basis
  - Reads data from counter database
  - Analyze amount listened, sentiment, etc
  - Stores analysis in another database
- Data Viewer
  - Frontend to display data from both counter and analysis databases
  - Focus on data visualizations
- Telemetry Insights
  - Sink for logs from all services
  - Analyze logs for system health

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
