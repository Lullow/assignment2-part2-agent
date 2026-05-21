import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from schemas import AgentDecision, validate_agent_decision, normalize_agent_decision


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"


def load_enviroment() -> None:
  """
  Load environment variables.

  In local development, values can come from a .env file.
  In Docker, values are passed directly as environment variables, so .env
  does not need to exist inside the container.
  """

  if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH, override=True)



def create_client() -> OpenAI:
  """
  Create an OpenAI-compatible client.

  The API key, base URL, and model name are loaded from .env.
  This makes it possible to use OpenAI or another OpenAI-compatible provider.
  """
  load_dotenv(dotenv_path=ENV_PATH, override=True)

  api_key = os.getenv("OPENAI_API_KEY")
  base_url = os.getenv("OPENAI_BASE_URL")

  if not api_key:
    raise ValueError(f"OPEN_API_KEY is missing in .env at: {ENV_PATH}")

  if base_url:
    return OpenAI(api_key=api_key, base_url=base_url)

  return OpenAI(api_key=api_key)



def get_model_name() -> str:
  """
  Read the model name from .env.

  If MODEL_NAME is not set, a default model name is used.
  """
  load_enviroment()

  return os.getenv("MODEL_NAME", "gpt-4o-mini")



def get_agent_decision(messages: list[dict[str, str]]) -> AgentDecision:
  """
  Send message to the model and ask for a structured AgentDecision.

  The model must return data that matches the AgentDecision schema.
  Our Python code then validates the decision before the agent loop uses it.
  """
  client = create_client()
  model_name = get_model_name()

  # Ask the model to return output that matches our Pydantic schema.
  completion = client.chat.completions.parse(
    model=model_name,
    messages=messages,
    response_format=AgentDecision,
  )

  parsed_decision = completion.choices[0].message.parsed

  if parsed_decision is None:
    refusal = completion.choices[0].message.refusal
    raise ValueError(f"Model did not return a valid AgentDecision - Refusal: {refusal}")


  parsed_decision = normalize_agent_decision(parsed_decision)

  # Validate the cleaned decision before the agent loop uses it.
  validate_agent_decision(parsed_decision)

  return parsed_decision