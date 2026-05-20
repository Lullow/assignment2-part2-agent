from pathlib import Path

from output_limiter import limit_output
from schemas import ToolResult
from path_safety import is_inside_project, is_sensitive_path

# Resolve the project root so file access can be restricted to this project.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent



def read_file(path: str) -> ToolResult:
  """
  Read a file from the current project.

  The path must stay inside the project root and must not point to sensitive
  files or directories such as .env, .git, .venv, logs, or __pycache__.
  """

  try:
      # Convert the user-provided path into an absolute resolved path.
      # This also handles things like "../" before we do safety checks.
      requested_path = (PROJECT_ROOT / path).resolve()

      # Block attempts to read files outside the project directory.
      if not is_inside_project(requested_path, PROJECT_ROOT):
        return ToolResult(
          success=False,
          tool_name="read_file",
          output="",
          error="Access denied: path is outside the project root.",
        )

      # Block files and folders that may contain secrets or generated data.
      if is_sensitive_path(requested_path, PROJECT_ROOT):
        return ToolResult(
          success=False,
          tool_name="read_file",
          output="",
          error="Access denied: path points to a sensitive or ignored project file.",
        )

      # Make sure the requested file actually exists.
      if not requested_path.exists():
        return ToolResult(
          success=False,
          tool_name="read_file",
          output="",
          error=f"File not found: {path}",
        )

      # Only allow reading files, not folders.
      if not requested_path.is_file():
        return ToolResult(
          success=False,
          tool_name="read_file",
          output="",
          error=f"Path is not a file: {path}",
        )

      # Read the file content as text.
      content = requested_path.read_text(encoding="utf-8")

      # Limit the returned output so large files do not flood the context.
      return ToolResult(
        success=True,
        tool_name="read_file",
        output=limit_output(content),
        error=None,
      )

  except Exception as exc:
    # Return errors as ToolResult instead of crashing the agent loop.
    return ToolResult(
      success=False,
      tool_name="read_file",
      output="",
      error=str(exc),
    )