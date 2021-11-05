# CLI

A CLI application for interacting with the Datafy backend API from the terminal.

The CLI serves multiple purposes. It speeds up development and allows for a more
ergonomic way to test the backend API while circumventing the need for a fully
developed frontend. Ultimately it can also serve as a fully-featured way to
interact with the system.

## Usage

The Python3.10 runtime is __required__ for development and to run the CLI from source.

You can install from source by running `poetry install` in the current directory
and then running `python main.py -c CONTENT [-t TIME_RANGE] [-a AGGREGATE]`.
__NOTE__: To use the CLI, the backend API must be running. See the API [readme](../backend/api/README.md)
for more information.


## Contributing

Run `poetry install` to install all requirements.

The CLI uses the `argparse` library for argument parsing and validation.
