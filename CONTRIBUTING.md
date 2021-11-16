# Contributing

- [Contributing](#contributing)
  - [Prerequisites](#prerequisites)
    - [Language Runtimes and Tools](#language-runtimes-and-tools)
    - [Secrets](#secrets)
  - [Local Development](#local-development)
    - [Getting Setup](#getting-setup)
      - [Python](#python)
      - [Rust](#rust)
    - [Flow](#flow)
    - [Submitting Issues](#submitting-issues)
    - [Submitting PRs](#submitting-prs)
  - [Running Locally](#running-locally)
    - [CLI](#cli)
    - [Backend](#backend)
    - [Notes on Port Mappings with Docker](#notes-on-port-mappings-with-docker)

## Prerequisites

### Language Runtimes and Tools

Python:

- Python >= 3.10
- pip >= 21
- [poetry](https://python-poetry.org/docs/master/) >= 1.1.11 (dev)
- [black](https://github.com/psf/black)
- [pylint](https://pylint.org/)

Rust:

- Rust >= 1.56
- Cargo >= 1.56

Docker:

- Docker
- Docker Compose

Optional for Python version management:

- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

### Secrets

__The Spotify API keys are required for backend services__ to interact with the Spotify
application. The application __will not work__ without these keys and their related
configurations.

To get these keys, reach out to <donovan.dicks@outlook.com>.

## Local Development

### Getting Setup

#### Python

For Python work, it is recommended to make use of `pyenv` with virtual environments
to manage different python interpreters. Since each python package has different
dependencies, it can be easier to work with them as separate virtual environments.

The dependency manager `poetry` is also being used to resolve and install dependencies.
For the best experience, it is recommended to use poetry and pyenv in conjunction.

See [pyenv build environment](https://github.com/pyenv/pyenv-installer) for the
prerequisites for installing pyenv. This is recommended to avoid any issues with
the pyenv installation.

See [pyenv](https://github.com/pyenv/pyenv-installer) for installing pyenv.

See [pyenv virtualenv](https://github.com/pyenv/pyenv-installer) for installing pyenv
virtualenv for managing virtual environments with pyenv.

See [poetry](https://python-poetry.org/docs/master/#installation) for installing
the dev branch of poetry.

See [poetry environments](https://python-poetry.org/docs/master/managing-environments/#switching-between-environments) for using
poetry with pyenv virtual environments.

#### Rust

For Rust work, it is recommended to use the standard toolchain. Builds can be slow
so you should have an editor that can lint your code as it's written, so as not
to depend on build output to find errors. To check your code manually without
building an executable, you can run `cargo check`.

All Rust libraries can be found on [crates.io](https://crates.io) and should be
added to the appropriate `Cargo.toml` file. Dependencies are installed during the
build process.

### Flow

Visit the [issues](https://github.com/donovandicks/datafy/issues) page for items that
need to be completed. Once you've selected an issue, assign it to yourself.

To contribute to the repository, use [trunk-based development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development)

Your flow should look like this:

1. Clone the remote main (only need to do this once)
2. Checkout a new branch with a descriptive name for your change
3. Make your changes locally
    1. Code
    2. Tests
    3. Documentation
4. Test your changes locally
5. Push to the remote
6. Submit a PR for your branch
7. Revise until approved
8. Squash and merge on approval
   1. Delete your remote branch
   2. Delete your local branch

### Submitting Issues

If you have a request for new functionality, would like to report a bug, or need
to ask a question, create a new issue. If you are actively developing something
that does not have a related issue, please create one and tag it appropriately.

### Submitting PRs

Pull requests should automatically be generated with a template for the repo. Please
fill out the checklist and include the request information. If an item on the list
does not apply to your change, mark it as N/A.

## Running Locally

### CLI

See the CLI [README](./rcli/README.md) for more information on running the CLI

### Backend

See the backend [README](./backend/README.md) for more information on running
backend services.

### Notes on Port Mappings with Docker

Running multiple services at the same time on the same port will require the
port mapping to adjust to different ports on the host machine. This can be
accomplished like so:
`docker run -p 5000:5000 serviceA && docker run -p 5001:5000 serviceB`
The port exposed on the container will remain the same, but will be mapped to a
different port on the host machine.
