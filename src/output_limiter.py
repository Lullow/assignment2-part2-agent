MAX_TOOL_OUTPUT_CHARS = 4000


def limit_output(output: str, max_chars: int = MAX_TOOL_OUTPUT_CHARS) -> str:
  """
  Limit tool output so the agent does not send huge outputs abck to the model.

  This is important for cost control, context control, and safety.
  """

  # Small outputs can be returned unchanged.
  if len(output) <= max_chars:
    return output

  # Large outputs are truncated so the model only receives a controlled amount of text.
  return (
    output[:max_chars]
    + "\n\n[OUTPUT TRUNCATED]\n"
    + f"Only the first {max_chars} characters are shown."
  )
