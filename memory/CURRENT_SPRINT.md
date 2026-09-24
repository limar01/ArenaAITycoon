# CURRENT_SPRINT (Chronos sole writer)
Sprint: G5-ALPHA-TICKETS (Phase 4.6 — post-migration gameplay)
Updated: 2026-09-23 (Zillion, Phase 4.6)

## Active tickets (AIT-IDs, owners, deps, acceptance)

### AIT-001: True 4-direction sprite frames for all 10 personas
- **Owner:** Pixel (lead art) + Cody (renderer integration)
- **Deps:** None (can start immediately)
- **Deliverables:** 5 remaining directional spritesheets (Marcus, Echo, Vortex, Vanguard, Chronos) replacing front-only fallback; 3 cols × 4 rows format, 34px target height
- **Acceptance:** All 10 agents render correct directional frames when facing up/down/left/right; no flip/tint hacks; existing save format unchanged
- **Test:** Visual QA on PC headless + phone; screenshot compare
- **Priority:** HIGH (blocks visual polish)

### AIT-002: Complete idle + walk animation cycles
- **Owner:** Cody
- **Deps:** AIT-001 (sprites)
- **Deliverables:** Smooth walk cycle (3 frames), idle breathing/bob variation, no jitter at frame transitions
- **Acceptance:** Agents visibly alive even when not actively walking (amplified idle animation per Gate 15 spec)
- **Test:** Frame-step QA; visual regression
- **Priority:** HIGH
- **Status:** ✅ COMPLETE — Commit 382f59e. Idle breathing amplified 6x (0.5→3.0px) with per-agent phase offsets (breathSeed 0.0-10.9). Walk cycle uses Math.floor() for clean integer frame stepping, 9-frame dwell per pose. NPC parity maintained. docs/AIT-002_ANIMATION_ACCEPTANCE.md.

### AIT-003: Full mobile QA pass with evidence schema
- **Owner:** Jax (adversarial QA) + Zillion (coordinate)
- **Deps:** AIT-001, AIT-002
- **Deliverables:** `qa/reports/<date>_mobile_qa.json` with procedure/expected/actual/evidence/severity for: touch input, collision, save/load, performance, PWA install, audio resume
- **Acceptance:** Zero severity-1 findings; severity-2 documented with timeline
- **Test:** Chrome mobile + Termux :8888; PC headless baseline
- **Priority:** HIGH (blocks G6 Beta)

### AIT-004: Formal economy/progression spec
- **Owner:** Aria (design)
- **Deps:** None (can parallelize with AIT-001/002)
- **Deliverables:** `docs/ECONOMY_PROGRESSION.md` — XP curve, upgrade costs, income rates, win/lose conditions, balance spreadsheet
- **Acceptance:** Mathematically balanced (no trivial infinite cash, no unwinnable state); Boss review
- **Test:** Simulation run (automated balance check)
- **Priority:** MEDIUM

### AIT-005: Deploy verified build to phone + on-device check
- **Owner:** Zillion (ops) + Boss (final approval)
- **Deps:** AIT-003 (QA pass), Phase 4.8 (push path)
- **Deliverables:** Live phone build at :8888 with title screen, walk, collision, events, save/load verified on physical device
- **Acceptance:** Boss confirms on-device functionality
- **Test:** Same as AIT-003 on actual device
- **Priority:** MEDIUM (push path dependency)

### AIT-006: Spatial audio integration
- **Owner:** Echo
- **Deps:** None
- **Deliverables:** Zone-aware audio (volume/fade by distance), event SFX triggers, BGM transitions per time-of-day
- **Acceptance:** Audio context respects mobile resume; no clicks/pops
- **Test:** Headless audio context mock + manual device test
- **Priority:** LOW

## Sprint rules
- One active project in context (this game)
- Single writer for CURRENT_SPRINT.md = Chronos (Zillion edits via patch tool, not hand-edit)
- Evidence over claims — no "done" without test results
