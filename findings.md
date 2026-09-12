# Findings — CoreWeave Hacks: Agent Loops (2026-09-12)

Consolidated from this session's research. Superseded/updated by the plan's own Status section if
they ever diverge — `../RDI-AgentBeats-MAS-GraphJudge/docs/plans/0001-agent-oversight-self-evolution.md`
is still the live source of truth for what's built/next; this file is the research record.

## Event logistics (verified from the actual event page, 2026-09-11)

- Two-day event: Sat Sept 12 (9am breakfast, 10:30am kickoff, **11:15am hacking starts**, 6:30pm
  dinner, 9pm office closes) → Sun Sept 13 (9am doors, **1:00pm submissions due**, 1:30pm judging,
  3:30pm presentations, 4:30pm awards). ~14 hacking hours.
- Location: CoreWeave Office, 400 Alabama St, SF. Registration confirmed.
- Theme (verbatim, matches MAS-GraphJudge's actual thesis): "observe, evaluate, track, document,
  and self-improve agent iterations."
- Two prize tracks: **Best Loop Design** (awarded 9/13 on-site) and **Most Production-Ready**
  (awarded ~2 weeks later at Fully Connected, Sept 29-Oct 1) — target track, ~80/20 over Best Loop
  Design. **Unconfirmed**: whether that track judges the Sunday snapshot or live repo state at
  Fully Connected — ask on-site (plan's B2).
- Acceptance criterion stated on the page favors hackers with an existing project to point to —
  consistent with using the real `RDI-AgentBeats-MAS-GraphJudge` repo rather than starting fresh.

## Sponsor stack — verified first-party, not from memory

- **W&B Weave**: `@weave.op` decorator, OTel-based cross-process tracing. Real, usable today.
- **W&B Sandboxes**: serverless isolated execution, auto-correlates Weave traces to the run that
  produced them — the concrete answer to "where do critique-refine iterations actually run."
  Launched May 2026.
- **ARIA**: CoreWeave's own coding agent; it *analyzes already-logged W&B run data*, it is not
  integrable infrastructure for this build — secondary demo-mention beat only, not core plumbing.
- **marimo/molab**: free RTX Pro 6000 Blackwell GPU notebooks, 12hr session cap. Not needed — the
  critique-refine loop design has no weight training in scope, so no GPU dependency.
- **TypeSafe AI** (Bronze sponsor): no public API found. Don't build against it.

## What got rejected, and why (don't re-litigate without new information)

- **`freellmapi`** (github.com/tashfeenahmed/freellmapi, 25.6k stars): disqualified by its own
  README — "personal experimentation only." **OpenRouter** used instead, consistent with the
  estate's own prior research (`ai-agents-research/docs/non-cc/llm-routers-gateways-landscape.md`).
- **Reviving `goals.json` as the agent loop** (`qte77/qte77`): read directly — `goals.json` is
  literally `{"goals": []}`, and `docs/goals.md` confirms it's a human-authored goal→Issue→PR→CI
  rollup, not a reasoning-act-observe loop. Doesn't fit the theme even if populated. Fable's
  explicit verdict: zero pre-event hours here — Phase-3-shaped scope creep on unrelated code. One
  door left ajar: pointing the same critique-refine loop at `goals.json` as a 30-minute stretch,
  mid-event only, after the core demo is recorded.
- **Deploying `liminal-flux-gh-acc` ("Lim Sid")**: read directly — documentation-only, "Phase 0
  ready to deploy; no running infrastructure yet," its own AGENTS.md says "do not add runtime
  code." Not viable to pivot to on hackathon day.
- **HarnessRouter integration**: real project, but a new dependency with no current necessity for
  this arc. One genuine post-hackathon lead found: `cc-recursive-team-mode` fits HarnessRouter's
  own issue #25 (Claude Code subprocess lifecycle) — worth filing later, not now.

## SOTA research — honest, not assumed (say so if judges ask)

- The critique-refine loop shape (judge → critique → refine → re-run) is **not novel**: it's the
  Self-Refine (2023) → Reflexion (2023) → CRITIC (2024) lineage, still active in 2026
  (ReflexiCoder, ReasoningBank/ACE).
- Graph-structural signal for self-improvement is **also an active 2026 research cluster**, not
  untouched: LLM-GNCF, TPGO ("Learning to Evolve"), SkillGraph, Coordination Graphs in MARL.
- **The real, narrow, defensible claim**: *interpretable, post-hoc* NetworkX graph metrics (Tier 1)
  feeding *prompt/behavior* refinement (the critique-refine loop) — not baked into training or
  model weights. Don't claim the idea is unique; claim this specific combination
  (interpretable + post-hoc + no-training) is the differentiator.
- **DGM citation was wrong**, inherited unverified from `MAS-GraphJudge`'s own README:
  `arxiv.org/abs/2410.04444` is "Gödel Agent" (Yin et al.), not the Darwin Gödel Machine. Actual
  DGM paper: `arxiv.org/abs/2505.22954` (Zhang, Hu, Lu, Lange, Clune). **Fixed in plan 0001** as of
  2026-09-12 — Phase 3/DGM is now explicitly out of scope for this arc, not just cited correctly.
- Worth a 5-minute read before building further: `../ai-agents-research/docs/non-cc/hermes-agent-analysis.md`
  (existing self-improving-agent analysis, validated gotchas) — not yet read this session.

## Competitive positioning correction (from a live reviewer Q&A, Astra hackathon context)

"We correct mid-execution, observability tools only flag" does **not** hold against Arize's
guardrails, which already do real-time block/regenerate on a live evaluator score. The narrower,
still-standing differentiation: MAS-GraphJudge judges the *structure of a whole multi-step task*
(a graph over the tool-call sequence) rather than a single output/message, and corrects the *same
in-progress task* via a steering primitive rather than discarding and regenerating one output.

## Git/infra state as of 2026-09-12

- `RDI-AgentBeats-MAS-GraphJudge#19` (plan 0001) and `qte77/dotfiles#20` (disk-cleanup repair hook,
  now permanent via `install.sh`) — both merged.
- `qte77/qte77#169`: merge conflict fixed (README union), now `MERGEABLE` but still `BLOCKED` on
  required checks/review — not investigated further.
- `RDI-AgentBeats-MAS-GraphJudge#14` (CVE-affected deps) — open, explicitly out of scope for this
  arc.
