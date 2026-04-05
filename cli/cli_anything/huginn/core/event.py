import click
import json
from cli_anything.huginn.utils.huginn_backend import back_event_list, back_event_clear
from cli_anything.huginn.utils.repl_skin import ReplSkin

skin = ReplSkin("huginn")

@click.group()
def event_group():
    """Manage Huginn Events."""
    pass

@event_group.command("list")
@click.option("--agent-id", type=int, help="Filter by agent id")
@click.pass_context
def list_events(ctx, agent_id):
    """List recent events."""
    try:
        data = back_event_list(agent_id=agent_id)
        if ctx.obj.get("json_output"):
            click.echo(json.dumps(data, indent=2))
            return
            
        headers = ["ID", "Agent ID", "Created At", "Payload Sample"]
        rows = []
        for m in data:
            payload_sample = str(m.get("payload", {}))[:40]
            rows.append([m["id"], m["agent_id"], m["created_at"], payload_sample])
            
        skin.table(headers, rows)
    except Exception as e:
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"error": str(e)}))
        else:
            skin.error(str(e))

@event_group.command("clear")
@click.pass_context
def clear_events(ctx):
    """Clear all events."""
    try:
        data = back_event_clear()
        if ctx.obj.get("json_output"):
            click.echo(json.dumps(data, indent=2))
            return
        skin.success("All events cleared.")
    except Exception as e:
        if ctx.obj.get("json_output"):
            click.echo(json.dumps({"error": str(e)}))
        else:
            skin.error(str(e))
