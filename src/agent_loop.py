from llm_client import get_agent_decision
from session import Session
from tool_registry import execute_tool_call

# Limit how many times the agent is allowed to loop.
# This prevents infinite loops and unnecessary API/tool usage.
MAX_STEPS = 5


def run_agent(user_task: str, system_prompt: str) -> str:
    """
    Run the agent loop.

    The model can perform multiple tool-calling rounds before yielding
    a final answer to the user.
    """

    # Create a new session with the system prompt.
    # The session stores the conversation history during this run.
    session = Session(system_prompt=system_prompt)

    # Add the user's task to the conversation history.
    session.add_user_message(user_task)

    # Let the agent take multiple steps, but never more than MAX_STEPS.
    for step in range(1, MAX_STEPS + 1):
        print()
        print(f"--------- STEP {step} ---------")
        print("Requesting decision from model...")

        # Ask the model what it wants to do next.
        # The decision can either be a tool call or a final answer.
        decision = get_agent_decision(session.messages)
        # Store the model's decision so future steps have context.
        session.add_agent_decision(decision)

        print()
        print("Decision:")
        print(decision.model_dump_json(indent=2))

        # If the agent is done, return the final answer to the user.
        if decision.decision == "yield_to_user":
            if decision.yield_to_user is None:
                return "Agent tried to yield, but no final answer was provided."

            return decision.yield_to_user.final_answer

        # If the agent wants to use a tool, validate and execute that tool call.
        if decision.decision == "tool_call":
            if decision.tool_call is None:
                return "Agent tried to call a tool, but no tool call was provided."

            print()
            print(f"Executing tool: {decision.tool_call.tool_name}")

            # Run the requested tool through the tool registry.
            result = execute_tool_call(decision.tool_call)

            print()
            print("Tool result:")
            print(result.model_dump_json(indent=2))

            # Add the tool result back into the session as an observation.
            # This lets the model use the result in the next step.
            session.add_tool_result(result)
            continue

    # Stop safely if the agent did not finish within the step limit.
    return f"Stopped after reaching MAX_STEPS={MAX_STEPS}."
