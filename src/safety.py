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
}


def is_safe_bash_command(command: str) -> tuple[bool, str]:
  """
  Check whether a bash command is allowed to run.

  This is a conservative safety layer. It blocks destructive commands,
  shell chaining, redirection, and risky patterns.
  """

  # Normalize whitespace before checking the command.
  stripped_command = command.strip()

  # Empty commands should never be executed.
  if not stripped_command:
    return False, "Empty command is not allowed."

  # The first word is treated as the base command, for example "ls" in "ls -la".
  command_parts = stripped_command.split()
  base_command = command_parts[0]

  # Block commands like rm, sudo, curl, and wget directly.
  if base_command in BLOCKED_COMMANDS:
    return False, f"Blocked command: {base_command}"

  # Block shell operators that could combine commands or redirect output.
  for operator in BLOCKED_OPERATORS:
    if operator in stripped_command:
      return False, f"Blocked shell operator: {operator}"

  # Lowercase the command so pattern checks are case-insensitive.
  lowered_command = stripped_command.lower()

  # Block known dangerous patterns such as rm -rf or disk device access.
  for pattern in BLOCKED_PATTERNS:
    if pattern in lowered_command:
      return False, f"Blocked risky pattern: {pattern}"

  return True, "Command passed safety checks."