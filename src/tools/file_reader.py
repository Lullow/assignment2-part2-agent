from pathlib import Path

from output_limiter import limit_output
from schemas import ToolResult

# Resolve the project root so file access can be restricted to this project.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent



def read_file(path: str) -> ToolResult:
  """
  Read a file from the current project.

  The path must stay inside the project root to avoid reading files outside
  the assignment project.
  """

  try:
    # Resolve the requested path to prevent tricks like "../../".
    requested_path = (PROJECT_ROOT / path).resolve()

    # Refuse access if the resolved path points outside the project folder.
    if not str(requested_path).startswith(str(PROJECT_ROOT)):
      return ToolResult(
        success=False,
        tool_name="read_file",
        output="",
        error="Access denied: path is outside the project root"
      )

    # Make sure the target exists before trying to read it.
    if not requested_path.exists():
      return ToolResult(
        success=False,
        tool_name="read_file",
        output="",
        error=f"File not found: {path}"
      )

    # Only regular files should be readable by this tool, not folders.
    if not requested_path.is_file():
      return ToolResult(
        success=False,
        tool_name="read_file",
        output="",
        error=f"Path is not a file: {path}"
      )

    # Read the file as UTF-8 text and limit the output before returning it to the agent.
    content = requested_path.read_text(encoding="utf-8")

    return ToolResult(
      success=True,
      tool_name="read_file",
      output=limit_output(content),
      error=None
    )


  except Exception as exc:
    return ToolResult(
      success=False,
      tool_name="read_file",
      output="",
      error=str(exc)
    )

