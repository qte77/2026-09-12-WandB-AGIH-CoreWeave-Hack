# Quick demo script — glance-at-while-presenting version

Full pitch with judge talking points: `docs/PITCH.md`. This is the trimmed live-demo version.

## Before you start — tabs open, in this order

1. https://qte77.github.io/2026-09-12-WandB-AGIH-CoreWeave-Hack/ (the landing page)
2. https://wandb.ai/w77/coreweave-hacks-2026-09-12/r/call/01a0982c-49f4-7869-9860-94a71b10f788 (Weave call tree)
3. https://wandb.ai/w77/coreweave-hacks-2026-09-12/runs/8zvt118e (W&B run)

## Say this (under 60 seconds)

> "Most self-correcting agent loops just re-ask the same model and hope. Ours makes one real
> decision: TypeSafe's Jev model diagnoses *why* a fix failed before anything escalates."

**[Point at tab 1 — the landing page]**

> "This agent fixes real Elixir bugs — not Python, on purpose, since Elixir is rare enough in
> most models' training data that the loop has actual work to do. A cheap 2.6-billion-parameter
> model drafts a fix. We execute it for real. On failure, TypeSafe classifies the failure —
> logic error, off-by-one, syntax error — and *that diagnosis* goes into the refine prompt for
> a stronger model."

**[Switch to tab 2 — the Weave call tree]**

> "Here's the actual trace. `run_task` → `attempt_task` → `classify_failure` → `refine_task` →
> `classify_failure` → `refine_task`. This one task needed two escalations. The draft model
> wrote `math:sqrt(n)` — valid Erlang, invalid Elixir — TypeSafe caught it both times."

**[Click into the nested `openai.chat.completions.create` span if there's time]**

> "This nested span isn't ours — Weave auto-instruments it. We get clean semantics and raw
> provider data for free. This call spent 1897 of 2000 completion tokens just reasoning."

**[Switch to tab 3 — the W&B run, or say the numbers]**

> "9 independently verified Elixir tasks. Cheap model alone: 3 out of 9 correct first try.
> Diagnosis-gated escalation: 9 out of 9, 100%, verified through the W&B API — not the console
> log."

**[Close]**

> "Critique-refine itself isn't new — Self-Refine, Reflexion. What's ours is that the escalation
> trigger is a real diagnosis, not a guess."

## If asked a hard question

- **"Is this a real benchmark?"** — No. 9 hand-authored tasks, each independently verified
  before any LLM spend. Say so plainly.
- **"Did you use CoreWeave compute?"** — No, OpenRouter handles the LLM calls. Say so plainly.
- **"Sandboxes?"** — Investigated for real, working SDK and auth, blocked on org entitlement.
  Local subprocess execution is what actually ran.
- **"Is the loop shape novel?"** — No, Self-Refine/Reflexion lineage. The diagnosis-driven
  escalation trigger is the real contribution.

## Timing

Practiced at ~60-75 seconds core script. If you have the full 90 seconds, add the judge lines
from `docs/PITCH.md` (Emmanuel Turlay on Weave, Xiangyi Li on BenchFlow overlap).
