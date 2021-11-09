# Core API

The core backend service for the project, housing the main API server.

## Configuration

This service requires a `.env` file in the current directory. The file should
have the following keys:

- CLIENT_ID=***
- CLIENT_SECRET=***

The keys are available from <donovan.dicks@outlook.com> and are required
for the service to authenticate properly with Spotify. They should __never__ be
committed to the repository.

## Contributing

### Development

The Python3.10 runtime is __required__ for development and deployment.

To install all deploy and dev dependencies, run `poetry install`

The API service is built on the Flask and Flask-Restful libraries. The Spotipy
library is used for communicating with the Spotify application.

### Running Locally

To run in a responsive dev environment where code changes are picked up without
the need for manually building and running the image again, use `docker compose`:

Run `docker compose up` from the current directory.

To build and run the container manually:

1. Run `docker build -t datafy-api:<tag> .`
2. Run `docker run -p 5000:5000 datafy-api:<tag>`
    - You can also add the `-d` option to run in detached mode (as a background process)

This will run the server and map your port 5000 to the
container's port 5000. The app can be accessed via HTTP requests from the console
or the browser.

Steps to run locally:

- Run `poetry run python main.py`
