# Style Guide

- [Style Guide](#style-guide)
  - [Overview](#overview)
  - [Python](#python)
    - [Black Formatting](#black-formatting)
    - [Pylint](#pylint)
    - [Pylance](#pylance)
  - [Rust](#rust)
    - [Rustfmt](#rustfmt)
    - [Rust Analyzer](#rust-analyzer)

## Overview

Guidelines on formatting, idiomatic code patterns, and other matters of style.

To keep code uniform, good-looking, and correct, please follow the guidelines
below. It is also recommended to set your editor to format files on save, trim
trailing whitespace, and organize imports.

## Python

### Black Formatting

Formatting is general accomplished with the tool `black`. No extra configurations
have been made to the tool and it generally runs as provided.

### Pylint

Pylint is the chosen python linting tool for this project. It alerts for common
formatting and style issues, as well as real runtime issues like unresolved
imports and misaligned function signatures with implementations. Again, no
configurations have been made at the root level, however, some rules are disabled
on a line-by-line basis throughout the project. This is typically to solve
compatibility issues between Pylint and other modules, or because Pylint has
not been updated to accommodate new Python syntax.

Take Pylint warnings seriously. Resolve as many as possible while retaining a
reasonable style. Some issues can not be avoided.

Never disable Pylint at the file or project level and only disable lines if
absolutely necessary.

### Pylance

The current language server for this project is Pylance and the type checking
is set to "basic." This setting may be reevaluated in the future.

## Rust

### Rustfmt

The default formatter `rustfmt` is used for all Rust code. Formatting can be triggered
by executing `cargo fmt` in a Rust project directory.

### Rust Analyzer

The Rust Analyzer language server handles all type checking and linting for Rust
code.
