# Pitch — 90 seconds

**Recording is on you (owner-gated) — this is the script + checklist, not the video.**

## Script (5 beats, ~90s)

1. **Problem** (15s) — "Agents that cycle through reasoning and action, catching their own
   mistakes" is the theme. Most loops just re-ask the same model and hope. We wanted the
   loop to actually *know why* it failed before it tries again.
2. **The loop** (20s) — Draft model attempts a fix → we actually execute it against real
   tests (not another LLM's opinion) → on failure, TypeSafe's `Choice` primitive classifies
   *why* it failed → that diagnosis feeds the refine prompt → a stronger model fixes it →
   re-run. Draft-then-verify-then-escalate, the same shape as TypeSafe's own "SDE cascade."
3. **What's real, not simulated** (20s) — Show the W&B run: execution-graded pass/fail
   (real pytest, not self-reported), full Weave trace of the whole session, and the actual
   TypeSafe classification for the one task that needed it.
4. **The numbers** (20s) — 9 hand-authored bug-fix tasks, each independently verified before
   the run. Cheap draft model alone: 8/9 correct on the first try. The 9th
   (`fix_binary_search`) failed, TypeSafe correctly diagnosed it as a `logic_error`, the
   loop escalated to the stronger model, and it passed. Final: 9/9, 100% real pass rate.
5. **Honesty line** (15s) — Critique-refine is Self-Refine/Reflexion lineage, not a new
   idea — we're not claiming otherwise. What's real here is that a cheap model plus a loop
   that actually diagnoses its own failures gets you most of the way to what a strong model
   does alone, at a fraction of the cost — verified, not assumed.

## Demo checklist — tabs to have open

- **W&B run (the cascade run — use this one, not the single-model runs)**:
  https://wandb.ai/w77/coreweave-hacks-2026-09-12/runs/23dnrd8h
- **One Weave call tree** (the `fix_binary_search` escalation — verified via
  `client.get_call()` to actually be this task, not assumed from print order):
  https://wandb.ai/w77/coreweave-hacks-2026-09-12/r/call/01a09738-a3fa-7b59-9fbd-68933a1efe0f
- **W&B project overview** (for ARIA / Best-Use-of-Weave questions):
  https://wandb.ai/w77/coreweave-hacks-2026-09-12
- **TypeSafe playground** (console.typesafe.ai/playground) — optional, if a judge asks how
  the `Choice` classification actually works.
- **marimo notebook** (`notebooks/loop_viz.py`, run via `uvx marimo run notebooks/loop_viz.py`)
  — two real plots: iterations-to-pass per task/run, and the failure-category distribution.

## Judge-specific talking points

- **Xiangyi Li (Founder, BenchFlow — agent-skill benchmarking)**: frame this as the same
  problem BenchFlow builds around — agent self-verification — solved structurally
  (execute-and-classify) rather than by trusting the model's own claim of success.
- **Jinjing (Co-founder/CEO, Stably AI — AI-generated self-healing E2E tests)**: the loop's
  "catch failures, diagnose why, fix, re-verify" shape is the same lifecycle Stably AI
  automates for test suites — here it's applied to the agent's own code output.

## What NOT to claim

- Not a novel loop shape — say so if asked (Self-Refine/Reflexion lineage).
- Not tested against a public benchmark (HumanEval etc.) — 9 hand-authored tasks, each
  individually verified (buggy version fails, hand-written correct fix passes) before any
  real LLM/API spend. Say this plainly if asked "is this a real benchmark."
- Execution isolation is a local subprocess with a 10s timeout, not W&B Sandboxes. Sandboxes
  was investigated for real (working SDK, working auth) but blocked on org entitlement
  ("sandboxes not enabled for this organization" — see findings.md). If asked, say exactly
  that: the integration is real and one enablement step away, not vaporware, not shipped.
