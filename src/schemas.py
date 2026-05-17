from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
  """
  Represents a tool call requested by the model.

  The model does not execute tools directly.
  It only returns a structured request, and our Python agent loop decides
  weather the tool is valid and safe to run.
  """

  tool_name: Literal[
    "bash",
    "readl_file",
    "edit_file_section",
  ] = Field(
    description="The name of the tool the model wants to call"
  )


  # Each tool can require different arguments.
  # For example:
  # - bash: {"command": "ls -la"}
  # - read_file: {"path": "README.md"}
  # - edit_file_section: {"path": "...", "old_text": "...", "new_text": "..."}
  arguments: dict[str, Any] = Field(
    default_factory=dict,
    description="Arguments for the selected tool."
  )



class YieldToUser(BaseModel):
  """
  Represents a final response to the user.

  This is used when the agent is done with its work and should stop
  the tool-calling loop.
  """

  final_answer: str = Field(
    description="The final answer that should be shown to the user."
  )



class AgentDecision(BaseModel):
  """
  Struvtured decision returned by the model.

  Instead of parsing raw text like in Part 1, Part 2 uses a structured schema.

  The model must either:

  1. request a tool call:
    The agent wants to use a tool, such as "bash" or "read_file"

  2. yield a final answer to the user:
    The agent is finished and wants to respond to the user.

  Our own Python code still controls the agent loop, validation,
  safety checks, and actual tool execution
  """

  decision: Literal["tool_call", "yield_to_user"] = Field(
    description="Whether the model wants to call a tool or respond to the user."
  )

  # A short explanation is usefor for logging and debugging.
  # It lets us understand why the model made the decision.
  reason: str = Field(
    descritption="Brief explanation of why this decision was made."
  )

  # This should only be provided when decision == "tool_call"
  tool_call: ToolCall | None = Field(
    default=None,
    description="Tool call details. Required when decision is tool_call."
  )

  # This shuld only be provided when decision == "yield_to_user"
  yield_to_user: YieldToUser | None = Field(
    default=None,
    description="Final response detals. Required when decision is yield_to_user"
  )



def validate_agent_decision(decision: AgentDecision) -> None:
  """
  Validate that the structured decision i internally consistent.

  Pydantic validates the general shape of the object, but this function
  checks the relationships between fields.

  Example:
  - If decision is "tool_call", then tool_call must exist.
  - If decision is "yield_to_user", then yield_to_user must exist.
  - The model should not provide both "tool_call" and "yield_to_user" at once.
  """

  if decision.decision == "tool_call" and decision.tool_call is None:
    raise ValueError("Decision is 'tool_call', but tool_call is missing.")

  if decision.decision == "yield_to_user" and decision.yield_to_user is None:
    raise ValueError("Decision is 'yield_to_user', but yield_to_user is missing.")

  if decision.decision == "tool_call" and decision.yield_to_user is not None:
    raise ValueError("Decision is 'tool_call', but yield_to_user was also provided.")

  if decision.decision == "yield_to_user" and decision.tool_call is not None:
    raise ValueError("Decision is 'yield_to_user', but tool_call was also provided.")

