"""Google Vertex AI backend (Gemini and Model-as-a-Service partner models).

Vertex AI exposes an OpenAI-compatible chat-completions endpoint::

    https://aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/endpoints/openapi

Authentication uses Google Application Default Credentials (run
``gcloud auth application-default login`` once); Vertex AI does not accept
plain API keys for this endpoint. Access tokens expire after ~1 hour and are
refreshed transparently.

Two additions over :class:`evaloop.models.closed_source.OpenAILLM`:

* ``batch_generate`` runs requests concurrently with a thread pool. The loop
  runner (``BatchEvaluationCycle``) already switches to batch mode whenever a
  model defines ``batch_generate``, so API models get the same batching path
  as vLLM models without touching the runner.
* Every request is appended to a JSONL call log (token usage, finish reason,
  latency, errors). The log is what lets us (a) report the cost of a run and
  (b) separate infrastructure errors and truncated outputs from genuine
  model failures during the failure analysis.
"""

import json
import logging
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from .base import BaseLLM

ERROR_PREFIX = "Error generating response"
_RETRYABLE_STATUS = {408, 409, 429, 500, 502, 503, 504}


class VertexAILLM(BaseLLM):
    """Chat model served by Vertex AI through its OpenAI-compatible endpoint."""

    DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."

    def __init__(self, model_config: Dict[str, Any], credentials: Any = None, client: Any = None):
        super().__init__(model_config)
        self.model_id = model_config["model_id"]
        self.project = model_config.get("project")
        self.location = model_config.get("location", "global")
        self.temperature = model_config.get("temperature", 0.0)
        self.top_p = model_config.get("top_p", 1.0)
        self.max_tokens = model_config.get("max_tokens", 1024)
        self.system_prompt = model_config.get("system_prompt", self.DEFAULT_SYSTEM_PROMPT)
        self.concurrency = max(1, int(model_config.get("concurrency", 8)))
        # ~12 retries with capped exponential backoff ~= 10 minutes of patience per request, so that
        # rate limiting (429) is absorbed instead of surfacing as a spurious model failure.
        self.max_retries = int(model_config.get("max_retries", 12))
        self.extra_body = model_config.get("extra_body") or None
        # For reasoning models: "low" | "medium" | "high" (None = provider default)
        self.reasoning_effort = model_config.get("reasoning_effort") or None
        self.call_log_path = model_config.get("call_log_path")
        self.logger = logging.getLogger(__name__)

        self._log_lock = threading.Lock()
        self._token_lock = threading.Lock()
        self._credentials = credentials
        self._client = client
        if self._client is None:
            if not self.project:
                raise ValueError("Vertex AI models need a GCP project (--vertex_project)")
            self._client = self._build_client()

    # ------------------------------------------------------------------ setup
    def _base_url(self) -> str:
        host = "aiplatform.googleapis.com" if self.location == "global" \
            else f"{self.location}-aiplatform.googleapis.com"
        return (f"https://{host}/v1/projects/{self.project}"
                f"/locations/{self.location}/endpoints/openapi")

    def _build_client(self):
        import google.auth
        from openai import OpenAI

        if self._credentials is None:
            self._credentials, _ = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
        return OpenAI(
            api_key=self._fresh_token(),
            base_url=self._base_url(),
            # Bills quota to the evaluation project when ADC are user credentials.
            default_headers={"x-goog-user-project": self.project},
            max_retries=0,  # retries are handled below, with logging
            timeout=180,
        )

    def _fresh_token(self) -> str:
        """Return a valid access token, refreshing it under a lock if needed."""
        if self._credentials is None:  # injected test client
            return "test-token"
        with self._token_lock:
            if not self._credentials.valid or self._credentials.expiry is None or \
                    (self._credentials.expiry.timestamp() - time.time()) < 300:
                import google.auth.transport.requests
                for attempt in range(6):  # transient network errors must not kill a run
                    try:
                        self._credentials.refresh(google.auth.transport.requests.Request())
                        break
                    except Exception as exc:  # noqa: BLE001
                        if attempt == 5:
                            raise
                        self.logger.warning(f"Token refresh failed ({exc}); retrying")
                        time.sleep(5 * (attempt + 1))
            return self._credentials.token

    # ------------------------------------------------------------- generation
    def _messages(self, prompt: str) -> List[Dict[str, str]]:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def generate(self, prompt: str, **kwargs) -> str:
        last_error: Optional[str] = None
        for attempt in range(self.max_retries + 1):
            start = time.time()
            try:
                if self._credentials is not None:
                    self._client.api_key = self._fresh_token()
                request = dict(
                    model=self.model_id,
                    messages=self._messages(prompt),
                    temperature=kwargs.get("temperature", self.temperature),
                    top_p=kwargs.get("top_p", self.top_p),
                    max_tokens=kwargs.get("max_tokens", self.max_tokens),
                )
                if self.reasoning_effort:
                    request["reasoning_effort"] = self.reasoning_effort
                if self.extra_body:
                    request["extra_body"] = self.extra_body
                response = self._client.chat.completions.create(**request)
                choice = response.choices[0]
                content = choice.message.content or ""
                usage = getattr(response, "usage", None)
                details = getattr(usage, "completion_tokens_details", None)
                if isinstance(details, dict):
                    reasoning_tokens = details.get("reasoning_tokens")
                else:
                    reasoning_tokens = getattr(details, "reasoning_tokens", None)
                self._log_call(
                    prompt=prompt, start=start, attempt=attempt,
                    finish_reason=getattr(choice, "finish_reason", None),
                    prompt_tokens=getattr(usage, "prompt_tokens", None),
                    completion_tokens=getattr(usage, "completion_tokens", None),
                    reasoning_tokens=reasoning_tokens,
                    output_chars=len(content),
                )
                # An empty answer is returned as is, not retried: under greedy decoding the same
                # request yields the same output (typically a reasoning model that spent the whole
                # token budget on hidden reasoning, finish_reason="length"). The call log records
                # it so these cases can be separated from ordinary failures in the analysis.
                return content
            except Exception as exc:  # noqa: BLE001 - network/API errors are retried
                status = getattr(exc, "status_code", None)
                last_error = f"{type(exc).__name__}({status}): {str(exc)[:300]}"
                self._log_call(prompt=prompt, start=start, attempt=attempt, error=last_error)
                if status is not None and status not in _RETRYABLE_STATUS:
                    break
            if attempt < self.max_retries:
                time.sleep(min(60.0, 2.0 * (2 ** attempt)) * (0.75 + 0.5 * random.random()))
        self.logger.error(f"Vertex AI request failed after retries: {last_error}")
        return f"{ERROR_PREFIX}: {last_error}"

    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate for many prompts concurrently; output order matches input order."""
        if not prompts:
            return []
        with ThreadPoolExecutor(max_workers=min(self.concurrency, len(prompts))) as pool:
            return list(pool.map(lambda p: self.generate(p, **kwargs), prompts))

    # ---------------------------------------------------------------- logging
    def _log_call(self, prompt: str, start: float, attempt: int, **fields: Any) -> None:
        if not self.call_log_path:
            return
        record = {
            "time": round(start, 3),
            "latency_s": round(time.time() - start, 3),
            "model": self.model_id,
            "attempt": attempt,
            "prompt_chars": len(prompt),
            **fields,
        }
        with self._log_lock:
            with open(self.call_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def __str__(self) -> str:
        return self.model_id
