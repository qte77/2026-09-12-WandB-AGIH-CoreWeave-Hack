# Session Handoff — 2026-09-12

**Read this first if resuming CoreWeave Hacks prep.** Hackathon: CoreWeave Hacks: Agent Loops,
CoreWeave Office SF, Sat 11:15am (Sept 12) hacking start → Sun 1:00pm (Sept 13) submissions due.
Registration confirmed. Target track: Most Production-Ready (~80/20 over Best Loop Design).

## What Was Done

- Merged `RDI-AgentBeats-MAS-GraphJudge#19` (plan 0001) and `qte77/dotfiles#20` (disk-cleanup fix,
  permanent — repair hook now wired into `.bashrc` via `install.sh`).
- Fixed `qte77/qte77#169`'s merge conflict (union of two README lines), pushed, now `MERGEABLE`
  but still `BLOCKED` on required checks/review — not investigated further.
- Verified sponsor stack first-party (not from memory): Weave (`@weave.op`, OTel cross-process
  tracing), W&B Sandboxes (isolated exec, auto-correlates Weave traces — the concrete "where
  iterations run" answer), marimo/molab (free GPU, not needed — no weight training in scope), ARIA
  (secondary demo beat only, reads already-logged runs, not core infra), TypeSafe AI (no public
  API found, don't build against it).
- Verified `freellmapi` (25.6k stars) is disqualified — "personal experimentation only" per its
  own README. OpenRouter confirmed instead, backed by the estate's own prior research
  (`ai-agents-research/docs/non-cc/llm-routers-gateways-landscape.md`).
- Ran fresh SOTA research: the critique-refine loop shape (Self-Refine/Reflexion lineage) is NOT
  novel — say so if asked. Graph-structural signal for self-improvement is an active 2026 research
  cluster too (LLM-GNCF, SkillGraph), not untouched. Real, narrow, defensible claim: *interpretable
  post-hoc* NetworkX metrics feeding *prompt/behavior* refinement, not baked into training/weights.

## What's Pending

1. **Not yet applied to plan 0001** (still reads as originally written, A6 = ART-training
   harness): swap A6 to the critique-refine loop (judge→critique→refine→re-run over existing
   Tier1/Tier2), add a Weave+Sandboxes instrumentation task on `GraphEvaluator.evaluate()` /
   `llm_evaluate()` / `Executor.evaluate_all()`, add OpenRouter as fallback provider, drop Phase 3
   explicitly, fix the DGM citation (see below).
2. **DGM citation is wrong in the plan's source map**: linked `arxiv.org/abs/2410.04444`
   ("Gödel Agent") — actual Darwin Gödel Machine paper is `arxiv.org/abs/2505.22954`. Not yet fixed
   anywhere.
3. **Fable's de-risking checklist, not yet done**: verify Weave/Sandboxes creds+quotas+cold-start
   latency for real; pre-stage eval tasks; script a Sandboxes-down fallback (candidate: GH
   Actions + Workers/microVMs, using the estate's existing deep expertise there, e.g.
   `cc-recursive-team-mode`); time the 90-second pitch.
4. Confirm whether "Most Production-Ready" judges the Sunday snapshot or live repo state at Fully
   Connected (2 weeks later) — unconfirmed, ask on-site, changes how hard to lean on the
   two-extra-weeks advantage.
5. Worth a 5-minute read before building: `ai-agents-research/docs/non-cc/hermes-agent-analysis.md`
   (existing self-improving-agent analysis) for validated gotchas.

## Key Decisions (rejected alternatives)

- **Not** reviving `goals.json`-as-agent-loop or deploying `liminal-flux-gh-acc` ("Lim Sid") —
  Fable's explicit verdict: zero pre-event hours on either, both are Phase-3-shaped scope creep on
  unrelated/unbuilt code. One door left ajar: pointing the same loop at `goals.json` as a
  30-minute stretch, mid-event only, after the core demo is recorded.
- **Not** integrating HarnessRouter now — real project, but new dependency with no current
  necessity; one genuine post-hackathon lead found (`cc-recursive-team-mode` fits HarnessRouter's
  own issue #25 on Claude Code subprocess lifecycle).

## Blockers

- None blocking the next step — B1-B4 (owner gates: OpenAI/OpenRouter key+budget, sign-off on
  drift signals, merge approval) haven't come up yet because no code has shipped for this arc.
