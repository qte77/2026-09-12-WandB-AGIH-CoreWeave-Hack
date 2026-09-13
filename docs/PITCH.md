# Pitch — 90 seconds

**Recording is on you (owner-gated) — this is the script + checklist, not the video.**

## Script (5 beats, ~90s) — leads with TypeSafe, then Weave, then the numbers

1. **The decision, not the theme** (15s) — Most self-correcting loops just re-ask the same
   model and hope. Ours makes one real decision: **TypeSafe's `Choice` primitive diagnoses
   *why* a fix failed** (`logic_error`, `off_by_one`, `syntax_or_runtime_error`...) before
   anything escalates. That one call is what turns "retry" into a *designed* loop — an
   Escalation Chain gated by a real diagnosis, not a coin flip. This is the loop design.
2. **Why that's Best-Loop-Design AND Most-Production-Ready** (20s) — A cheap 2.6B model
   drafts a fix in **Elixir** (not another generic Python bug — real gotchas: div/rem
   confusion, MapSet's unordered-ness, function-clause shadowing). We *execute* it against
   real tests — no self-grading. On failure, TypeSafe's diagnosis routes straight into the
   refine prompt for a stronger model. Cost scales with genuine difficulty, and the
   escalation trigger is a calibrated classification, not a guess — that's the production
   argument and the design argument, from the same one call.
3. **Show the Weave trace live** (20s) — Open the `fix_is_prime` call tree: `run_task` →
   `attempt_task` → `classify_failure` → `refine_task` → `classify_failure` → `refine_task`.
   Point at the nested, auto-instrumented `openai.chat.completions.create` span *inside* our
   own op — Weave captured both our clean semantics and the raw provider call for free. Then
   point at the real number: that call spent 1897 of 2000 completion tokens on reasoning
   before answering — a genuine cost signal, not a claimed one.
4. **The numbers — 3 repeated runs, not one** (20s) — 9 independently-verified Elixir tasks,
   run 3 times. Draft model's first-try success genuinely varies: 3/9, 1/9, 1/9 (Elixir is rare
   in training data — the loop has real work to do). What's stable across all 3 runs: **final
   pass rate hit 9/9, 100%, every time**, and `fix_is_prime` never passed first try in any run —
   the draft model wrote `math:sqrt(n)` (valid Erlang, invalid Elixir) consistently; TypeSafe
   correctly caught it each time. Verified via the wandb API, not the console log.
5. **Honesty line** (15s) — Critique-refine itself is Self-Refine/Reflexion lineage, not new.
   What's real and ours: the escalation trigger is a purpose-built diagnosis, not another
   LLM's opinion — verified end to end, not assumed.

## Wow factor, one sentence

**You can watch the exact moment a diagnosis — not a guess — decides to escalate, in a live
trace, on a language the cheap model demonstrably doesn't know well.**

## What to cut if time is short

- Drop ARIA and marimo from the spoken pitch entirely — they're real but not in the top 4
  target tracks (Best Loop Design, Most Production-Ready, TypeSafe, Weave). Only mention if
  a judge asks directly.
- Drop the Self-Refine/Reflexion lineage explanation unless asked — say the one-line honesty
  version in beat 5 and move on; don't spend demo seconds on academic lineage.
- Skip the TypeSafe playground tab unless a judge specifically asks how `Choice` works.

## Demo checklist — tabs to have open, in this order

1. **Weave call tree for `fix_is_prime`** (open this FIRST — it's the lead, not a footnote):
   https://wandb.ai/w77/coreweave-hacks-2026-09-12/r/call/01a0982c-49f4-7869-9860-94a71b10f788
2. **W&B run** (the Elixir cascade run):
   https://wandb.ai/w77/coreweave-hacks-2026-09-12/runs/8zvt118e
3. **W&B project overview** (only if asked about Weave/ARIA more broadly):
   https://wandb.ai/w77/coreweave-hacks-2026-09-12

## Judge talking points — lead with these two, in this order

- **Emmanuel Turlay (Director of Engineering, leads the Weave team)**: we deliberately used
  explicit `@weave.op()` wrapping instead of relying only on provider auto-patching, because
  our provider is swappable (OpenRouter) — and it turns out both fire together, giving clean
  semantics *and* raw provider detail (token usage, reasoning-token burn) for free.
- **Xiangyi Li (Founder, BenchFlow — agent-skill benchmarking)**: this is the same problem
  BenchFlow builds around — agent self-verification — solved structurally (execute-and-
  classify) instead of trusting the model's own claim of success.
- (Time permitting) **Jinjing (Co-founder/CEO, Stably AI)**: the "catch failure, diagnose why,
  fix, re-verify" shape is the same lifecycle Stably AI automates for test suites.

## What NOT to claim

- Not a novel loop shape — Self-Refine/Reflexion lineage, say so if asked.
- Not a public benchmark — 9 hand-authored Elixir tasks, each independently verified before
  any real spend.
- Execution isolation is a local subprocess (10s timeout), not W&B Sandboxes — investigated
  for real (working SDK, working auth), blocked on org entitlement. Say exactly that if asked.
- CoreWeave compute itself isn't used — OpenRouter handles the LLM calls. Say so plainly if
  asked; don't imply otherwise.
