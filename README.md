# Assignment 2 Part 2 Agent

This is a Python-based software engineering agent for Assignment 2 Part 2.

The goal of Part 2 is to build a stronger version of the Part 1 ReAct agent using structured output, while still keeping the agent loop, context handling, tool-calling, safety checks, and tool execution in our own Python code.

## Planned Features

- Structured output from the model
- Custom agent loop
- Safe bash tool
- File reading tool
- File section editing tool
- Session history during runtime
- System prompt loaded from config file
- Tool output limits
- SWE-only behavior controlled by system prompt

## Project Structure

```text
src/
  main.py
  agent_loop.py
  llm_client.py
  schemas.py
  tool_registry.py
  safety.py
  session.py
  output_limiter.py
  logger.py
  tools/
    bash_tool.py
    file_reader.py
    file_editor.py
config/
  system_prompt.md