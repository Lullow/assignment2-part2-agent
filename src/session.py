from schemas import AgentDecision, ToolResult


class Session:
  """
  Stores conversation history during one program run.

  This gives the agent memory within the current serssion.
  Multi-session presistence is not required for this assignment part.
  """

  def __init__(self, system_prompt: str) -> None:
    # Start the conversation with the system prompt.
    # This defines the agent's rules and behavior.
    self.messages: list[dict[str, str]] = [
      {
        "role": "system",
        "content": system_prompt,
      }
    ]

  def add_user_message(self, content: str) -> None:
    """
    Add the user's task to the session history.
    """
    # Store the user's input so the model can see the original task.
    self.messages.append(
      {
        "role": "user",
        "content": content,
      }
    )

  def add_agent_decision(self, descision: AgentDecision) -> None:
    """
    Store the model's strudtured decision as assistant context.
    """
    # Save the model's decision so the next step has access to it.
    self.messages.append(
      {
        "role": "assistant",
        "content": descision.model_dump_json(indent=2)
      }
    )


  def add_tool_result(self, result: ToolResult) -> None:
    """
    Add a tool observation back into the conversation

    The model can use this obervation to decide the next step.
    """
    # Convert the tool result into a readable observation for the model.
    observation = (
      f"Tool result from {result.tool_name}:\n"
      f"success: {result.success}\n"
      f"output:\n{result.output}\n"
      f"error:\n{result.error}"
    )

    # Add the observation as a user message so the agent can react to it.
    self.messages.append(
      {
        "role": "user",
        "content": f"OBSERVATION:\n{observation}"
      }
    )

