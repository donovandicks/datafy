# CLI

A CLI application for interacting with the Datafy backend API from the terminal.

The CLI serves multiple purposes. It speeds up development and allows for a more
ergonomic way to test the backend API while circumventing the need for a fully
developed frontend. Ultimately it can also serve as a fully-featured way to
interact with the system.

## Usage

You can install from source by running `poetry install` in the current directory
and then running `python main.py -c CONTENT -t TIME_RANGE`. __NOTE__: To use the
CLI, the backend API must be running. See the API [readme](../api/README.md) for
more information.
