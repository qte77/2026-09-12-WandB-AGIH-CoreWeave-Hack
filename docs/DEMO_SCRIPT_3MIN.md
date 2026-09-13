# ~3-minute demo script — full walkthrough with annotations

Shorter version for time-constrained slots: `docs/DEMO_SCRIPT.md` (~60-75s). Full pitch with
judge talking points: `docs/PITCH.md`. This is the expanded, annotated version for a full demo
slot.

## Tabs open before you start, in this exact order (left to right)

1. `https://qte77.github.io/2026-09-12-WandB-AGIH-CoreWeave-Hack/` — landing page
2. `https://wandb.ai/w77/coreweave-hacks-2026-09-12/r/call/01a0982c-49f4-7869-9860-94a71b10f788` — Weave call tree (`fix_is_prime`)
3. `https://wandb.ai/w77/coreweave-hacks-2026-09-12/runs/8zvt118e` — W&B run
4. `https://qte77.github.io/2026-09-12-WandB-AGIH-CoreWeave-Hack/notebook.html` — marimo notebook

---

### 0:00–0:20 — Hook (tab 1, landing page)

**SHOW**: the landing page title + tagline + loop diagram.

**SAY**:
> "Most self-correcting agent loops just re-ask the same model and hope. Ours makes one real
> decision before it retries anything: a purpose-built model diagnoses *why* the fix failed.
> That's the whole pitch — everything else is proof."

### 0:20–0:55 — The mechanism (tab 1, scroll to "The loop")

**SHOW**: point at each step in the loop diagram as you say it.

**SAY**:
> "A cheap draft model — 2.6 billion parameters, free tier — attempts a fix in Elixir. Not
> Python; Elixir bugs are rare enough in training data that this loop has real work to do. We
> *execute* the candidate against real tests — pass or fail is graded by actually running the
> code, never by asking the model if it thinks it worked. On failure, TypeSafe's Jev model
> classifies the failure — logic error, off-by-one, wrong data structure, syntax error — and
> *that specific diagnosis* goes into the prompt for a stronger model to refine. Not 'try
> again' — 'try again, and here's exactly what went wrong.'"

### 0:55–1:45 — Live trace walkthrough (switch to tab 2, Weave call tree)

**SHOW**: the call tree — `run_task` expanded, showing `attempt_task` → `classify_failure` →
`refine_task` → `classify_failure` → `refine_task`.

**SAY**:
> "This is a real trace, not a mockup. `run_task` is the whole attempt for one bug —
> `fix_is_prime`. First call: `attempt_task`, the draft model's try. It failed. Second call:
> `classify_failure` — TypeSafe looked at the actual error output and returned
> `syntax_or_runtime_error`. Third: `refine_task` used that diagnosis to try again. It failed
> *again*, differently — needed a second full escalation cycle before it passed."

**SHOW**: click into the `attempt_task` span, then the nested `openai.chat.completions.create`
span inside it.

**SAY**:
> "This nested call isn't something we wrote — Weave auto-instruments the OpenAI client and
> nests it inside our own explicit trace automatically. So we get clean, readable step names
> *and* raw provider data for free. Look at the token breakdown: this call used 2000 completion
> tokens, and 1897 of them were reasoning tokens. The free model is spending almost its entire
> budget just thinking before it answers — a real cost signal we didn't have to instrument for,
> Weave surfaced it."

### 1:45–2:20 — The numbers, three real runs (switch to tab 3, W&B run — or just say it)

**SAY**:
> "We didn't stop at one run, because one run isn't a claim, it's an anecdote. We ran the full
> 9-task set three times. First-try success genuinely varies — 3 out of 9, then 1 out of 9,
> then 1 out of 9. If we'd only run it once and gotten lucky, that number would be
> meaningless. What's actually stable across all three runs: final pass rate hit 9 out of 9,
> 100%, every single time. And `fix_is_prime` — the one we just walked through — never passed
> on the first try in *any* of the three runs. That's not a fluke case we cherry-picked for the
> demo. It's the consistently hardest task, and the loop consistently closes it."

### 2:20–2:45 — Sponsor tool depth, fast (tab 4, marimo notebook, quick glance)

**SHOW**: the two plots — iterations-to-pass per task, failure-category distribution.

**SAY**:
> "This notebook pulls that same data live from the W&B API — not hardcoded — so these numbers
> update automatically if we run again. Between TypeSafe doing the actual escalation decision,
> Weave tracing every step including nested provider calls, and this pulling live results, the
> sponsor stack isn't decoration here — TypeSafe's call is the mechanism the loop runs on."

### 2:45–3:00 — Honesty + close

**SAY**:
> "Two things we want to say plainly, not bury: critique-refine as a loop shape isn't new —
> it's Self-Refine and Reflexion lineage, and we're not claiming otherwise. What's ours is that
> the escalation trigger is a calibrated diagnosis, not a guess, and we verified that claim with
> three real runs instead of one convenient one. Thanks."

---

## If you're running short, cut in this order

1. Drop the marimo notebook glance (2:20–2:45) entirely — least essential visually.
2. Shorten the trace walkthrough to just the `run_task` children, skip clicking into the nested
   OpenAI span.
3. Never cut the three-run numbers (1:45–2:20) or the honesty line (2:45–3:00) — those are what
   survive judge scrutiny.

## If asked a hard question

- **"Is this a real benchmark?"** — No. 9 hand-authored tasks, each independently verified
  before any LLM spend.
- **"Did you use CoreWeave compute?"** — No, OpenRouter handles the LLM calls. Say so plainly.
- **"Sandboxes?"** — Investigated for real, working SDK and auth, blocked on org entitlement.
  Local subprocess execution is what actually ran.
- **"Is 3 runs enough?"** — It's enough to show the number isn't fixed and the final result is
  stable; it's not a statistically powered study. Say that directly if pushed.
