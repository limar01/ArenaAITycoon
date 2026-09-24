# AIT-003: Full Mobile QA Pass — Test Procedure & Evidence Schema
## Author: Zillion (coordinate) · **Date:** 2026-09-23
## For: Jax (adversarial QA execution)
## Status: READY — awaiting phone server online

---

## Execution Prerequisites

1. **Phone server ONLINE** at `http://192.168.1.X:8888` (Termux + `npm run start` or equivalent)
2. **PC baseline running** at `file:///home/limar01/Data/Projects/workspace/ArenaAITycoon/builds/arena_ai_simulator/index.html`
3. **Screenshot capability** on both PC (electron/Chrome devtools) and phone (Termux scrot or screenshot command)
4. **Network info:** Phone IP, both devices on same WiFi
5. **QA evidence output dir:** `qa/reports/<YYYYMMDD>_mobile_qa/`

---

## Test Procedure

### Phase 1: Baseline (PC)

Run on PC first to establish baseline behavior. Record all measurements.

#### P1.1 App Launch
- Open `index.html` in Chrome headless or Firefox
- **Expect:** Title screen renders, no console errors, FPS stable at 60
- **Measure:** Console error count, initial FPS (30s sample), load time (paint to interactive)
- **Evidence:** Screenshot of title screen, console log, FPS counter reading

#### P1.2 Agent Spawn & Idle
- Start game, let agents spawn
- Wait 30s without input
- **Expect:** 10 agents visible, each breathing (idle bob), no freezing, no console errors
- **Measure:** Agent count rendered, idle bob amplitude (px), FPS stability (min/max/avg over 30s)
- **Evidence:** Screenshot with all 10 agents visible, annotated with agent IDs

#### P1.3 Directional Movement
- Click/swipe to send each agent in all 4 directions (up/down/left/right)
- **Expect:** Correct sprite row per direction, smooth walk cycle, facing updates
- **Measure:** Per-agent direction rendering correctness (pass/fail per direction), walk cycle frame rate
- **Evidence:** 4 screenshots per agent (one per direction) OR video capture

#### P1.4 Collision
- Move agents into each other
- **Expect:** Collision avoidance works, agents don't overlap, no physics explosion
- **Measure:** Collision events count, agent position deltas before/after collision
- **Evidence:** Screenshot sequence showing collision resolution

#### P1.5 Save/Load
- Save game state (if UI available) or trigger save via console
- Reload page
- **Expect:** Agents at correct positions, stats preserved, game state restored
- **Measure:** Saved state file size, restore accuracy (position delta < 2px), stat preservation
- **Evidence:** Before-save screenshot, after-load screenshot, state file diff

#### P1.6 Performance Budget
- 60s gameplay session with all agents active
- **Expect:** FPS >= 55 sustained, memory stable (no leak), CPU < 30%
- **Measure:** FPS min/max/avg, heap size start/end, GC count
- **Evidence:** Performance timeline screenshot, memory profile

---

### Phase 2: Mobile (Phone)

Same tests as Phase 1 but on physical device. Additional mobile-specific tests.

#### P2.1 Touch Input
- Tap to select/move agents
- Swipe to pan camera
- Pinch to zoom
- **Expect:** Touch targets responsive (< 100ms latency), no missed taps, pinch zoom smooth
- **Measure:** Tap-to-agent-response latency (ms), pinch zoom range (min/max scale), missed tap count (target: 0)
- **Evidence:** Screen recording of touch interaction, latency measurements

#### P2.2 Mobile Performance
- 60s gameplay on phone
- **Expect:** FPS >= 30 sustained (mobile target), touch responsive, no thermal throttling visible
- **Measure:** FPS min/max/avg, frame time consistency (jitter), touch latency
- **Evidence:** FPS counter readout, frame time graph if available

#### P2.3 Mobile Audio Resume
- Start BGM, lock phone screen, unlock after 10s
- **Expect:** Audio context resumes automatically or on first tap, no clicks/pops
- **Measure:** Audio context state before/after lock, resume success (yes/no), audio glitch count
- **Evidence:** Audio context state log, user report of audio behavior

#### P2.4 Mobile Save/Load
- Save on phone, close tab/app, reopen
- **Expect:** State persists, agents at correct positions
- **Measure:** Same as P1.5
- **Evidence:** Before-save screenshot, after-reopen screenshot, state file diff

#### P2.5 PWA Install (if applicable)
- Check if PWA installable (manifest + service worker)
- **Expect:** Install prompt appears or "Add to Home Screen" available
- **Measure:** Manifest validity, service worker registration status
- **Evidence:** DevTools Application panel screenshot, manifest.json validation

#### P2.6 Orientation
- Test portrait and landscape (if supported)
- **Expect:** Canvas resizes correctly, UI not clipped, agents still interactive
- **Measure:** Canvas dimensions in each orientation, UI element visibility
- **Evidence:** Screenshots in both orientations

---

## Evidence Schema (per test case)

Every test case result must include:

```json
{
  "test_id": "P2.1",
  "name": "Touch input responsiveness",
  "device": "phone-model-or-PC",
  "procedure": "Step-by-step what was done",
  "expected": "What should happen",
  "actual": "What actually happened",
  "evidence": {
    "type": "screenshot|video|log|measurement",
    "path": "qa/reports/<date>_mobile_qa/<file>",
    "description": "Human-readable description of evidence"
  },
  "result": "PASS|FAIL|BLOCKED",
  "severity": 1|2|3,
  "notes": "Optional observations"
}
```

**Severity levels:**
- 1 = Critical (blocks release — crash, data loss, unfixable bug)
- 2 = Major (significant feature broken, workaround exists)
- 3 = Minor (cosmetic, edge case, non-blocking)

---

## Severity-1 Criteria (zero tolerance)

Any of these = FAIL, must fix before G6 Beta:
1. App crash on launch (phone or PC)
2. Data loss on save/load (agents positions lost, stats reset)
3. Touch input completely non-functional (no response to any tap)
4. Audio context permanently broken (never resumes after lock)
5. Console errors that break gameplay (not warnings — actual errors)
6. Agents don't spawn or all render as fallback sprites

---

## Jax Execution Instructions

1. Wait for phone server to be online (Zillion will notify)
2. Run Phase 1 (PC baseline) first — record all evidence
3. Run Phase 2 (mobile) — record all evidence
4. For each test case, fill in the evidence schema JSON
5. Compile all results into `qa/reports/<YYYYMMDD>_mobile_qa.json`
6. If any severity-1 findings: STOP, report to Zillion immediately
7. If severity-2 findings: document with timeline, continue testing
8. Submit final report to Zillion for Chronos state update

---

## Evidence File Naming Convention

```
qa/reports/
  20260924_mobile_qa/          # date-stamped directory
    P1.1_launch_screenshot.png
    P1.1_console_log.txt
    P1.3_zillion_directions.png    # 4-dir collage
    P2.1_touch_recording.mp4
    P2.3_audio_resume_log.txt
    20260924_mobile_qa.json        # compiled results
```

---

## Blockers

- Phone server must be ONLINE before Phase 2 can execute
- Physical phone required for touch tests (emulator insufficient for touch latency)
- Network access to phone from PC required for coordinated testing

---

## Current Blocker Status

| Prerequisite | Status |
|-------------|--------|
| Phone server online | ⏳ BLOCKED — server currently offline |
| PC baseline available | ✅ — index.html runs locally |
| Screenshot capability | ✅ — assumed available on both devices |
| Network connectivity | ⏳ Unknown — verify when server online |

**Next action:** When phone server comes online, Zillion notifies Jax, Jax starts Phase 1 immediately.
