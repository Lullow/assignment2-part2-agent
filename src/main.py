"""from config_loader import load_system_prompt
from schemas import AgentDecision, ToolCall, YieldToUser, validate_agent_decision


# ----------------- TEST 2---------------------

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
  print(final_decision.model_dump_json(indent=2))"""

"""
# ------------------- TEST 3 --------------------------
from config_loader import load_system_prompt
from llm_client import get_agent_decision


def main() -> None:
    # Load the SWE/safety system prompt from config
    system_prompt = load_system_prompt()

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": "List the files in this project. Do not execute anything yet, only choose the correct next structured decision.",
        },
    ]

    print("Assignment 2 Part 2 Agent")
    print("Requesting structured decision from model...")
    print()

    # Test that the model can return a structured AgentDecision.
    decision = get_agent_decision(messages)

    print("Structured decision received:")
    print(decision.model_dump_json(indent=2))
"""


"""
# ---------------- TEST 4: ------------------
from schemas import ToolCall
from tool_registry import execute_tool_call


def main() -> None:
  print("Assignment 2 Part 2 Agent")
  print("Testing tool registry...")
  print()

  # Manual test cases for checking that the tool registry routes calls correctly.
  tests = [
    # Should pass: safe bash command.
    ToolCall(
      tool_name="bash",
      command="ls -la",
    ),

    # Should pass if README.md exists in the project root.
    ToolCall(
      tool_name="read_file",
      path="README.md",
    ),

    # Should be blocked by the bash safety layer.
    ToolCall(
      tool_name="bash",
      command="rm README.md",
    ),
  ]

  # Run each test call and print the structured ToolResult.
  for test in tests:
    print(f"Running tool: {test.tool_name}")
    result = execute_tool_call(test)
    print(result.model_dump_json(indent=2))
    print("-" * 60)"""



"""# ------- TEST 5 ------------
from agent_loop import run_agent
from config_loader import load_system_prompt


def main() -> None:
    # Load the system prompt from the configuration file.
    # This defines the agent's role, rules, and behavior.
    system_prompt = load_system_prompt()

    print("Assignment 2 Part 2 Agent")
    print("Type a software engineering task for the agent.")
    print()

    # Ask the user what task the agent should perform.
    # strip() removes extra whitespace before and after the input.
    user_task = input("Task: ").strip()

    # Stop early if the user did not enter a task.
    if not user_task:
        print("No task provided.")
        return

    # Run the agent loop with the user's task and the loaded system prompt.
    final_answer = run_agent(
        user_task=user_task,
        system_prompt=system_prompt,
    )

    print()
    print("--------- FINAL ANSWER ---------")
    print(final_answer)"""







"""# ---------- TEST 6 ---------------
from schemas import ToolCall
from tool_registry import execute_tool_call


def main() -> None:
  print("Assignment 2 Part 2 Agent")
  print("Testing edit_file_section tool...")
  print()

  test = ToolCall(
    tool_name="edit_file_section",
    path="README.md",
    old_text="This is a Python-based software engineering agent for Assignment 2 Part 2.",
    new_text=(
      "This is a Python-based software engineering agent for Assignment 2 Part 2. "
      "It uses structured output, safe tools, and a custom agent loop."
    ),
  )

  result = execute_tool_call(test)

  print(result.model_dump_json(indent=2))"""





from agent_loop import run_agent
from config_loader import load_system_prompt


def main() -> None:
  system_prompt = load_system_prompt()

  print("Assignment 2 Part 2 Agent")
  print("Type a software engineering task for the agent.")
  print()

  user_task = input("Task: ").strip()

  if not user_task:
    print("No task provided.")
    return

  final_answer = run_agent(
    user_task=user_task,
    system_prompt=system_prompt,
  )

  print()
  print("--------- FINAL ANSWER ---------")
  print(final_answer)




if __name__ == "__main__":
    main()
