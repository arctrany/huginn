---
name: "cli-anything-huginn"
description: "Control Huginn automated agents via CLI. Can list, trigger, export scenarios, and check events."
---

# cli-anything-huginn

## Description
This skill allows AI agents to directly control a Huginn instance (an IFTTT-like automation server). Through this CLI, you have programmatic access to view internal Agents, trigger them, and export/import whole Scenarios as JSON.

## System Requirements
- Command is available globally if installed: `cli-anything-huginn`
- Backend relies on the local Huginn environment (`bundle exec rails runner`). 

## Command Groups

* `agent`: `list`, `info <id>`, `trigger <id>`, `delete <id>`
* `scenario`: `list`, `export <id> -o file.json`, `import <file.json>`
* `event`: `list`, `clear`

## Agent Guidelines
1. You MUST use the `--json` flag when running commands to receive easily parseable, pure JSON output.
2. Example for listing agents: `cli-anything-huginn --json agent list`
3. If an error is returned related to "Ruby not found" or "Rails Script Error", the executing environment may not be in the correct Huginn working directory (or `HUGINN_ROOT` env isn't valid).
