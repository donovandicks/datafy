# Backend

The core backend service for the project, housing the main API server.

## Configuration

This service requires a `.env` file in the current directory. The file should
have the following keys:

- CLIENT_ID=***
- CLIENT_SECRET=***
- REDIRECT_URI=***

The keys are available from [Donovan](donovan.dicks@outlook.com) and are required
for the service to authenticate properly with Spotify. They should __never__ be
committed to the repository.

## Contributing

### Development

To install all deploy and dev dependencies, run `poetry install`

### Container

Run `docker build -t backend:<tag> .`

After the build completes, run `docker run -p 5000:5000 backend:<tag>` to
run the container image. This will run the server and map your port 5000 to the
container's port 5000. The app can be accessed via HTTP requests from the console
or the browser.
