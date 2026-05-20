from pathlib import Path

# Folder names that tools should not read from or write to.
# These can contain secrets, generated files, logs, or internal project data.
SENSITIVE_PATH_PARTS = {
  ".git",
  ".venv",
  "venv",
  "env",
  "__pycache__",
  "logs",
}

# Specific file names that should always be blocked.
# .env often contains API keys and other secrets.
SENSITIVE_FILE_NAMES = {
    ".env",
}


def is_inside_project(path: Path, project_root: Path) -> bool:
  """
  Check whether a resolved path stays inside the project root.

  Path.relative_to is safer than string startswith checks because it compares
  actual path components instead of raw string prefixes.
  """

  try:
    # If this succeeds, the path is inside the project root.
    path.relative_to(project_root)
    return True
  except ValueError:
    # If relative_to fails, the path is outside the project root.
    return False


def is_sensitive_path(path: Path, project_root: Path) -> bool:
  """
  Check whether a path points to sensitive or ignored project areas.

  This prevents tools from reading or editing secrets, logs, virtual
  environments, git internals, or Python cache files.
  """

  try:
    # Convert the full path into a path relative to the project root.
    relative_path = path.relative_to(project_root)
  except ValueError:
    # Treat paths outside the project as sensitive by default.
    return True

  # Block exact sensitive file names, such as .env.
  if path.name in SENSITIVE_FILE_NAMES:
    return True

  # Check every folder/file part in the relative path.
  for part in relative_path.parts:
    if part in SENSITIVE_PATH_PARTS:
      return True
    # Block .env files that may contain secrets, but allow .env.example..
    if part == ".env" or (part.startswith(".env.") and part != ".env.example"):
      return True

  return False