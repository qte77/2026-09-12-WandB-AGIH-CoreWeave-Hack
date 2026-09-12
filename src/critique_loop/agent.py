"""Thin, provider-agnostic wrapper over an OpenAI-compatible chat completions endpoint.

Deliberately not tied to any single vendor's SDK (freellmapi was considered and rejected —
its own README says "personal experimentation only" — OpenRouter is the actual choice, see
findings.md). Because the provider is swappable via base_url/model, these two functions are
explicitly `@weave.op()`-decorated rather than relying on any provider-specific auto-patch:
that keeps the trace complete no matter which OpenAI-compatible backend is configured.
"""

import weave
from openai import OpenAI

from critique_loop.settings import Settings
from critique_loop.tasks import Task

SYSTEM_PROMPT = (
    "You are a precise Python bug-fixer. Reply with ONLY the corrected function's source "
    "code. No markdown fences, no explanation, no surrounding text."
)


def _strip_markdown_fences(text: str) -> str:
    """Models routinely wrap code in ```python fences despite instructions not to -
    stripping defensively here is more reliable than tightening the prompt further."""
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        lines = lines[1:]  # drop opening ``` or ```python
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines)
    return stripped.strip()


@weave.op()
def attempt_task(client: OpenAI, settings: Settings, task: Task) -> str:
    """Uses the draft model (falls back to the main model if none is configured) - a
    draft-then-verify-then-escalate cascade, not a demo trick: the full model only gets
    invoked (in refine_task) when the cheap draft actually fails."""
    response = client.chat.completions.create(
        model=settings.openrouter_draft_model or settings.openrouter_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"{task.prompt}\n\n```python\n{task.starter_code}\n```",
            },
        ],
    )
    return _strip_markdown_fences(response.choices[0].message.content or "")


@weave.op()
def refine_task(
    client: OpenAI,
    settings: Settings,
    task: Task,
    previous_code: str,
    failure_output: str,
    failure_category: str,
) -> str:
    response = client.chat.completions.create(
        model=settings.openrouter_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"{task.prompt}\n\nYour previous attempt:\n```python\n{previous_code}\n```"
                    f"\n\nRunning the tests against it failed with:\n```\n{failure_output}\n```"
                    f"\n\nDiagnosed failure category: {failure_category}"
                    "\n\nFix it. Reply with ONLY the corrected function's source code."
                ),
            },
        ],
    )
    return _strip_markdown_fences(response.choices[0].message.content or "")
