import pytest
import click
from click.testing import CliRunner
from cli_anything.huginn.huginn_cli import main

# Since backend relies on Rails Runner, unit tests here test the Click interfaces.

@pytest.fixture
def runner():
    return CliRunner()

def test_agent_list_help(runner):
    result = runner.invoke(main, ['agent', 'list', '--help'])
    assert result.exit_code == 0
    assert 'List all agents' in result.output

def test_scenario_export_help(runner):
    result = runner.invoke(main, ['scenario', 'export', '--help'])
    assert result.exit_code == 0
    assert 'Output JSON file path' in result.output

def test_event_list_help(runner):
    result = runner.invoke(main, ['event', 'list', '--help'])
    assert result.exit_code == 0
    assert 'Filter by agent id' in result.output
