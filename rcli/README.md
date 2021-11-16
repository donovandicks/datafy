# Rustify

The Rust CLI to interact with the Datafy backend

- [Rustify](#rustify)
  - [Getting Started](#getting-started)
  - [Contributing](#contributing)

## Getting Started

To use the CLI, you must currently have the Rust toolchain installed on your machine.

The application can be run using `cargo run` or by calling `cargo build` and executing
the compiled executable found in `./target/debug/rcli`

## Contributing

All source code is contained under [src](./src). The `main.rs` file contains the
entry point for the CLI and handles the main program loop which prompts the user
for input and delegates the necessary actions to the appropriate programs.

[Models](./src/models) are a collection of data models that define the structure
and any associated behavior for the data retrieved from the Datafy backend.

[Libs](./src/libs) contains logic for parsing and validating user input, interacting
with the Datafy backend, and displaying data to the terminal.
