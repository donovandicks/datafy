# Play Counter

A scheduled serverless function that pings the user for their current listening
status and track information and records that data in a database.

__NOTE:__ This is only setup for myself right now.

## Design

The service functions as follows:

1. Ask Spotify for the track the user is currently listening to
2. If not currently listening - END
3. Cache currently listening song
4. Update database
   - Insert the track if it's not already present
   - Increment the playcount if the track already exists
5. Reschedule invocations if necessary

## Infrastructure

This service is built on the serverless framework and deployed to AWS. The function
is serverless and uses AWS Lambda while the database is a table in AWS DynamoDB.

## Scheduling

Function invocation is scheduled via an AWS EventBridge Rule and is dynamically
updated based on the following rules:

- If the user is currently listening to a track, invoke every minute
- If the user is __not__ currently listening to a track, invoke every 5 minutes
- If the current time is between 2AM and 8AM EST, invoke every hour

## Running Locally

Users can run locally using the `serverless` framework CLI or via the `just` tool
(similar to `make`).

To run with `serverless`, use the command `serverless invoke local --function play-counter`
To run with `just`, use the command `just run` from the current directory.

View the [`Justfile`](./Justfile) for more commands.

## Roadmap

- [ ] Add support for other users
