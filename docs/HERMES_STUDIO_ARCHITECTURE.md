# HERMES STUDIO ARCHITECTURE — ArenaAITycoon (reference implementation)

**Author:** Zillion · **Date:** 2026-09-22 · **Scope:** studio-level (reusable for Game #2…#N) + project-level bindings for ArenaAITycoon.

---

## 1. LAYER SEPARATION (reusability requirement)

**STUDIO LEVEL (game-agnostic, reusable):** agent protocol (`AGENTS.md`), QA methodology (`game-qa` skill, evidence schema), Vanguard independence rule, Chronos memory schema, gates 0–8, workflows, generic skills, model-tier strategy.
**PROJECT LEVEL (ArenaAITycoon-specific):** mechanics, personas-as-characters, economy, assets, locked decisions (MEMORY_CORE §3), `builds/`, gate history, project memory contents.
A new game = new project dir + new `memory/` contents + same studio layer. Bootstrap procedure in §8.

## 2. ORG CHART (runtime)

```
BOSS ─ ZILLION(director, permanent) ─ CHRONOS(memory, permanent)
  ├─ MARCUS(production) ⇄ ARIA(design)          [on-demand]
  │    └─ CODY(code) · PIXEL(art) · ECHO(audio)  [on-demand, parallel-safe iff disjoint files]
  │         └─ VORTEX(engine/graphics)
  ├─ JAX(adversarial QA, on-demand)
  └─ VANGUARD(independent review, permanent role, spawned per review)
Flow: BOSS→ZILLION→CHRONOS(context inject)→planning(MARCUS/ARIA)→specialists→integration(ZILLION)→JAX→VANGUARD→(FAIL≤3→fix loop)→CHRONOS update→ZILLION→BOSS approval→RELEASE
```
Permanent = conceptual roles always in the loop; specialists **spawned only when needed** (no 9-agent standing army).

## 3. CHRONOS MEMORY SCHEMA (`memory/`)

| File | Owns |
|---|---|
| `PROJECT_STATE.md` | confirmed facts, current gate, verified commits |
| `GAME_DESIGN.md` | loop/mechanics/economy/progression pointer → GDD docs |
| `ARCHITECTURE.md` | engine/technical decisions pointer |
| `ART_BIBLE.md` / `AUDIO_BIBLE.md` | visual/audio identity, asset specs |
| `AI_PERSONAS.md` | single roster (studio team), model tiers, Hermes profile links |
| `QA_STATE.md` | last QA run, open findings by severity |
| `DECISIONS.md` | accepted/rejected approaches w/ dates (append-only) |
| `BACKLOG.md` | ticket IDs, owners, deps, acceptance |
| `CURRENT_SPRINT.md` | active sprint (single writer: Chronos) |
| `RELEASE_STATE.md` | build versions, deploy targets, release gate status |
| `MEMORY_CORE.md` | LEGACY canonical brain — append-only, pointer to this set |

Rule: **never store assumptions as facts** — unverified = labeled `UNESTABLISHED`.

## 4. GATES 0–8

Each gate: entry criteria · deliverables · tests · Jax QA · Vanguard review · exit criteria. Boss = final approver (sole).

| Gate | Entry | Exit |
|---|---|---|
| G0 Audit | mission start | audit doc accepted |
| G1 Vision | G0 | vision one-liner + Boss sign-off |
| G2 Design | G1 | GDD accepted |
| G3 Architecture | G2 | ARCHITECTURE.md + risk review |
| G4 Vertical Slice | G3 | full loop playable on target device, QA+Vanguard PASS |
| G5 Alpha | G4 | content complete, backlog criticals=0 |
| G6 Beta | G5 | regression suite green, perf budget met |
| G7 RC | G6 | release checklist + Boss dry-run |
| G8 Release | G7 | Boss final approval, tagged deploy |

ArenaAITycoon now: G0–G4 PASS (evidence: audit §4), **G5 active**.

## 5. PROTOCOLS
- **Task dispatch** = `studio/prompts/task_template.md` (TASK/OBJECTIVE/CONTEXT/RELEVANT FILES/CONSTRAINTS/ACCEPTANCE/TEST REQUIREMENTS/EXPECTED OUTPUT; unique ID `AIT-<n>`).
- **Agent return** = `studio/prompts/report_template.md` (STATUS/TASK/IMPLEMENTATION/FILES_CHANGED/TESTS/TEST_RESULTS/KNOWN_RISKS/FOLLOW_UP/REVIEW_REQUIRED).
- **Jax evidence** = procedure · expected · actual · evidence(path/hash/screenshot) · severity. "It seems to work" = automatic FAIL.
- **Vanguard** = independent session/model; PASS|FAIL; FAIL template per mission §14; ≤3 cycles then STOP+escalate.
- **Failure record** = AGENT/TASK/FAILURE/CAUSE/ATTEMPTED FIX/CURRENT STATE/RECOMMENDATION → then RETRY|REASSIGN|DECOMPOSE|ESCALATE.

## 6. MODEL TIERS (no hardcoded obsolete names)
STRONG (Zillion, Vanguard, hard arch/debug) · CODING (Cody, Vortex) · FAST (routine docs/memory/QA). Concrete IDs live in Hermes profiles/config, resolved at runtime; observed providers recorded in audit §6. Ollama phone models = FAST/CODING fallback tier.

## 7. SKILLS CATALOG
Project `.hermes/skills/`: game-studio (bundle), game-project-manager, game-design, game-programming, game-art-direction, game-audio, game-qa, game-performance, game-balancing, github-workflow, git-safe-workflow, browser-game-testing, release-management.
**Reuse global:** `github/*` (auth/pr/issues), `python-project-qa`, `software-development/*` — project skills reference, never copy.

## 8. NEW-GAME BOOTSTRAP (reusability proof)
1. `git init GameX` + copy studio layer: `AGENTS.md`, `.hermes.md`, `.hermes/skills/`, `studio/`, empty `memory/` set. 2. Run G1–G2 with Boss. 3. Chronos seeds `memory/` from GDD. 4. Same gates/QA/Vanguard. ArenaAITycoon remains reference implementation.
