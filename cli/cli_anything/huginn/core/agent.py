import click
import json
from cli_anything.huginn.utils.huginn_backend import back_agent_list, back_agent_info, back_agent_trigger, back_agent_delete
from cli_anything.huginn.utils.repl_skin import ReplSkin

skin = ReplSkin("huginn")

@click.group()
def agent_group():
    """Manage Huginn Agents."""
    pass

@agent_group.command("list")
@click.pass_context
def list_agents(ctx):
    """List all agents."""
    try:
        data = back_agent_list()
        if ctx.obj.get("json_output"):
            click.echo(json.dumps(data, indent=2))
            return
            
        headers = ["ID", "Name", "Type", "Disabled", "Events Count"]
        rows = [[m["id"], m["name"], m["type"], m["disabled"], m["events_count"]] for m in data]
        skin.table(headers, rows)
    except Exception as e:
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"error": str(e)}))
        else:
            skin.error(str(e))

@agent_group.command("info")
@click.argument("agent_id")
@click.pass_context
def info_agent(ctx, agent_id):
    """Get detail info of an agent."""
    try:
        data = back_agent_info(agent_id)
        if ctx.obj.get("json_output"):
            click.echo(json.dumps(data, indent=2))
            return
            
        skin.status("Agent ID", data["id"])
        skin.status("Name", data["name"])
        skin.status("Schedule", data.get("schedule", "N/A"))
        skin.status("Last Check", data.get("last_check_at", "N/A"))
        skin.info(f"Options: {json.dumps(data.get('options', {}), indent=2)}")
    except Exception as e:
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"error": str(e)}))
        else:
            skin.error(str(e))

@agent_group.command("trigger")
@click.argument("agent_id")
@click.pass_context
def trigger_agent(ctx, agent_id):
    """Trigger an agent immediately."""
    try:
        data = back_agent_trigger(agent_id)
        if ctx.obj.get("json_output"):
            click.echo(json.dumps(data, indent=2))
            return
        skin.success(f"Agent {agent_id} triggered successfully.")
    except Exception as e:
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"error": str(e)}))
        else:
            skin.error(str(e))

@agent_group.command("delete")
@click.argument("agent_id")
@click.pass_context
def delete_agent(ctx, agent_id):
    """Delete an agent."""
    try:
        data = back_agent_delete(agent_id)
        if ctx.obj.get("json_output"):
            click.echo(json.dumps(data, indent=2))
            return
        skin.success(f"Agent {agent_id} deleted successfully.")
    except Exception as e:
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"error": str(e)}))
        else:
            skin.error(str(e))
