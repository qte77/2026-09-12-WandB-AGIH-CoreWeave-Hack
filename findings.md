# Findings — CoreWeave Hacks: Agent Loops (2026-09-12)

Consolidated from this session's research. Superseded/updated by the plan's own Status section if
they ever diverge — `../RDI-AgentBeats-MAS-GraphJudge/docs/plans/0001-agent-oversight-self-evolution.md`
is still the live source of truth for what's built/next; this file is the research record.

## Submission rules (relayed by the user from kickoff, 2026-09-12 — supersedes the vehicle choice below)

- **Deadline: Sun Sept 13, 1:00pm PT** — matches event-page logistics, no change.
- **The GitHub project must have been created today, with no prior work carried in.** This
  invalidates `RDI-AgentBeats-MAS-GraphJudge` as the submission vehicle — that repo's Tier1-4
  evaluator code predates 2026-09-12 (commits #3/#5/#16/#19 etc.). **The actual submission must be
  built fresh in this repo** (`2026-09-12-WandB-AGIH-CoreWeave-Hack`, confirmed created today —
  single placeholder commit before today's work started). MAS-GraphJudge's *design ideas*
  (critique-refine loop shape, graph-metric evaluation) can inform the fresh build; its *code and
  repo* cannot be the submission. **Unconfirmed and asked of the user**: whether "GitHub account"
  in the relayed rule means a literally new account, or just a new repo under the existing
  `qte77` account (assumed, pending confirmation) — a new-account requirement would invalidate the
  PRs already opened under `qte77` and needs a different remediation.
- **W&B (wandb.ai) is required for at least traces** — not optional; Weave instrumentation must be
  real, not a stretch goal.
- **Integrate sponsor components early** — wire Weave (and any other sponsor tool used) in from the
  first meaningful piece of code, not bolted on at the end.
- **Use sponsor tools** (plural) — reinforces the earlier "unexpected value" side-track adds
  (Best Use of Weave / ARIA / marimo) as more than optional bonus points.
- **Commit often** — likely because judges/rules can audit commit timestamps to confirm work was
  actually done during the event window, not dumped in one late commit. Build incrementally, commit
  small and frequently from here on.

## Event logistics (verified from the actual event page, 2026-09-11)

- Two-day event: Sat Sept 12 (9am breakfast, 10:30am kickoff, **11:15am hacking starts**, 6:30pm
  dinner, 9pm office closes) → Sun Sept 13 (9am doors, **1:00pm submissions due**, 1:30pm judging,
  3:30pm presentations, 4:30pm awards). ~14 hacking hours.
- Location: CoreWeave Office, 400 Alabama St, SF. Registration confirmed.
- Theme (verbatim, matches MAS-GraphJudge's actual thesis): "observe, evaluate, track, document,
  and self-improve agent iterations."
- **Seven prize tracks** (corrected 2026-09-12 from the live event page — previously this file
  tracked only two): **Best Loop Design** (robot dog ~$4k + $2k cash, awarded 9/13 on-site),
  **Most Production-Ready** (F1 tickets ~$1-2k/ticket + $1k cash, awarded ~2 weeks later at Fully
  Connected, Sept 29-Oct 1 — target track, ~80/20 over Best Loop Design), **Best Use of Weave**
  ($1,000), **Best Use of ARIA** ($1,000), **Best Use of marimo** ($500), **Best Social Media
  demo** ($1,000), **Best Use of TypeSafe AI** (2 HF Microducks + ~$1k swag). **Unconfirmed**:
  whether Most-Production-Ready judges the Sunday snapshot or live repo state at Fully Connected —
  ask on-site (plan's B2).
- Acceptance criterion stated on the page favors hackers with an existing project to point to —
  consistent with using the real `RDI-AgentBeats-MAS-GraphJudge` repo rather than starting fresh.
- **Judges, 10 total (named 2026-09-12; previously 5 were "announced soon")**: AGI House side —
  Jinjing/Jinjing Liang (co-founder/CEO Stably AI, YC W2026, AI-generated self-healing E2E tests —
  direct domain overlap with "catching their own mistakes"), Kshitij Dixit (Co-Founder/CEO Zeo
  Auto/Zeo Route Planner), Shivank Joshi (Partner at The Foundery; "Exploring Capital" per the
  event page is likely "Exploring Minds," a podcast — don't misquote back to them), Venkatarao
  Rebba (ML Engineer at Meta, Gen AI/LLM), Xiangyi Li (Founder @BenchFlow — agent-skill
  benchmarking, SkillsBench/ClawsBench — direct domain overlap with our evaluation framing).
  Sponsor side — Emmanuel Turlay (Director of Engineering, CoreWeave, **leads the Weave team**,
  publicly posts on agent-first observability for multi-turn/tool-call semantics — matches our
  Tier-4 framing closely), Lorenzo Porras (W&B), Julia Rose (ARIA team, W&B), Konstantin Taletskiy
  (marimo), Mo Tiwari (Google; "DeepMind" per the event page unconfirmed independently — don't
  overclaim in the pitch). Xiangyi Li and Jinjing are worth naming deliberately in the pitch.

## Sponsor stack — verified first-party, not from memory

- **W&B Weave**: `@weave.op` decorator, OTel-based cross-process tracing. Real, usable today.
- **W&B Sandboxes**: serverless isolated execution, auto-correlates Weave traces to the run that
  produced them — the concrete answer to "where do critique-refine iterations actually run."
  Launched May 2026.
- **ARIA**: re-verified 2026-09-12 — a chat-in-sidebar agent inside an opened W&B project, **UI-only,
  no API/programmatic invocation**, public preview since June 2026. It reads **classic
  `wandb.log()` Experiment Runs** (training code, logs, loss curves, metrics, artifacts,
  checkpoints) — **not confirmed to ingest Weave traces**. Since "Best Use of ARIA" is now a named
  $1,000 track (not just a demo beat), and the plan's A6b only instruments `@weave.op`, **the plan
  as written likely does not clear this track** — needs a small classic-Run logging add-on (see
  plan's new table row).
- **marimo/molab**: re-verified 2026-09-12, numbers confirmed exactly — free RTX Pro 6000
  Blackwell (96GB VRAM) notebooks, 12hr hard session cap, 90min idle auto-shutdown, default 4
  CPU/32GB RAM. No GPU dependency in our plan (no weight training in scope), so this remains a pure
  optional add-on — now relevant only because "Best Use of marimo" ($500) is a named track.
- **TypeSafe AI** (Bronze sponsor): **correction, 2026-09-12, later same day** — the earlier
  "stealth, no public API" finding is now stale. Their marketing site (typesafe.ai) still reads as
  stealth, but `github.com/typesafe-ai` has public `typesafe-sdk-python` and `typesafe-sdk-js`
  repos (pushed 2026-09-11/12 — literally around this hackathon's start) and a full docs site at
  docs.typesafe.ai. Real product: **"System One"** models (flagship: `jev-latest`) — fast,
  calibrated structured-decision primitives (`Choice`, `Score`, `Noul`) via `POST
  https://api.typesafe.ai/v1/systemone` or the `typesafe-sdk` Python/JS packages (confirmed
  installable: `typesafe-sdk==0.5.7` resolves from PyPI). Not a general chat/completion API —
  narrow, cheap, fast structured judgments, explicitly positioned as an alternative to using an LLM
  for classification/scoring. Has cookbooks for exactly our domain ("Guardrails for LLMs",
  "Classifying RAG passages") and a **drop-in Claude Code agent skill**
  (`claude plugin marketplace add typesafe-ai/skills` + `claude plugin install typesafe@typesafe-ai`).
  **Integrated 2026-09-12** as the critique-refine loop's failure-triage step (`triage.py`,
  `Choice` question classifying each test failure before refine) — a genuinely different signal
  than another LLM call, not a bolt-on. "Best Use of TypeSafe AI" is back in scope.

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

## Unexpected value — cheap side-track adds found 2026-09-12 (don't divert from Most-Production-Ready)

Ranked by payoff/effort, riding on top of plan items already in scope — added as plan table rows
A6d/A8 rather than duplicated here in full:

1. Log a classic `wandb.log()` Run alongside the existing `@weave.op` instrumentation (rides on
   A6b, ~15 min) — makes "Best Use of ARIA" actually winnable (ARIA can only read classic Runs, not
   Weave traces) and doubles as a strong production-readiness demo beat (dogfooding the sponsor's
   own agent on our own agent's data).
2. A ~30-45 min marimo/molab notebook visualizing Tier-1 graph metrics or the Weave trace timeline
   (no GPU needed, so no risk from the 12hr cap) — clears "Best Use of marimo" ($500) using data
   A3/A4 already produce, no new engineering surface.
3. Zero-cost: name-drop Xiangyi Li (BenchFlow) and Jinjing (Stably AI) deliberately in the pitch —
   frame Tier1-4 as the same agent-self-verification problem they've built companies around,
   applied structurally (graph) instead of per-output. Pitch/demo-script change only, folds into C3.
4. Lower priority, skip unless time remains: Best Social Media demo ($1,000) — a short clip of the
   robot dog/humanoid + one line on the loop; owner-gated content task, not agent build time.
5. **Superseded 2026-09-12 (later same day)**: TypeSafe AI turned out to have a real, current API
   (see corrected Sponsor stack entry above) — now integrated as the failure-triage step, so "Best
   Use of TypeSafe AI" is realistically in scope too, not skipped.

## Git/infra state as of 2026-09-12

- `RDI-AgentBeats-MAS-GraphJudge#19` (plan 0001) and `qte77/dotfiles#20` (disk-cleanup repair hook,
  now permanent via `install.sh`) — both merged.
- `qte77/qte77#169`: merge conflict fixed (README union), now `MERGEABLE` but still `BLOCKED` on
  required checks/review — not investigated further.
- `RDI-AgentBeats-MAS-GraphJudge#14` (CVE-affected deps) — open, explicitly out of scope for this
  arc.
