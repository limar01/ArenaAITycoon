# HERMES MIGRATION PLAN — ArenaAITycoon

**Author:** Zillion (Studio Director) · **Date:** 2026-09-22 · **Companion docs:** `HERMES_MIGRATION_AUDIT.md`, `HERMES_STUDIO_ARCHITECTURE.md`
**HOLD RULE:** No gameplay code modification until this plan is Boss-reviewed. Phases 1–3 are documentation-only and ship with this commit.

---

## PHASE 1 — AUDIT ✅ DONE
Read-only inspection; classification table in `HERMES_MIGRATION_AUDIT.md`.

## PHASE 2 — COMPARE ✅ DONE
Gap analysis (audit §4–§6): existing system already has personas, gates, gauntlet loop, memory core, QA rig, bridge, deploys. Missing: structured Chronos memory set, gates 0–8 criteria, task/report protocol formalization, studio/project separation, project-level skills, independent-Vanguard procedure, PC push path.

## PHASE 3 — SCAFFOLD ✅ DONE (this commit, additive-only)
Created: `.hermes.md`, `AGENTS.md`, `.hermes/skills/*` (13 project skills), `studio/agents/*` (10 role cards), `studio/prompts/*` (task+report templates), `studio/workflows/*` (pipeline, gauntlet, vertical-slice QA, restore), `memory/*` (11 structured files). **Nothing existing was edited or deleted.**

## PHASE 4 — INCREMENTAL MIGRATION (after Boss review; each step = small commit + Jax + Vanguard)

| # | Step | Type | Rollback |
|---|---|---|---|
| 4.1 | Append pointer header to `memory/MEMORY_CORE.md`; label `studio.py`/`zillion_studio_master.py`/`cli.py` docstrings LEGACY | MODIFY (append-only) | revert commit |
| 4.2 | Repath `start_studio.sh`/`pull_all_models.sh` to active checkout; keep old path fallback | MODIFY | revert commit |
| 4.3 | Author formal `GDD` (Aria) from MEMORY_CORE facts → `docs/GDD_ARENA_AI_TYCOON.md` | ADD | delete file |
| 4.4 | Author `ARCHITECTURE.md` game-engine doc (Cody/Vortex) from index.html structure (read-only analysis) | ADD | delete file |
| 4.5 | QA evidence-schema upgrade: `run_qa_audit.py` emits procedure/expected/actual/evidence/severity JSON | MODIFY (additive) | revert commit |
| 4.6 | Gate-5 Alpha tasks as decomposed tickets (IDs, owners, deps, acceptance) in `memory/CURRENT_SPRINT.md` + `BACKLOG.md` | ADD | — |
| 4.7 | Resolve Boss decisions (audit §7): canonical home, language, push path | DECISION | — |
| 4.8 | Register push path per decision; first verified push | OPS (approved) | — |

**Never in Phase 4:** editing `builds/arena_ai_simulator/index.html` by hand; deleting any legacy file; changing locked decisions without Boss vote.

## PHASE 5 — VERIFY NEW ARCHITECTURE
- `studio/workflows/production_pipeline.md` dry-run with a trivial non-gameplay task (e.g., doc generation) through Zillion→Chronos→specialist→Jax→Vanguard→Chronos-update.
- Verify skill resolution: project `.hermes/skills/` + global reuse paths.
- Verify memory writes land in the 11-file set and MEMORY_CORE pointer stays consistent.

## PHASE 6 — FULL QA RUN (Jax)
Run `qa/` rig + new evidence schema against v15 build on phone (Chrome/Termux :8888) and PC headless; produce `qa/reports/<date>_migration_qa.json` with severity-graded findings.

## PHASE 7 — VANGUARD INDEPENDENT REVIEW
Vanguard (separate session/model from implementer) reviews: this plan, Phase-4 diffs, Phase-6 evidence. Verdict PASS/FAIL in `studio/reports/VANGUARD_MIGRATION_REVIEW.md` using the FAIL template (EXPECTED/ACTUAL/EVIDENCE/ROOT CAUSE/REQUIRED FIX/REGRESSION TEST). Max 3 refinement cycles, then STOP + escalate.

## PHASE 8 — CHRONOS MEMORY UPDATE
Checkpoint: `memory/PROJECT_STATE.md` (gate status), `DECISIONS.md` (Boss rulings from §7), `RELEASE_STATE.md`; mirror per doctrine rule 24 (private repo + phone pack + SD).

## PHASE 9 — BOSS REPORT
Section-30 format report (this mission's closing report).

---

## GIT SAFETY (binding)
- Every Phase-4 step: `git status` first; commit only the step's paths; descriptive messages; no force, no reset, no amend of shared commits.
- Uncommitted Boss work found = stop and report, never stash/discard.
- Push only after §7.3 decision; never embed credentials in remotes (doctrine rule 12).

## PARALLELISM
Independent: (Aria GDD) ∥ (QA schema 4.5) ∥ (scripts 4.2). Serialized: anything touching `memory/CURRENT_SPRINT.md` (single writer = Chronos).
