# CLI

A CLI application for interacting with the Datafy backend API from the terminal.

The CLI serves multiple purposes. It speeds up development and allows for a more
ergonomic way to test the backend API while circumventing the need for a fully
developed frontend. Ultimately it can also serve as a fully-featured way to
interact with the system.

## Usage

The Python3.10 runtime is __required__ for development and to run the CLI from source.

### Installation

Run `poetry install` in the current directory

### Running

To interact with the main API, run:
`python api.py -c CONTENT [-l LIMIT] [-t TIME_RANGE] [-a AGGREGATE]`

To interact with the recommendations API, run:
`python rec.py [-l LIMIT] [-sa SEED_ARTISTS] [-st SEED_TRACKS] [-sg SEED_GENRES]`

__NOTES__:

- To use the CLI, the backend API must be running. See the API [readme](../backend/api/README.md) for more information.
- Depending on your setup, you may need to append `poetry run` to these commands

## Contributing

Run `poetry install` to install all requirements.

The CLI uses the `argparse` library for argument parsing and validation.
