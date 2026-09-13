# CoreWeave Hacks: Agent Loops — Critique-Refine Loop with TypeSafe Triage

Hackathon submission for **CoreWeave Hacks: Agent Loops** (2026-09-12/13, AGI House). Built
entirely in this repo, created 2026-09-12, per the event's no-prior-work rule.

## What this is

A small, real critique-refine agent loop fixing **Elixir** bugs: a cheap draft model attempts a
fix, the fix is graded by **actually executing it against real tests** (not another LLM's
opinion of itself), and on failure **TypeSafe's `Choice` primitive diagnoses why** before a
stronger model refines it. Instrumented end-to-end with **W&B Weave** traces and a classic
**W&B run**, with **OpenRouter** as the provider-agnostic LLM layer (any OpenAI-compatible
model/endpoint works).

Elixir, not Python, on purpose — each bug is a genuine Elixir idiom/gotcha (div/2 vs rem/2
confusion, `MapSet`'s unordered-ness vs `Enum.uniq/1`'s order-preservation, function-clause
ordering, `List.flatten/1`'s full recursion vs a one-level flatten), not a generic
LeetCode-style task ported to a new syntax.

Not claimed as a novel loop shape — critique-refine is Self-Refine/Reflexion lineage. The real
claim is narrower: a draft-then-verify-then-escalate cascade where the escalation trigger is a
genuine execution failure, diagnosed by a purpose-built classifier, not guessed.

## Quickstart

```bash
sudo apt-get install -y elixir   # runtime for the bug-fixing tasks themselves
uv sync
cp .env.example .env   # fill in WANDB_API_KEY, OPENROUTER_API_KEY, OPENROUTER_MODEL, TYPESAFE_API_KEY
uv run python -m critique_loop.main
```

`OPENROUTER_DRAFT_MODEL` is optional — set it to a small/cheap model to see the loop and
TypeSafe triage actually fire; without it, the same strong model drafts and refines.

## Results — real, not simulated

9 hand-authored Elixir bug-fix tasks (not a public benchmark — see Honesty below), each
independently verified (buggy version fails its test, a hand-written correct fix passes) via
actual `elixir` execution before any real LLM/API spend.

- **Cascade run** (cheap 2.6B draft model + strong refine model): **3/9 correct on the first
  try, 5/9 needed one escalation, 1/9 (`fix_is_prime`) needed two** — TypeSafe correctly
  diagnosed each failure (`syntax_or_runtime_error`, `logic_error`, `other`). Spot-checked the
  richest case directly: the draft model wrote `math:sqrt(n)` (valid Erlang, invalid Elixir — a
  genuine small-model mistake, not a harness bug). **Final: 9/9, 100% pass rate.**
- Live data: https://wandb.ai/w77/coreweave-hacks-2026-09-12
- Full methodology, every run's numbers, and what didn't work: `findings.md`

## Visualize

```bash
uvx marimo run notebooks/loop_viz.py
```

Pulls real per-task results live from the W&B API — iterations-to-pass per task/run, and the
distribution of TypeSafe-diagnosed failure categories.

## Docs

- **`findings.md`** — research record, verified sponsor-tool facts (W&B, TypeSafe AI, marimo),
  every real run's results, the Sandboxes investigation, submission rules.
- **`docs/PITCH.md`** — 90-second pitch script, demo checklist with live URLs, judge-specific
  talking points.
- **`handoff.md`** — session history (historical record, superseded by findings.md for current
  facts).

## Honesty

- Critique-refine loop: Self-Refine/Reflexion lineage, not novel.
- Task set: 9 hand-authored coding bugs, not a public benchmark like HumanEval — say so if
  asked.
- Execution isolation: a local subprocess with a 10s timeout, not W&B Sandboxes. Sandboxes was
  investigated for real (working SDK, working auth) but blocked on org entitlement — see
  findings.md.

## Target track

Most Production-Ready (~80/20 over Best Loop Design), among 7 total tracks (Best Use of Weave,
ARIA, marimo also realistically in scope) — see `findings.md` for the full breakdown.
