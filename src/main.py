from config_loader import load_system_prompt
from schemas import AgentDecision, ToolCall, YieldToUser, validate_agent_decision


# Test loader in config_loader.py
def main() -> None:
  # Load the system prompt from the config file.
  # This confirms that the config-based prompt setup from Phase 2 still works
  system_prompt = load_system_prompt()

  print("Assignment 2 Part 2 Agent")
  print("System prompt loaded successfully.")
  print(f"System prompt length: {len(system_prompt)} characters")
  print()

  # Create an example decision where the model wants to call a tool.
  # In the real agent loop, this kind of object will come from the LLM.
  tool_decision = AgentDecision(
    decision="tool_call",
    reason="I need to inspect the project files.",
    tool_call=ToolCall(
      tool_name="bash",
      arguments={"command": "ls -la"},
    ),
  )

  # Validate that the tool decision is logically correct.
  validate_agent_decision(tool_decision)

  # Create an example decision where the model is done and wants to answer the user.
  final_decision = AgentDecision(
    decision="yield_to_user",
    reason="The task is complete",
    yield_to_user=YieldToUser(
      final_answer="The structured outpit schemas is working"
    ),
  )

  # Validate that the final response decision is logically correct.
  validate_agent_decision(final_decision)

  print("Structured output schema test passed")
  print()
  # Print examples so we can visually confirm the structured format.
  print("Example tool decision:")
  print(tool_decision.model_dump_json(indent=2))
  print()
  print("Example final decision:")
  print(final_decision.model_dump_json(indent=2))

if __name__ == "__main__":
  main()

