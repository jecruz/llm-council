"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# Set LLM_PROVIDER in .env to switch backends.
# Accepted values: "llmdynamix" (default) | "openrouter" | "lmstudio"
PROVIDER = os.getenv("LLM_PROVIDER", "llmdynamix")

def _parse_models(env_var: str) -> list[str]:
    raw = os.getenv(env_var, "")
    return [m.strip() for m in raw.split(",") if m.strip()]

_PROVIDERS = {
    "llmdynamix": {
        # LLM Dynamix — Amp menu-bar proxy (formerly VibeProxy), OpenAI-compatible local proxy.
        # No real key required; any non-empty string satisfies the SDK.
        "api_url": "http://localhost:12444/v1/chat/completions",
        "api_key": "llmdynamix",
        "council_models": [
            "gpt-5.6-sol",
            "gpt-5.6-terra",
            "claude-opus-5",
            "claude-sonnet-5",
            "deepseek-v4-pro",
        ],
        "chairman_model": "claude-opus-5",
    },
    "openrouter": {
        # OpenRouter — multi-provider gateway, requires OPENROUTER_API_KEY in .env.
        # Model IDs use "provider/model" format.
        "api_url": "https://openrouter.ai/api/v1/chat/completions",
        "api_key": os.getenv("OPENROUTER_API_KEY", ""),
        "council_models": [
            "openai/gpt-5.1",
            "google/gemini-3-pro-preview",
            "anthropic/claude-sonnet-4.5",
            "x-ai/grok-4",
        ],
        "chairman_model": "google/gemini-3-pro-preview",
    },
    "lmstudio": {
        # LM Studio — local OpenAI-compatible server at 10.0.0.30:4521.
        # Model IDs match whatever is loaded in LM Studio.
        # Required .env vars:
        #   LM_STUDIO_COUNCIL_MODELS=model-a,model-b,model-c
        #   LM_STUDIO_CHAIRMAN_MODEL=model-a
        "api_url": "http://10.0.0.30:4521/v1/chat/completions",
        "api_key": "lmstudio",
        "council_models": _parse_models("LM_STUDIO_COUNCIL_MODELS"),
        "chairman_model": os.getenv("LM_STUDIO_CHAIRMAN_MODEL", ""),
    },
}

if PROVIDER not in _PROVIDERS:
    raise ValueError(
        f"Unknown LLM_PROVIDER '{PROVIDER}'. "
        "Choose 'llmdynamix', 'openrouter', or 'lmstudio'."
    )

if PROVIDER == "lmstudio":
    _cfg = _PROVIDERS["lmstudio"]
    if not _cfg["council_models"]:
        raise ValueError(
            "LM_STUDIO_COUNCIL_MODELS is not set. "
            "Load chat models in LM Studio, then set e.g.: "
            "LM_STUDIO_COUNCIL_MODELS=lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF,..."
        )
    if not _cfg["chairman_model"]:
        raise ValueError(
            "LM_STUDIO_CHAIRMAN_MODEL is not set. "
            "Set it to one of the models in LM_STUDIO_COUNCIL_MODELS."
        )

_active = _PROVIDERS[PROVIDER]
LLM_API_URL = _active["api_url"]
LLM_API_KEY = _active["api_key"]
COUNCIL_MODELS = _active["council_models"]
CHAIRMAN_MODEL = _active["chairman_model"]

# Data directory for conversation storage
DATA_DIR = "data/conversations"
