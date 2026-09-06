"""Runtime model configuration. Never hard-code models, keys, or limits in harness code."""
from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULTS = {
    "provider": "claude-cli",   # claude-cli | anthropic | openai
    "model": "sonnet",
    "max_steps": 30,
    "step_timeout_s": 300,
    "run_timeout_s": 1800,
    "max_tool_output_chars": 6000,
    "context_budget_chars": 60000,
    "llm_retries": 3,
    "effort": None,
}


def load_model_config(path: str | None) -> dict:
    cfg = dict(DEFAULTS)
    if path:
        cfg.update(json.loads(Path(path).read_text()))
    # environment overrides (provider-neutral names)
    env_map = {
        "MODEL_NAME": "model", "MODEL_ID": "model", "CONTAINER_MODEL_NAME": "model",
        "LLM_PROVIDER": "provider",
        "OPENAI_BASE_URL": "base_url", "CONTAINER_OPENAI_BASE_URL": "base_url", "BASE_URL": "base_url",
        "OPENAI_API_KEY": "api_key", "CONTAINER_OPENAI_API_KEY": "api_key", "API_KEY": "api_key",
        "HARNESS_MAX_STEPS": "max_steps",
    }
    for env, key in env_map.items():
        if os.environ.get(env) and key not in (json.loads(Path(path).read_text()) if path else {}):
            cfg[key] = int(os.environ[env]) if key == "max_steps" else os.environ[env]
    return cfg
