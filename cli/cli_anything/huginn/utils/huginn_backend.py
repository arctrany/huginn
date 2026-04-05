import os
import subprocess
import json
import shutil
import tempfile

def find_huginn_runner():
    """Check if we can run rails runner in docker, else fallback to local."""
    # Check if docker container 'huginn' is running
    try:
        proc = subprocess.run(["docker", "ps", "-q", "-f", "name=huginn"], capture_output=True, text=True, check=True)
        if proc.stdout.strip():
            # Container is running
            return ["docker", "exec", "-i", "huginn", "bundle", "exec", "rails", "runner", "-"]
    except Exception:
        pass
        
    ruby_path = shutil.which("ruby")
    if not ruby_path:
        raise RuntimeError(
            "Ruby is not installed and 'huginn' docker container is not running. CLI-Anything Huginn backend requires one of them."
        )
    return ["bundle", "exec", "rails", "runner", "-"]

def run_ruby_script(script_code: str) -> dict:
    """Execute a ruby script synchronously inside the Huginn environment and parse JSON result."""
    runner_cmd = find_huginn_runner()

    # Wrap script to ensure JSON formatted safely
    wrapped_script = f"""
    begin
      require 'json'
      result = begin
{script_code}
      end
      puts JSON.generate({{"success" => true, "data" => result}})
    rescue => e
      puts JSON.generate({{"success" => false, "error" => e.message, "backtrace" => e.backtrace}})
      exit 1
    end
    """
    
    try:
        cwd = os.environ.get("HUGINN_ROOT", os.getcwd())
        
        proc = subprocess.run(
            runner_cmd,
            input=wrapped_script,
            cwd=cwd,
            capture_output=True,
            text=True
        )

        try:
            # Parse only the last line or parse the output
            lines = [line for line in proc.stdout.strip().split('\n') if line.strip()]
            last_line = lines[-1] if lines else "{}"
            result = json.loads(last_line)
            if not result.get("success"):
                raise RuntimeError(f"Rails Script Error: {result.get('error')}")
            return result.get("data")
        except json.JSONDecodeError:
            raise RuntimeError(f"Failed to parse backend output.\\nSTDOUT: {proc.stdout}\\nSTDERR: {proc.stderr}")

    except Exception as e:
        raise RuntimeError(f"Failed to run backend: {e}")

def back_agent_list():
    code = "Agent.all.map { |a| { id: a.id, type: a.type, name: a.name, disabled: a.disabled, events_count: a.events_count } }"
    return run_ruby_script(code)

def back_agent_info(agent_id):
    code = f"a = Agent.find({agent_id}); {{ id: a.id, name: a.name, options: a.options, schedule: a.schedule, last_check_at: a.last_check_at }}"
    return run_ruby_script(code)

def back_agent_trigger(agent_id):
    code = f"a = Agent.find({agent_id}); a.check!; {{ triggered: true, time: Time.now }}"
    return run_ruby_script(code)

def back_agent_delete(agent_id):
    code = f"a = Agent.find({agent_id}); a.destroy; {{ deleted: true }}"
    return run_ruby_script(code)

def back_scenario_list():
    code = "Scenario.all.map { |s| { id: s.id, name: s.name, description: s.description, tag_bg_color: s.tag_bg_color, agent_count: s.agents.count } }"
    return run_ruby_script(code)

def back_scenario_export(scenario_id):
    code = f"s = Scenario.find({scenario_id}); JSON.parse(s.export.to_json)"
    return run_ruby_script(code)

def back_scenario_import(scenario_json_path):
    code = f"""
      file_content = File.read('{scenario_json_path}')
      parsed = JSON.parse(file_content)
      import = ScenarioImport.new(parsed)
      import.set_user(User.first) # default to first user
      if import.valid?
        import.import_confirmed
        {{ imported: true }}
      else
        {{ imported: false, errors: import.errors.full_messages }}
      end
    """
    return run_ruby_script(code)

def back_event_list(agent_id=None):
    if agent_id:
        code = f"Event.where(agent_id: {agent_id}).order(id: :desc).limit(20).map {{ |e| {{ id: e.id, agent_id: e.agent_id, payload: e.payload, created_at: e.created_at }} }}"
    else:
        code = "Event.order(id: :desc).limit(20).map { |e| { id: e.id, agent_id: e.agent_id, payload: e.payload, created_at: e.created_at } }"
    return run_ruby_script(code)

def back_event_clear():
    code = "Event.delete_all; { cleared: true }"
    return run_ruby_script(code)
