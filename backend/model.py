"""Single approved model configuration for every Campus Customs agent."""

import os
from pathlib import Path

from dotenv import load_dotenv

from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
MODEL_NAME = "gpt-6-luna"
PORTKEY_BASE_URL = os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1")


def build_model() -> OpenAIChatModel:
    """Build the requested model through Portkey's OpenAI-compatible gateway."""
    api_key = os.getenv("PORTKEY_API_KEY")
    virtual_key = os.getenv("PORTKEY_VIRTUAL_KEY")
    headers = {"x-portkey-api-key": api_key or ""}
    if virtual_key:
        headers["x-portkey-virtual-key"] = virtual_key
    client = AsyncOpenAI(
        api_key=api_key or "missing-portkey-key",
        base_url=PORTKEY_BASE_URL,
        default_headers=headers,
    )
    return OpenAIChatModel(MODEL_NAME, provider=OpenAIProvider(openai_client=client))


AGENT_MODEL = build_model()
MODEL_POLICY = {
    "provider": "Portkey",
    "model": MODEL_NAME,
    "max_requests_per_run": 12,
    "max_delegation_depth": 4,
    "max_output_tokens": 1200,
    "reasoning_effort": "none",
}

MODEL_SETTINGS = {
    "max_tokens": MODEL_POLICY["max_output_tokens"],
    "openai_reasoning_effort": MODEL_POLICY["reasoning_effort"],
}
