# cli-anything-huginn

A CLI-Anything agent harness for [Huginn](https://github.com/huginn/huginn).

## Installation

```bash
# In the agent-harness directory
pip install -e .
```

## Prerequisite

1. Ensure you have Ruby installed and the `bundle exec rails runner` works in your Huginn directory.
2. Provide the `HUGINN_ROOT` environment variable if you are invoking `cli-anything-huginn` from outside the project directory.

## Usage

Start the REPL:
```bash
cli-anything-huginn
```

Run subcommands:
```bash
cli-anything-huginn agent list
cli-anything-huginn scenario export <sc_id> -o config.json
cli-anything-huginn event list --agent-id 1
```

Get JSON output for Agent context:
```bash
cli-anything-huginn --json agent list
```
