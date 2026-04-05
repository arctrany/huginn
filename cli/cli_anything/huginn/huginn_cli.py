import click
import json
import traceback

from cli_anything.huginn.utils.repl_skin import ReplSkin
from cli_anything.huginn.core.agent import agent_group
from cli_anything.huginn.core.scenario import scenario_group
from cli_anything.huginn.core.event import event_group

skin = ReplSkin("huginn", version="1.0.0")

@click.group(invoke_without_command=True)
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
@click.pass_context
def main(ctx, json_output):
    """CLI-Anything harness for Huginn (Ruby on Rails Automated Agent Platform)."""
    ctx.ensure_object(dict)
    ctx.obj["json_output"] = json_output

    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)

@main.command()
@click.pass_context
def repl(ctx):
    """Start the interactive REPL session."""
    skin.print_banner()
    commands_dict = {
        "agent": "Manage internal ruby agents",
        "scenario": "Export and Import workflows",
        "event": "Manage agent events",
        "help": "Show this message",
        "exit": "Exit the REPL"
    }

    pt_session = skin.create_prompt_session()

    while True:
        try:
            line = skin.get_input(pt_session, project_name="global", modified=False)
            if not line:
                continue

            args = line.split()
            cmd = args[0]

            if cmd in ["exit", "quit"]:
                break
            elif cmd == "help":
                skin.help(commands_dict)
                continue

            # Route to Click subcommands by splitting line
            try:
                main.main(args=args, standalone_mode=False)
            except click.UsageError as e:
                skin.error(str(e))
            except click.exceptions.Exit:
                pass # normally happens on --help for subcommand
            except Exception as e:
                skin.error(f"Command failed: {e}")
                # Traceback for debugging
                # skin.error(traceback.format_exc())

        except (KeyboardInterrupt, EOFError):
            break

    skin.print_goodbye()

# Register subcommands
main.add_command(agent_group, name="agent")
main.add_command(scenario_group, name="scenario")
main.add_command(event_group, name="event")
