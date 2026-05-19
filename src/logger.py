from datetime import datetime
from pathlib import Path

# Find the project root based on this file's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Store all agent run logs inside the logs/ folder.
LOG_DIR = PROJECT_ROOT / "logs"


class AgentLogger:
  """
  Writes a readable log file for one agent run.

  This helps with debugging and makes the agent's behavior easier to inspect.
  """

  def __init__(self) -> None:
    # Create the logs directory if it does not already exist.
    LOG_DIR.mkdir(exist_ok=True)

    # Use a timestamp so each agent run gets its own log file.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    self.log_path = LOG_DIR / f"agent_run_{timestamp}.log"

  def write(self, message: str) -> None:
    """
    Append a message to the current log file.
    """

    # Open the log file in append mode and write one line.
    with self.log_path.open("a", encoding="utf-8") as file:
      file.write(message)
      file.write("\n")

  def section(self, title: str) -> None:
    """
    Write a visible section heading to the log file.
    """

    # Add separators to make different parts of the log easier to read.
    self.write("")
    self.write("=" * 80)
    self.write(title)
    self.write("=" * 80)