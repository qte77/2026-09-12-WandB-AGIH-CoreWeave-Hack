# CoreWeave Hacks: Agent Loops — 2026-09-12

Working folder for this hackathon. Hacking Sat Sep 12 11:15am → submissions due Sun Sep 13 1:00pm.
Open this folder to resume — it's the entry point, not a duplicate of the other artifacts below.

## Files in this folder

- **`findings.md`** — consolidated research record: event logistics, sponsor-stack verification,
  rejected alternatives + why, SOTA honesty notes, competitive positioning, git/infra state.
- **`handoff.md`** — session-handoff narrative (copy of `../.claude/handoffs/2026-09-12-coreweave-hacks-prep.md`,
  kept there too since that's Claude Code's own handoff convention — this is the working-folder copy).

## Where the live work-in-progress still lives (not copied here — it changes, this folder doesn't)

- **Technical plan (single source of truth for what's built/next):**
  `../RDI-AgentBeats-MAS-GraphJudge/docs/plans/0001-agent-oversight-self-evolution.md`
- **Full hackathon facts, including still-open conflict-resolution rules for the other two Sept 12
  events:** Claude memory `project_hackathon_astra_coreweave_2026-09.md`

## Open items right now

See the plan's own **Remaining-work table** (single source of truth) plus:

1. Fable's de-risking checklist not yet executed: verify real Weave/Sandboxes creds + quota +
   cold-start latency (now B1's done-when in the plan); pre-stage eval tasks; script/exercise a
   Sandboxes-down fallback (now part of C2's done-when); time the 90-second pitch.
2. B2 (new): ask on-site whether "Most Production-Ready" judges the Sunday snapshot or live state
   at Fully Connected — unconfirmed.
3. Optional pre-build read: `../ai-agents-research/docs/non-cc/hermes-agent-analysis.md`.
4. `qte77/qte77#169` still `BLOCKED` on required checks/review (merge conflict itself already
   fixed) — not investigated.

## Target

Primary track: Most Production-Ready (~80/20 over Best Loop Design), of **7 total tracks** — see
`findings.md` for the full list and the 2 near-free side-track adds (ARIA, marimo) worth stacking.
Vehicle: `RDI-AgentBeats-MAS-GraphJudge` — Tier 4 oversight/mid-turn-steering (Astra) + a
critique-refine loop over existing Tier1/Tier2 evaluators, instrumented with W&B Weave + run in
W&B Sandboxes, OpenRouter as fallback provider. Not claimed as a novel loop shape (Self-Refine/
Reflexion lineage) — the defensible claim is interpretable post-hoc graph metrics feeding
prompt/behavior refinement, no training/weights.

## Repo state (2026-09-12)

This folder is now pushed to `origin` (`qte77/2026-09-12-WandB-AGIH-CoreWeave-Hack`) — PR #1 open
with these working notes. `RDI-AgentBeats-MAS-GraphJudge`'s plan 0001 has PR #20 open with the
critique-refine pivot + track/judge-alignment corrections. **Still open: whether this repo stays a
submission wrapper (docs + demo links, code stays in the vehicle repo) or becomes the actual build
location** — ask before assuming either way if resuming this session.
