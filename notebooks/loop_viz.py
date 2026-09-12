# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "wandb>=0.18",
#     "python-dotenv>=1.0",
#     "matplotlib>=3.8",
# ]
# ///

# Run with: uvx marimo run notebooks/loop_viz.py  (from the repo root, so .env resolves)
# Deliberately kept out of pyproject.toml/uv.lock - this is a standalone viz tool, not
# part of the critique-refine loop itself, run via marimo's own PEP 723 sandbox.

import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    from dotenv import load_dotenv

    load_dotenv()
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Critique-refine loop — real run data

    Pulled live from the W&B project (`wandb.Api()`, not hardcoded numbers) for
    CoreWeave Hacks: Agent Loops. Compares runs across different draft/refine model
    configurations to show the loop and TypeSafe triage actually firing.
    """)
    return


@app.cell
def _(mo):
    import wandb

    api = wandb.Api()
    runs = api.runs("w77/coreweave-hacks-2026-09-12", filters={"jobType": "critique-refine-loop"})

    rows = []
    for run in runs:
        draft_model = run.config.get("draft_model", "unknown")
        refine_model = run.config.get("refine_model", "unknown")
        label = f"{run.name} (draft={draft_model.split('/')[-1]})"
        for record in run.history(pandas=False):
            if "task_id" in record:
                rows.append(
                    {
                        "run": label,
                        "task_id": record["task_id"],
                        "passed": record["passed"],
                        "iterations_used": record["iterations_used"],
                        "last_failure_category": record.get("last_failure_category") or "",
                    }
                )

    mo.md(f"Loaded **{len(rows)}** task-outcome rows across **{len(runs)}** runs.")
    return (rows,)


@app.cell
def _(mo, rows):
    import matplotlib.pyplot as plt
    from collections import defaultdict

    by_run: dict[str, dict[str, int]] = defaultdict(dict)
    for row in rows:
        by_run[row["run"]][row["task_id"]] = row["iterations_used"]

    task_ids = sorted({row["task_id"] for row in rows})
    run_labels = sorted(by_run.keys())

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    bar_width = 0.8 / max(len(run_labels), 1)
    x_positions = range(len(task_ids))
    for i, run_label in enumerate(run_labels):
        values = [by_run[run_label].get(tid, 0) for tid in task_ids]
        offsets = [x + i * bar_width for x in x_positions]
        ax1.bar(offsets, values, width=bar_width, label=run_label)

    ax1.set_xticks([x + bar_width * (len(run_labels) - 1) / 2 for x in x_positions])
    ax1.set_xticklabels(task_ids, rotation=30, ha="right")
    ax1.set_ylabel("Iterations to pass")
    ax1.set_title("Iterations-to-pass per task, by run")
    ax1.legend(fontsize=8)
    fig1.tight_layout()

    mo.md("## Iterations to pass, per task and run")
    fig1
    return


@app.cell
def _(mo, rows):
    import matplotlib.pyplot as plt2
    from collections import Counter

    categories = Counter(
        row["last_failure_category"] for row in rows if row["last_failure_category"]
    )

    fig2, ax2 = plt2.subplots(figsize=(6, 4))
    if categories:
        labels, counts = zip(*sorted(categories.items(), key=lambda kv: -kv[1]))
        ax2.bar(labels, counts, color="#c0392b")
        ax2.set_ylabel("Count")
        ax2.set_title("TypeSafe-diagnosed failure categories (across all runs)")
        plt2.setp(ax2.get_xticklabels(), rotation=20, ha="right")
    else:
        ax2.text(0.5, 0.5, "No failures logged yet", ha="center", va="center")
    fig2.tight_layout()

    mo.md("## Failure categories TypeSafe actually diagnosed")
    fig2
    return


if __name__ == "__main__":
    app.run()
