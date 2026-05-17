from pathlib import Path
from schemas import ToolResult

# Resolve the project root so edits can be restricted to this project.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def edit_file_section(path: str, old_text: str, new_text: str) -> ToolResult:
  """
  Replace one exact section of a file.

  This tool only edits a file if old_text exists exactly once.
  That makes file editing safer and more predictable.
  """

  try:
    # Resolve the requested path to prevent editing files outside the project via "../".
    requested_path = (PROJECT_ROOT / path).resolve()

    # Refuse edits outside the project root for safety.
    if not str(requested_path).startswith(str(PROJECT_ROOT)):
      return ToolResult(
        success=False,
        tool_name="edit_file_section",
        output="",
        error="Access denied: path is outside the project root.",
    )

    if not requested_path.exists():
      return ToolResult(
        success=False,
        tool_name="edit_file_section",
        output="",
        error=f"File not found: {path}",
    )

    if not requested_path.is_file():
      return ToolResult(
        success=False,
        tool_name="edit_file_section",
        output="",
        error=f"Path is not a file: {path}",
    )

    content = requested_path.read_text(encoding="utf-8")
    # Count exact matches so the tool only edits when the target text is unambiguous.
    occurrences = content.count(old_text)

    # If the old text is missing, the model probably targeted the wrong section.
    if occurrences == 0:
      return ToolResult(
        success=False,
        tool_name="edit_file_section",
        output="",
        error="old_text was not found in the file.",
    )

    # If the text appears more than once, editing could change the wrong section.
    if occurrences > 1:
      return ToolResult(
        success=False,
        tool_name="edit_file_section",
        output="",
        error="old_text appears multiple times. Refusing ambiguous edit.",
    )

    # Replace only the first and only confirmed occurrence.
    updated_content = content.replace(old_text, new_text, 1)
    requested_path.write_text(updated_content, encoding="utf-8")

    return ToolResult(
      success=True,
      tool_name="edit_file_section",
      output=f"Successfully edited section in {path}",
      error=None,
    )

  except Exception as exc:
    return ToolResult(
      success=False,
      tool_name="edit_file_section",
      output="",
      error=str(exc),
  )