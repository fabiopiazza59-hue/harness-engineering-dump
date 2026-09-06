"""Provider-neutral LLM gateway.

Backends:
  claude-cli : shells out to `claude -p` in headless mode (no tools, custom system prompt)
  anthropic  : Anthropic Messages API over raw HTTPS (key from ANTHROPIC_API_KEY or config)
  openai     : any OpenAI-compatible chat-completions endpoint (base_url + api_key from config/env)

The gateway is configured, not policy: it sends messages and returns text plus usage.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.request


class LLMError(RuntimeError):
    pass


class LLM:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.provider = cfg.get("provider", "claude-cli")
        self.model = cfg.get("model")
        self.calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.cache_read_tokens = 0
        self.cost_usd = 0.0

    # ---------------------------------------------------------------- public
    def chat(self, system: str, messages: list[dict], max_tokens: int = 4000) -> str:
        """messages: [{"role": "user"|"assistant", "content": str}, ...]. Returns assistant text."""
        retries = int(self.cfg.get("llm_retries", 3))
        last = None
        for attempt in range(retries + 1):
            try:
                if self.provider == "claude-cli":
                    return self._claude_cli(system, messages)
                if self.provider == "anthropic":
                    return self._anthropic(system, messages, max_tokens)
                if self.provider == "openai":
                    return self._openai(system, messages, max_tokens)
                raise LLMError(f"unknown provider {self.provider}")
            except LLMError as e:
                last = e
                time.sleep(min(2 ** attempt, 20))
        raise LLMError(f"LLM call failed after {retries + 1} attempts: {last}")

    def usage(self) -> dict:
        return {"calls": self.calls, "input_tokens": self.input_tokens, "output_tokens": self.output_tokens,
                "cache_read_tokens": self.cache_read_tokens, "cost_usd": round(self.cost_usd, 4)}

    # -------------------------------------------------------------- backends
    @staticmethod
    def _flatten(messages: list[dict]) -> str:
        """The CLI takes one prompt; encode the transcript as a plain text conversation."""
        parts = []
        for m in messages:
            tag = "USER" if m["role"] == "user" else "ASSISTANT"
            parts.append(f"<<{tag}>>\n{m['content']}")
        parts.append("<<ASSISTANT>>")
        return "\n\n".join(parts)

    def _claude_cli(self, system: str, messages: list[dict]) -> str:
        cmd = ["claude", "-p", "--no-session-persistence", "--tools", "", "--output-format", "json",
               "--system-prompt", system]
        if self.model:
            cmd += ["--model", str(self.model)]
        if self.cfg.get("effort"):
            cmd += ["--effort", str(self.cfg["effort"])]
        timeout = int(self.cfg.get("step_timeout_s", 300))
        env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE",)}
        try:
            proc = subprocess.run(cmd, input=self._flatten(messages), capture_output=True, text=True,
                                  timeout=timeout, env=env)
        except subprocess.TimeoutExpired:
            raise LLMError("claude-cli timed out")
        if proc.returncode != 0 and not proc.stdout.strip():
            raise LLMError(f"claude-cli exit {proc.returncode}: {proc.stderr[-500:]}")
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            raise LLMError(f"claude-cli returned non-JSON: {proc.stdout[-300:]}")
        if data.get("is_error"):
            raise LLMError(f"claude-cli error: {data.get('result')}")
        u = data.get("usage", {})
        self.calls += 1
        self.input_tokens += int(u.get("input_tokens", 0)) + int(u.get("cache_creation_input_tokens", 0))
        self.cache_read_tokens += int(u.get("cache_read_input_tokens", 0))
        self.output_tokens += int(u.get("output_tokens", 0))
        self.cost_usd += float(data.get("total_cost_usd", 0) or 0)
        return data.get("result", "") or ""

    def _anthropic(self, system: str, messages: list[dict], max_tokens: int) -> str:
        key = self.cfg.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")
        base = self.cfg.get("base_url") or os.environ.get("ANTHROPIC_BASE_URL") or "https://api.anthropic.com"
        body = {"model": self.model, "max_tokens": max_tokens, "system": system,
                "messages": [{"role": m["role"], "content": m["content"]} for m in messages]}
        req = urllib.request.Request(f"{base.rstrip('/')}/v1/messages", data=json.dumps(body).encode(),
                                     headers={"content-type": "application/json", "x-api-key": key or "",
                                              "anthropic-version": "2023-06-01"})
        data = self._post(req)
        text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
        u = data.get("usage", {})
        self.calls += 1
        self.input_tokens += int(u.get("input_tokens", 0))
        self.output_tokens += int(u.get("output_tokens", 0))
        return text

    def _openai(self, system: str, messages: list[dict], max_tokens: int) -> str:
        key = self.cfg.get("api_key") or os.environ.get("OPENAI_API_KEY", "")
        base = self.cfg.get("base_url") or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        body = {"model": self.model, "messages": [{"role": "system", "content": system}] + messages}
        req = urllib.request.Request(f"{base.rstrip('/')}/chat/completions", data=json.dumps(body).encode(),
                                     headers={"content-type": "application/json", "authorization": f"Bearer {key}"})
        data = self._post(req)
        u = data.get("usage", {})
        self.calls += 1
        self.input_tokens += int(u.get("prompt_tokens", 0))
        self.output_tokens += int(u.get("completion_tokens", 0))
        return data["choices"][0]["message"]["content"] or ""

    def _post(self, req) -> dict:
        timeout = int(self.cfg.get("step_timeout_s", 300))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except Exception as e:  # noqa: BLE001 - surface as LLMError for retry
            raise LLMError(str(e))
