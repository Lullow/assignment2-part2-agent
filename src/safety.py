import shlex
from pathlib import Path


# Commands that are too destructive or risky for this assignment agent.
BLOCKED_COMMANDS = {
  "rm",
  "sudo",
  "shutdown",
  "reboot",
  "mkfs",
  "dd",
  "chmod",
  "chown",
  "curl",
  "wget",
  "ssh",
  "scp",
  "mv",
  "cp",
  "find",
  "python",
  "python3",
  "pip",
  "git",
}

# Operators that allow chaining, redirection, command substitution, or piping.
BLOCKED_OPERATORS = {
  ";",
  "&&",
  "||",
  "|",
  ">",
  ">>",
  "<",
  "$(",
  "`",
}

# Extra dangerous command patterns that should be blocked even if split differently.
BLOCKED_PATTERNS = {
  "rm -rf",
  "curl | bash",
  "wget | bash",
  "/dev/sda",
  "/dev/nvme",
  "find -delete",
  "git clean",
  "git reset --hard",
  "python -c",
  "python3 -c",
  "/bin/rm",
  "/usr/bin/rm",
}


def is_safe_bash_command(command: str) -> tuple[bool, str]:
  """
  Check whether a bash command is allowed to run.

  This is a conservative safety layer. It blocks destructive commands,
  shell chaining, redirection, and risky patterns.

  This is still a guardrail, not a full sandbox.
  """

  # Normalize whitespace before checking the command.
  stripped_command = command.strip()

  # Empty commands should never be executed.
  if not stripped_command:
    return False, "Empty command is not allowed."

  # Multi-line commands are harder to reason about and should not be executed.
  if "\n" in stripped_command or "\r" in stripped_command:
    return False, "Multi-line commands are not allowed."

  # Block shell operators that could combine commands or redirect output.
  # Sorting by length makes sure ">>" is checked before ">".
  for operator in sorted(BLOCKED_OPERATORS, key=len, reverse=True):
    if operator in stripped_command:
      return False, f"Blocked shell operator: {operator}"

  # Use shlex.split instead of normal split so quoted strings are parsed
  # more like a real shell command.
  try:
    command_parts = shlex.split(stripped_command)
  except ValueError:
    return False, "Invalid command syntax."

  if not command_parts:
    return False, "Empty command is not allowed."

  # Normalize the base command.
  # Example: "/bin/rm file.txt" becomes "rm".
  base_command = Path(command_parts[0]).name.lower()

  # Block commands like rm, sudo, curl, wget, python3, git, etc.
  if base_command in BLOCKED_COMMANDS:
    return False, f"Blocked command: {base_command}"

  # Lowercase the command so pattern checks are case-insensitive.
  lowered_command = stripped_command.lower()

  # Block known dangerous patterns such as rm -rf, git clean, or python -c.
  for pattern in BLOCKED_PATTERNS:
    if pattern in lowered_command:
      return False, f"Blocked risky pattern: {pattern}"

  return True, "Command passed safety checks."