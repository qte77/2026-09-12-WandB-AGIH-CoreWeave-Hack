"""The critique-refine loop: attempt -> execute -> (on failure) refine -> re-execute.

Weave instrumentation is intentionally minimal and early: `weave.init()` auto-traces every
Anthropic call (including any tool use) with zero extra code, and `@weave.op()` on the
orchestration functions gives the trace a clean session/turn/step shape. A classic
`wandb.log()` run records per-iteration pass/fail so W&B ARIA (which reads classic Runs, not
Weave traces) has real data to analyze.
"""

from dataclasses import dataclass

import wandb
import weave
from openai import OpenAI

from critique_loop.agent import attempt_task, refine_task
from critique_loop.evaluator import execute_candidate
from critique_loop.settings import Settings, get_settings
from critique_loop.tasks import TASKS, Task


@dataclass(frozen=True)
class TaskOutcome:
    task_id: str
    passed: bool
    iterations_used: int


@weave.op()
def run_task(client: OpenAI, settings: Settings, task: Task) -> TaskOutcome:
    code = attempt_task(client, settings, task)
    result = execute_candidate(code, task.test_code)
    iteration = 1

    while not result.passed and iteration < settings.max_refine_iterations:
        code = refine_task(client, settings, task, code, result.output)
        result = execute_candidate(code, task.test_code)
        iteration += 1

    wandb.log(
        {
            "task_id": task.id,
            "passed": result.passed,
            "iterations_used": iteration,
        }
    )
    return TaskOutcome(task_id=task.id, passed=result.passed, iterations_used=iteration)


@weave.op()
def run_all() -> list[TaskOutcome]:
    settings = get_settings()
    client = OpenAI(api_key=settings.openrouter_api_key, base_url=settings.openrouter_base_url)

    weave.init(f"{settings.wandb_entity or ''}/{settings.wandb_project}".lstrip("/"))
    wandb.init(
        entity=settings.wandb_entity,
        project=settings.wandb_project,
        job_type="critique-refine-loop",
    )

    outcomes = [run_task(client, settings, task) for task in TASKS]

    pass_rate = sum(o.passed for o in outcomes) / len(outcomes)
    wandb.log({"final_pass_rate": pass_rate})
    wandb.finish()
    return outcomes
