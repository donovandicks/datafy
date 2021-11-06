# Contributing

## Prerequisites

### Language Runtimes and Tools

- Python >= 3.10
- pip >= 21
- [poetry](https://python-poetry.org/docs/master/) >= 1.1.11 (dev)
- [black](https://github.com/psf/black)
- [pylint](https://pylint.org/)
- Node >= 14
- npm >= 7
- ESlint
- Docker
- Docker Compose

### Formatting, linting, and type checking

For Python, code is linted with Pylint and formatted with Black. They can be used
from the command line or via IDE integration. They are listed as dev-dependencies
in python packages. Type checking is performed by the Pylance language server set
to "basic".

For TypeScript, code is linted and formatted with ESlint, which is also listed

### Secrets

__The Spotify API keys are required for backend services__ to interact with the Spotify
application. The application __will not work__ without these keys and their related
configurations.

To get these keys, reach out to [Donovan](donovan.dicks@outlook.com).

Optional for Python version management:

- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

## Fullstack Development

To run the full application with communicating backend and frontend, run the
following command from the root directory:
`docker compose up -d`

This will start the frontend server on `localhost:3000` and the backend server
on `localhost:5000`. The frontend should be able to communicate with the backend
and data should be visible in the browser.

All applications are running on dev servers, meaning they will automatically pick
up changes to files as you make them. This means development can continue without
rebuilding and rerunning the containers, with the exception being changes to the
Dockerfiles and docker-compose file. While convenient, dev servers are less
performant and may not represent production level speeds.

## Frontend Only

Run `docker build -t frontend:<tag> .` from the [frontend](./frontend) directory
to build the frontend container image. Use a tag that is descriptive to your
current build to help keep track of separate images if you have them. Otherwise,
you can leave the tag blank and it will default to `latest`.

After the build completes, run `docker run -p 3000:3000 frontend:<tag>` to run
the container image. This will run the server and map your port 3000 to the
container's port 3000. The app can be accessed in the browser at localhost:3000.

## Backend Only

See the backend [README](./backend/README.md) for more information on running
backend services.

## Notes on Port Mappings

Running multiple services at the same time on the same port will require the
port mapping to adjust to different ports on the host machine. This can be
accomplished like so:
`docker run -p 5000:5000 serviceA && docker run -p 5001:5000 serviceB`
The port exposed on the container will remain the same, but will be mapped to a
different port on the host machine.

## Without Containers

Both frontend and backend services can be run locally __without__ containerization.

Frontend:

- Run `npm run dev` from the [frontend](./frontend) directory

Backend:

- Run `poetry run python main.py` from the [backend](./backend) directory
