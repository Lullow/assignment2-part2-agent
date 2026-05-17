import shlex
import subprocess
from pathlib import Path

from output_limiter import limit_output
from safety import is_safe_bash_command
from schemas import ToolResult

# All commands run from the project root, not from an arbitrary system folder.

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# Prevent long-running commands from hanging the agent loop.
TIMEOUT_SECONDS = 10


def run_bash(command: str) -> ToolResult:
  """
  Run a safe bash command inside the project root.

  The command is checked by the safety layer before execution.
  """

  # Check the command before running it.
  is_safe, safety_message = is_safe_bash_command(command)

  # If the safety layer rejects the command, return the reason instead of executing it.
  if not is_safe:
    return ToolResult(
      success=False,
      tool_name="bash",
      output="",
      error=safety_message,
    )

  try:
    # shlex.split turns the command string into a safe argument list.
    completed = subprocess.run(
      shlex.split(command),
      cwd=PROJECT_ROOT,        # Run inside the project root and avoid shell=True for safer execution.
      capture_output=True,
      text=True,
      timeout=TIMEOUT_SECONDS,
      shell=False,
    )

    # Return stdout, stderr, and the return code so the agent can reason about the result.
    output = (
      f"Return code: {completed.returncode}\n\n"
      f"STDOUT:\n{completed.stdout}\n\n"
      f"STDERR:\n{completed.stderr}"
    )

    # A zero return code means the command succeeded.
    return ToolResult(
      success=completed.returncode == 0,
      tool_name="bash",
      output=limit_output(output),
      error=None if completed.returncode == 0 else "Command returned non-zero exit code.",
    )

  except subprocess.TimeoutExpired:
    return ToolResult(
      success=False,
      tool_name="bash",
      output="",
      error=f"Command timed out after {TIMEOUT_SECONDS} seconds.",
    )

  except Exception as exc:
    return ToolResult(
      success=False,
      tool_name="bash",
      output="",
      error=str(exc),
    )