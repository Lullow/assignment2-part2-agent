import os
import time
from typing import Any

import requests


HUB_URL = os.getenv("HUB_URL", "https://wb48jtfnjng6on-8080.proxy.runpod.net")
HUB_PASSWORD = os.getenv("HUB_PASSWORD")
AGENT_NAME = os.getenv("AGENT_NAME", "lullo-test-agent")

REQUEST_INTERVAL_SECONDS = 1.2
MAX_LOOPS = int(os.getenv("HUB_MAX_LOOPS", "60"))


def require_config() -> None:
    """
    Validate required environment variables before starting the bot.
    """

    if not HUB_PASSWORD:
        raise ValueError("HUB_PASSWORD is missing. Set it before running the bot.")


def fetch_messages(since: int) -> list[dict[str, Any]]:
    """
    Fetch messages from the hub after a specific sequence number.
    """

    response = requests.get(
        f"{HUB_URL}/api/messages",
        params={
            "since": since,
            "password": HUB_PASSWORD,
        },
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    return data.get("messages", [])


def post_message(content: str) -> None:
    """
    Send one message to the hub.
    """

    response = requests.post(
        f"{HUB_URL}/api/message",
        json={
            "agent_name": AGENT_NAME,
            "content": content,
            "password": HUB_PASSWORD,
        },
        timeout=10,
    )

    response.raise_for_status()


def get_message_sequence(message: dict[str, Any]) -> int:
    """
    Read the message sequence number.

    The hub uses sequence numbers so clients can fetch only newer messages.
    """

    return int(message.get("seq", 0))


def should_respond(message: dict[str, Any]) -> bool:
    """
    Decide whether this bot should respond to a hub message.

    The bot only responds when its name is mentioned.
    It ignores its own messages to avoid self-reply loops.
    """

    sender = message.get("agent_name", "")
    content = message.get("content", "")

    if sender == AGENT_NAME:
        return False

    return AGENT_NAME.lower() in content.lower()


def build_response(message: dict[str, Any]) -> str:
    """
    Build a small safe response.

    This is only a smoke-test bot, not the full Part 3 agent.
    """

    sender = message.get("agent_name", "someone")

    return (
        f"Hello {sender}. {AGENT_NAME} is connected and ready. "
        "This is a simple hub smoke test, not the full Part 3 agent yet."
    )


def get_initial_since() -> int:
    """
    Start from the latest current message so the bot does not reply to old history.
    """

    messages = fetch_messages(since=0)

    if not messages:
        return 0

    return max(get_message_sequence(message) for message in messages)


def main() -> None:
    require_config()

    print(f"Starting hub smoke-test bot as: {AGENT_NAME}")
    print(f"Hub: {HUB_URL}")
    print("Listening for mentions...")
    print()

    since = get_initial_since()
    responded_to: set[int] = set()

    for loop_number in range(1, MAX_LOOPS + 1):
        messages = fetch_messages(since=since)

        for message in messages:
            sequence = get_message_sequence(message)
            since = max(since, sequence)

            sender = message.get("agent_name", "unknown")
            content = message.get("content", "")

            print(f"[{sequence}] {sender}: {content}")

            if sequence in responded_to:
                continue

            if should_respond(message):
                response = build_response(message)
                post_message(response)
                responded_to.add(sequence)

                print(f"Responded to message {sequence}.")
                time.sleep(REQUEST_INTERVAL_SECONDS)

        time.sleep(REQUEST_INTERVAL_SECONDS)

    print("Hub smoke-test bot stopped after MAX_LOOPS.")


if __name__ == "__main__":
    main()
