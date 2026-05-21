#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${AGENT_IMAGE:-assignment2-part2-agent}"
CONTAINER_NAME="${AGENT_CONTAINER_NAME:-assignment2-part2-agent-run}"

docker build -t "$IMAGE_NAME" .

docker run \
  --rm \
  --name "$CONTAINER_NAME" \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 128 \
  --memory 512m \
  --cpus 1 \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  -e OPENAI_API_KEY="${OPENAI_API_KEY:?OPENAI_API_KEY is required}" \
  -e OPENAI_BASE_URL="${OPENAI_BASE_URL:-https://openrouter.ai/api/v1}" \
  -e MODEL_NAME="${MODEL_NAME:-openai/gpt-4o-mini}" \
  -it "$IMAGE_NAME"