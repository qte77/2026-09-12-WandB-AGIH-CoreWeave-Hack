"""The critique-refine loop: attempt -> execute -> (on failure) triage+refine -> re-execute.

Weave instrumentation is deliberately explicit rather than relying on provider auto-patching
(see agent.py): `weave.init()` first, then `@weave.op()` on every LLM/TypeSafe-touching
function, giving the trace a clean session/turn/step shape regardless of backend. A classic
`wandb.log()` run records per-iteration pass/fail (and the diagnosed failure category) so
W&B ARIA — which reads classic Runs, not Weave traces — has real data to analyze.
"""

from dataclasses import dataclass

import wandb
import weave
from openai import OpenAI
from typesafe_sdk import TypeSafeClient

from critique_loop.agent import attempt_task, refine_task
from critique_loop.evaluator import execute_candidate
from critique_loop.settings import Settings, get_settings
from critique_loop.tasks import TASKS, Task
from critique_loop.triage import classify_failure


@dataclass(frozen=True)
class TaskOutcome:
    task_id: str
    passed: bool
    iterations_used: int


@weave.op()
def run_task(
    llm_client: OpenAI, typesafe_client: TypeSafeClient, settings: Settings, task: Task
) -> TaskOutcome:
    code = attempt_task(llm_client, settings, task)
    result = execute_candidate(code, task.test_code)
    iteration = 1
    failure_category = ""

    while not result.passed and iteration < settings.max_refine_iterations:
        failure_category = classify_failure(typesafe_client, result.output)
        code = refine_task(llm_client, settings, task, code, result.output, failure_category)
        result = execute_candidate(code, task.test_code)
        iteration += 1

    wandb.log(
        {
            "task_id": task.id,
            "passed": result.passed,
            "iterations_used": iteration,
            "last_failure_category": failure_category,
        }
    )
    return TaskOutcome(task_id=task.id, passed=result.passed, iterations_used=iteration)


def run_all() -> list[TaskOutcome]:
    """Driver, not a traced op: it calls weave.init() itself, so tracing isn't live yet
    when it starts. The real units of work (run_task and everything it calls) are traced.
    """
    settings = get_settings()
    llm_client = OpenAI(
        api_key=settings.openrouter_api_key, base_url=settings.openrouter_base_url
    )
    typesafe_client = TypeSafeClient(api_key=settings.typesafe_api_key)

    # weave.init() requires "entity/project" explicitly - unlike wandb.init(), it won't
    # resolve a default entity on its own - so fall back to the account's default here.
    entity = settings.wandb_entity or wandb.Api().default_entity

    weave.init(f"{entity}/{settings.wandb_project}")
    wandb.init(
        entity=entity,
        project=settings.wandb_project,
        job_type="critique-refine-loop",
    )
    wandb.config.update(
        {
            "draft_model": settings.openrouter_draft_model or settings.openrouter_model,
            "refine_model": settings.openrouter_model,
        }
    )

    outcomes = [run_task(llm_client, typesafe_client, settings, task) for task in TASKS]

    pass_rate = sum(o.passed for o in outcomes) / len(outcomes)
    wandb.log({"final_pass_rate": pass_rate})
    wandb.finish()
    return outcomes
