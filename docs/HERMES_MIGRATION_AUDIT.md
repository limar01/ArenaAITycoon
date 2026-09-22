# HERMES MIGRATION AUDIT — ArenaAITycoon

**Auditor:** Zillion (Studio Director) · **Date:** 2026-09-22 · **Lane:** zillionOM (PC Omarchy)
**Repo:** `limar01/ArenaAITycoon` (public) · **Local checkout:** `~/Projects/workspace/ArenaAITycoon` (PC, cloned 2026-09-22)
**Method:** read-only inspection of git history, repo tree, docs, code, QA rig, bridge worker, deploy scripts, and the PC Hermes runtime (`~/.hermes`). Nothing was modified during the audit.

---

## 1. REPOSITORY FACTS (verified)

| Fact | Value | Evidence |
|---|---|---|
| Git history | **1 commit**: `1a35ee0` "ARENA AI TYCOON v15 — public release" | `git log` |
| Branch | `main` == `origin/main`, clean tree at clone | `git status -sb` |
| Size | 123 MB (dominated by game builds + PNG art) | `du -sh` |
| Game | `builds/arena_ai_simulator/index.html` — 11.7 MB single-file HTML5 canvas game, base64-embedded assets; versioned builds v11–v15 | file tree |
| Personas | 10 (Zillion, Chronos, Marcus, Aria, Cody, Pixel, Echo, Vortex, Jax, Vanguard) — defined in `studio.py`, `zillion_studio_master.py`, README, `memory/MEMORY_CORE.md`, sprite art in `anim_sheets_master/` + `builds/.../assets/` | multiple sources |
| Gates shipped | 16 incremental Boss gates (7–16 documented live in MEMORY_CORE §5j–5s; tools `patch_gate7..15.py`) | MEMORY_CORE, `tools/` |
| QA | Headless rig: `qa/qa_visual.js`, `qa_g10.js`, `qa_g11.js`, `qa_facing.js`, `run_qa_audit.py`, `QA_TEST_SUITE.json`, `E_collision_report.json`, screenshots/shots evidence | `qa/` |
| Bridge | `arenabridge_worker.py` (25.7 KB, stdlib MiniMQTT, broker rotation emqx→hivemq→mosquitto, HMAC envelope, approvals policy, ops exec/note/put_file/get_file/manifest/del/approve) | code |
| Deploy | `tools/patch_gate*.py` sha-verified deploy scripts; `install_arena_tycoon.sh` Termux one-command installer; `builds/` version history | tree |
| Memory | `memory/MEMORY_CORE.md` v2.0 (53 KB) + `memory_core.json`; triple-mirrored in `savepoint/` and `docs/` | tree |
| Orchestrators | `studio.py` (5-agent Ollama pipeline), `zillion_studio_master.py` v5 (9 agents, verticals, per-role model routing, Chronos anchor injection, Vanguard gauntlet), `cli.py` interactive console | code |
| Reports | `reports/GAUNTLET_CLEARANCE_CERTIFICATE.md`, `reports/SUMMARIZED_QA_JUDGE_AUDIT_REPORT.md` (10/10 pass, 2026-08-25) | tree |

## 2. ENVIRONMENT FACTS (verified)

| Fact | Value |
|---|---|
| Hermes runtime (PC) | `~/.hermes` present; `_config_version: 39`; default provider `nous` → `upstage/solar-pro4:free` (base `inference-api.nousresearch.com/v1`); one `custom_providers` entry = a `*.trycloudflare.com` `/v1` endpoint (identity UNKNOWN — not asserted) |
| Hermes profiles (PC) | 15: all 10 studio personas (aria, chronos, cody, echo, jax, marcus, pixel, vanguard, vortex, zillion) + extras (fable, lumen, prima, rivet, scope) |
| Hermes global skills (PC) | 18 groups incl. `github` (7 sub-skills), `python-project-qa`, `software-development`, `creative`, `media`, `autonomous-ai-agents`, `devops` — **reuse, do not duplicate** |
| Hermes features live | kanban w/ `review_dispatch: true`, memory enabled, delegation `max_iterations: 250`, approvals `mode: 'off'`, compression enabled |
| Ollama (phone) | Models verified in MEMORY_CORE §2: `llama3.2:1b`, `qwen2.5:1.5b`, `qwen2.5-coder:1.5b`, `deepseek-r1:1.5b` (port 11434) |
| PC git | identity `Ramil <angelesramil79@gmail.com>`; `ssh -T git@github.com` → **Host key verification failed** (github.com absent from known_hosts) ⇒ PC push currently blocked |
| Phone lane (zillion doctrine) | CF tunnel + worker + adb stack LIVE; deploy keys `github-zr`/`github-ta` verified (zillion-restore / tunnel-adb only — **no key registered for ArenaAITycoon**) |
| Old phone checkout | MEMORY_CORE references `~/projects/hermes_game_studio` on the phone as "THE workspace" (locked decision #8/#9, 2026-08-25) |

## 3. CLASSIFICATION (KEEP / MODIFY / MERGE / REPLACE / DEPRECATE)

### KEEP (working systems — do not break)
| Component | Reason |
|---|---|
| `builds/arena_ai_simulator/` (game + versions v11–v15 + assets) | The product. v15 live. **No gameplay edits until migration plan is Boss-reviewed.** |
| `arenabridge_worker.py` | Live, proven MQTT remote-control channel; HMAC + approvals; matches doctrine worker lineage. |
| `qa/` rig + evidence | Working headless QA with screenshots/reports; basis for JAX QA tier. |
| `tools/patch_gate7..15.py` | Proven sha-verified deploy pattern; historical record of every shipped gate. |
| `install_arena_tycoon.sh` | Working one-command Termux installer (Gate 16 deliverable). |
| `anim_sheets_master/` | Source art for all 10 personas. |
| `reports/` | Gauntlet/QA evidence archive. |
| `memory/MEMORY_CORE.md` + `memory_core.json` | Canonical legacy project brain; every locked decision lives here. |
| Hermes profiles (`~/.hermes/profiles/*`) | Machine-level persona definitions already exist for all 10 roles. |
| Hermes global skills (`github/*`, `python-project-qa`, …) | Provide required capabilities; project skills must **reference**, not copy. |

### MODIFY (keep, but upgrade in place)
| Component | Change |
|---|---|
| `memory/MEMORY_CORE.md` | ADD a header pointer to the new structured `memory/` set; **delete nothing** (Rule: memory = append). |
| `README.md` | Add pointer to `.hermes.md`, `AGENTS.md`, `studio/`, new docs; keep existing content. |
| `studio.py` / `cli.py` | Keep as legacy 5-agent console; label LEGACY; new orchestration lives in `studio/workflows/` + Hermes. |
| `zillion_studio_master.py` | Keep as legacy 9-agent engine; its Chronos-anchor + model-routing ideas are **merged** into the new architecture; mark for retirement after verification. |
| `start_studio.sh` / `pull_all_models.sh` | Repath from `~/projects/hermes_game_studio` to the active checkout; keep behavior. |
| `qa/run_qa_audit.py` | Extend with the evidence schema (procedure/expected/actual/evidence/severity) — additive. |

### MERGE (consolidate duplicates into one source of truth)
| From | Into |
|---|---|
| Persona definitions scattered across `studio.py`, `zillion_studio_master.py`, README §table, MEMORY_CORE §2, sprite art | `studio/agents/*.md` + `memory/AI_PERSONAS.md` (single roster; profiles link to Hermes profiles). |
| 16 ad-hoc gates (MEMORY_CORE §5a–5s) + 6-gate roadmap (AAA_STUDIO_ROADMAP.md) | Gates 0–8 framework in `docs/HERMES_STUDIO_ARCHITECTURE.md` (mapping table below). |
| Save-point/restore protocol (MEMORY_CORE §0b + `savepoint/RESTORE_GUIDE.md`) | `studio/workflows/` restore workflow, merged with the current doctrine restore (zillion-restore kit). |
| `docs/ARENA_AI_TYCOON_MEMORY_CORE.md` ↔ `memory/MEMORY_CORE.md` ↔ `savepoint/MEMORY_CORE.md` (3 identical copies) | Canonical = `memory/MEMORY_CORE.md`; others frozen as archives. |

### REPLACE (superseded by newer Boss orders — evidence cited)
| Old | New | Evidence |
|---|---|---|
| "Taglish reporting to Boss always" (locked #10, 2026-08-25) | English reporting | Doctrine v1.3.9 (2026-09-09, later Boss order). Game *content* flavor may stay Taglish. |
| "Ignore Arch Linux for active work" (locked #8, 2026-08-25) | PC Omarchy is the active dev lane (Hermes installed; zillionOM lane declared 2026-09) | Doctrine v2.3.5; this audit executed on PC. |
| Phone = THE workspace (locked §5f) | PC = development canonical; phone = deploy/QA target tier | Lane declaration v2.3.5 (2026-09-19). |
| Ollama-only 1–1.5B model matrix | Tiered model strategy (STRONG / CODING / FAST) over Hermes providers + Ollama fallback | Mission §28; observed `~/.hermes/config.yaml`. |

### DEPRECATE (freeze; no new writes; keep as archive)
| Component | Reason |
|---|---|
| `savepoint/` mirror | Frozen 2026-08-25 snapshot; superseded by git + doctrine mirrors. Keep, never extend. |
| `workspace_updates_20260825/` | One-off transfer dir. Archive only. |
| Embedded `mqagent.py` in MEMORY_CORE §0b | Offline fallback only; primary bridge = repo `bridge/` + doctrine clients. |

## 4. GATE MAPPING (existing → target 0–8)

| Target | Status | Evidence (existing) |
|---|---|---|
| G0 Repository Audit | **PASS (this document)** | — |
| G1 Game Vision | PASS | Locked decisions §3 (title, branding, cozy life-sim vision) |
| G2 Game Design | PASS (partial docs) | Brainstorming meeting doc; loop/mechanics in MEMORY_CORE §0/§5x; formal GDD file = gap |
| G3 Tech Architecture | PASS (de facto) | Single-file canvas engine + Ollama brains + PWA; formal ARCHITECTURE.md = gap |
| G4 Vertical Slice | PASS | v15: title→office→walk/collision→NPC life→events→LLM tap→zoom→save/load all live (gates 7–15) |
| G5 Alpha | **IN PROGRESS** | Backlog §8: true 4-dir sprite frames, idle cycles, full mobile QA pass, 5 remaining sprite sheets |
| G6 Beta | NOT STARTED | — |
| G7 Release Candidate | NOT STARTED | — |
| G8 Release | NOT STARTED | v15 = public release candidate of the slice; installer exists (G16) |

**CURRENT GATE: G5 (Alpha) — in progress.**

## 5. VERTICAL-SLICE LOOP STATUS (mission §21, adapted)

START ✅ (title) → ENTER ARENA ✅ → GAMEPLAY ✅ (walk/A*/collision/zoom) → AI ACTIVITY ✅ (LLM brains g12, graceful fallback) → PLAYER INTERACTION ✅ (tap→dialogue) → EVENT ✅ (Beer Friday, coffee incident g14) → REWARD/PROGRESSION ⚠️ PARTIAL (stats/upgrades in summary; no formal progression spec) → SAVE ✅ → LOAD ✅.

## 6. MODEL AUDIT (mission §28 — observed, not assumed)

| Tier | Observed provider | Assigned roles |
|---|---|---|
| STRONG | Hermes default `nous/upstage:solar-pro4:free`; Arena chat model (this session) | Zillion, Vanguard, hard architecture/debugging |
| CODING | `qwen2.5-coder:1.5b` (Ollama phone); escalate to STRONG when quality matters | Cody, Vortex |
| FAST | `llama3.2:1b`, `qwen2.5:1.5b` (Ollama phone) | routine docs, memory maintenance, simple specs |
| UNKNOWN | `custom_providers[0]` CF-tunnel `/v1` endpoint — identity unverified; **do not use until identified** | — |

No model name is hardcoded in the new architecture; tiers are capability-based and resolved at runtime (profiles/config own concrete IDs).

## 7. CONFLICTS REQUIRING BOSS DECISION

1. **Canonical project home**: phone `~/projects/hermes_game_studio` (locked 08-25) vs PC `~/Projects/workspace/ArenaAITycoon` (this audit). *Recommendation:* PC = dev canonical; phone = deploy/QA tier; phone copy stays as installer source until re-bundled.
2. **Reporting language**: Taglish (locked #10) vs English (doctrine v1.3.9, later). *Recommendation:* English reports; Taglish preserved as in-game flavor.
3. **Push path for this repo**: no deploy key registered for ArenaAITycoon; PC ssh known_hosts missing github.com. *Recommendation:* Boss approves either (a) PC `known_hosts` + a new PC deploy key, or (b) phone deploy-key registration for this repo. Until then: **local commits only** (this audit's commits are local).
4. **Hermes approvals mode = 'off'** on PC vs doctrine approval gates. Studio-level ops still honor doctrine gates regardless of Hermes config.

## 8. RISK REGISTER

| Risk | Severity | Mitigation |
|---|---|---|
| Migration edits break v15 game | HIGH | Additive-only Phase 4; gameplay files untouched; every change behind Jax+Vanguard |
| Context/token burn re-reading 53 KB core | MED | Structured memory set; read-on-demand; slim-before-paste |
| Duplicate persona definitions drift | MED | Single roster (studio/agents) + AI_PERSONAS.md; legacy files labeled LEGACY |
| PC push blocked | MED | Local commits; decision §7.3 |
| 11.7 MB single-file HTML regression surface | HIGH | Never hand-edit built file; changes via build scripts + sha-verified deploys (existing pattern) |

---
*Audit complete. No gameplay code was modified. Classification stands until Boss review.*
