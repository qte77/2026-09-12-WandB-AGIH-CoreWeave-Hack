# Pitch — 90 seconds

**Recording is on you (owner-gated) — this is the script + checklist, not the video.**

## Script (5 beats, ~90s)

1. **Problem** (15s) — "Agents that cycle through reasoning and action, catching their own
   mistakes" is the theme. Most loops just re-ask the same model and hope. We wanted the
   loop to actually *know why* it failed before it tries again — and we wanted a demo that
   wasn't just another LeetCode-Python-bug fixer, so the agent fixes **Elixir** bugs.
2. **The loop** (20s) — Draft model attempts a fix → we actually execute it against real
   tests (not another LLM's opinion) → on failure, TypeSafe's `Choice` primitive classifies
   *why* it failed → that diagnosis feeds the refine prompt → a stronger model fixes it →
   re-run. Draft-then-verify-then-escalate, the same shape as TypeSafe's own "SDE cascade."
3. **What's real, not simulated** (20s) — Show the W&B run: execution-graded pass/fail (real
   `elixir` execution, not self-reported), full Weave trace of the whole session, and the
   actual TypeSafe classification for `fix_is_prime` — the case that needed two escalations.
4. **The numbers** (20s) — 9 hand-authored Elixir bugs (div/rem confusion, MapSet vs
   Enum.uniq ordering, function-clause-order shadowing, etc.), each independently verified
   before the run. Cheap 2.6B draft model alone: only 3/9 correct on the first try — Elixir
   is a much rarer training language than Python, so the loop actually has real work to do.
   5/9 needed one escalation, 1/9 (`fix_is_prime`) needed two — the draft model wrote
   `math:sqrt(n)`, valid Erlang, invalid Elixir. TypeSafe correctly diagnosed it. Final: 9/9,
   100% real pass rate.
5. **Honesty line** (15s) — Critique-refine is Self-Refine/Reflexion lineage, not a new
   idea — we're not claiming otherwise. What's real here is that a cheap model plus a loop
   that actually diagnoses its own failures closes a real capability gap (a language it
   barely knows) instead of just hoping a re-ask works — verified, not assumed.

## Demo checklist — tabs to have open

- **W&B run (the Elixir cascade run — use this one)**:
  https://wandb.ai/w77/coreweave-hacks-2026-09-12/runs/8zvt118e
- **One Weave call tree** (the `fix_is_prime` double-escalation — verified via
  `client.get_call()` to actually be this task, not assumed from print order):
  https://wandb.ai/w77/coreweave-hacks-2026-09-12/r/call/01a0982c-49f4-7869-9860-94a71b10f788
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
