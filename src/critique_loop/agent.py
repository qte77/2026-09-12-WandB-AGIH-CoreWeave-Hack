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


@weave.op()
def attempt_task(client: OpenAI, settings: Settings, task: Task) -> str:
    response = client.chat.completions.create(
        model=settings.openrouter_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"{task.prompt}\n\n```python\n{task.starter_code}\n```",
            },
        ],
    )
    return (response.choices[0].message.content or "").strip()


@weave.op()
def refine_task(
    client: OpenAI,
    settings: Settings,
    task: Task,
    previous_code: str,
    failure_output: str,
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
                    "\n\nFix it. Reply with ONLY the corrected function's source code."
                ),
            },
        ],
    )
    return (response.choices[0].message.content or "").strip()
