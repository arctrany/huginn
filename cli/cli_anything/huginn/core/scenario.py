import click
import json
import os
from cli_anything.huginn.utils.huginn_backend import back_scenario_list, back_scenario_export, back_scenario_import
from cli_anything.huginn.utils.repl_skin import ReplSkin

skin = ReplSkin("huginn")

@click.group()
def scenario_group():
    """Manage Huginn Scenarios."""
    pass

@scenario_group.command("list")
@click.pass_context
def list_scenarios(ctx):
    """List all scenarios."""
    try:
        data = back_scenario_list()
        if ctx.obj.get("json_output"):
            click.echo(json.dumps(data, indent=2))
            return
            
        headers = ["ID", "Name", "Description", "Agent Count"]
        rows = [[m["id"], m["name"], m.get("description", "")[:30], m["agent_count"]] for m in data]
        skin.table(headers, rows)
    except Exception as e:
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"error": str(e)}))
        else:
            skin.error(str(e))

@scenario_group.command("export")
@click.argument("scenario_id")
@click.option("-o", "--output", required=True, help="Output JSON file path")
@click.pass_context
def export_scenario(ctx, scenario_id, output):
    """Export sequence JSON for a scenario."""
    try:
        data = back_scenario_export(scenario_id)
        
        with open(output, "w") as f:
            json.dump(data, f, indent=2)
            
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"exported": True, "output": output}))
            return
        skin.success(f"Scenario {scenario_id} exported to {output}")
    except Exception as e:
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"error": str(e)}))
        else:
            skin.error(str(e))

@scenario_group.command("import")
@click.argument("file_path")
@click.pass_context
def import_scenario(ctx, file_path):
    """Import a scenario JSON."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Needs absolute path for ruby backend script
        abs_path = os.path.abspath(file_path)
        data = back_scenario_import(abs_path)
        
        if ctx.obj.get("json_output"):
            click.echo(json.dumps(data, indent=2))
            return
            
        if data.get("imported"):
            skin.success(f"Scenario imported successfully from {file_path}")
        else:
            skin.error(f"Failed to import: {data.get('errors')}")
    except Exception as e:
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"error": str(e)}))
        else:
            skin.error(str(e))
