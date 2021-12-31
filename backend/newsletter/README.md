# Newsletter

A scheduled serverless function that reports to the user about their listening
habits over the last week.

__NOTE:__ This is only setup for myself right now.

## Design

The service functions as follows:

1. Retrieve play counts from last week
2. Retrieve play counts from this week
3. Calculate the differences
4. Generate a report
5. Send the report to the user

## Infrastructure

Framework: Serverless

Platform: AWS

Tool: AWS Lambda

Database: AWS DynamoDB

## Scheduling

Function invocation is scheduled via an AWS EventBridge Rule that triggers the
lambda function every Sunday at 12pm EST.

## Running Locally

Users can run locally using the `serverless` framework CLI or via the `just` tool
(similar to `make`).

To run with `serverless`, use the command `serverless invoke local --function play-counter`
To run with `just`, use the command `just run` from the current directory.

View the [`Justfile`](./Justfile) for more commands.

## Roadmap

- [ ] Add support for other users
