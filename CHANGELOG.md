# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/). This is a one-shot hackathon
submission with a single tagged release.

## [1.0.0] - 2026-09-13

### Added

- Critique-refine agent loop that fixes real bugs in **Elixir** code: a cheap draft model
  attempts a fix, the fix is graded by actually executing it (never self-reported), and on
  failure a stronger model refines using a diagnosed failure category.
- **TypeSafe AI** integration (`src/critique_loop/triage.py`) — System One's `Choice`
  primitive classifies each test failure (`logic_error`, `off_by_one`, `wrong_data_structure`,
  `syntax_or_runtime_error`, `other`) before the refine step, gating escalation on a real
  diagnosis instead of a blind retry.
- **W&B Weave** tracing — explicit `@weave.op()` on every LLM/TypeSafe call (so the trace stays
  complete regardless of provider), plus a classic W&B Run logging per-task/iteration metrics
  and model config.
- Draft-then-verify-then-escalate model cascade — an optional cheap draft model for the first
  attempt, falling back to the main model if unset, so the loop's escalation logic and TypeSafe
  triage actually fire in a demo instead of a single strong model solving everything outright.
- **OpenRouter** as the provider-agnostic LLM layer (any OpenAI-compatible model/endpoint via a
  `base_url`/`model` config swap).
- 9 hand-authored Elixir bug-fixing tasks (`src/critique_loop/tasks.py`), each independently
  verified (buggy starter fails its test, a hand-written correct fix passes) via real `elixir`
  execution before any LLM/API spend.
- `notebooks/loop_viz.py` — a marimo notebook pulling per-task results live from the W&B API
  (iterations-to-pass per task/run, TypeSafe failure-category distribution), plus a static
  export (`docs/notebook.html`) for GitHub Pages.
- GitHub Pages landing page (`docs/index.html`) — loop diagram, real result stats, sponsor-tool
  usage table, track justifications, and an honesty section, with live links to the GitHub repo,
  a Weave call tree, the W&B run, and the notebook.
- `findings.md` — consolidated research record (sponsor-tool verification, submission rules,
  rejected alternatives, every real run's results, the Sandboxes investigation).
- `docs/PITCH.md`, `docs/DEMO_SCRIPT.md`, `docs/DEMO_SCRIPT_3MIN.md` — pitch script and
  live-demo scripts (short and full-length) with judge-specific talking points.

### Changed

- Task set switched from generic Python bugs (is_prime, binary search, etc.) to genuine Elixir
  idioms/gotchas (`div/2` vs `rem/2` confusion, `MapSet`'s unordered-ness vs `Enum.uniq/1`'s
  order-preservation, function-clause ordering, `List.flatten/1`'s full recursion vs a
  one-level flatten) — the Python harness itself was kept unchanged, since Weave/wandb/TypeSafe
  all operate on text, not source language.
- Reported numbers changed from a single run to **3 repeated runs**, after a simulated
  eval-focused judge persona (via `agentic-grounded-persona-eval`, modeled on real sourced
  research) correctly flagged that single-run statistics aren't meaningful on their own.
  First-try success genuinely varies (3/9, 1/9, 1/9 across the 3 runs); final pass rate reached
  9/9 (100%) in all 3.
- `README.md` rewritten from a pre-build working-folder stub into the actual submission's front
  door: what it is, how to run it, real numbers, and honesty caveats up front.
- `docs/PITCH.md` reordered to lead with the TypeSafe diagnosis decision and the Weave trace,
  matching the actual track priority (Best Loop Design, Most Production-Ready, TypeSafe, Weave)
  instead of burying the mechanism in "the numbers."
- GitHub Pages deployment switched from an Actions-based workflow to legacy branch serving
  (`main:/docs`), since the site is fully static and needs no build step.

### Fixed

- LLM output was silently wrapped in markdown code fences despite prompt instructions, causing
  every early task attempt to fail on a `SyntaxError` rather than a real logic issue — this made
  the original iteration-count data meaningless and was fixed with defensive fence-stripping.
- An Elixir range-semantics bug in the `is_prime` task's reference implementation: `2..(n-1)` is
  not empty at `n=2` in Elixir (unlike Python's `range(2, n)`), which broke that edge case in a
  first draft of the "correct" fix — caught by verifying every task via real execution before
  any LLM spend, not by reasoning about the semantics from memory.
- Two data-shape bugs in `notebooks/loop_viz.py`: a `None` (not merely absent) config value on
  some older runs broke a sort, and a stray W&B history row from the final summary log (with
  `task_id` present as a key but `null`) slipped through a row filter into the plotted data.
- GitHub Pages deployment failure (`startup_failure`) caused by the repository's default
  read-only Actions permissions blocking the `id-token: write` an OIDC-based deploy needed —
  resolved by switching to legacy branch-based serving, which needs no Actions run at all.

### Removed

- `handoff.md` — verified (via a subagent cross-check) to be fully superseded by `findings.md`,
  which restates every fact/decision with corrections applied where `handoff.md` had gone
  stale.
- The `cwsandbox` dependency, added temporarily to investigate W&B Serverless Sandboxes and
  removed again once the investigation confirmed it isn't usable yet for this account.

### Investigated, not shipped

- **W&B Serverless Sandboxes** — the real Python SDK (`cwsandbox`) and authentication (via
  `WANDB_API_KEY`) both work, but the account's organization returns
  `PERMISSION_DENIED: sandboxes not enabled for this organization`. Local subprocess execution
  (with a 10-second timeout) is what actually runs the candidate code today.
