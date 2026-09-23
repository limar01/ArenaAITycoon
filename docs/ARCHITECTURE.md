# 📐 ENGINE ARCHITECTURE — ARENA AI TYCOON
## Formal Architecture Document (Phase 4.4 Deliverable)

**Author:** Zillion (Studio Director) · **Date:** 2026-09-23
**Source of truth:** `builds/arena_ai_simulator/index.html` (v15, 2188 lines, 11.7 MB), `memory/ARCHITECTURE.md`, deploy scripts, QA rig

---

## 1. HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                  SINGLE HTML FILE (v15)                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  <style> — UI chrome, retro header, controls      │  │
│  │  <body> — title screen, modals, dialogue, canvas  │  │
│  │  <script> — game engine (~1600 lines JS)          │  │
│  │    ├── State machine (gameState 0/1/2)             │  │
│  │    ├── Asset loader (base64 PNG sprites)          │  │
│  │    ├── Input handler (touch/mouse/keyboard)       │  │
│  │    ├── Physics & collision (WALL_GRID)            │  │
│  │    ├── A* pathfinding                             │  │
│  │    ├── Agent scheduler (10 personas)              │  │
│  │    ├── Economy & store                            │  │
│  │    ├── Event system (Friday, standup, etc.)       │  │
│  │    ├── Renderer (canvas draw loop)                │  │
│  │    ├── Audio (Web Audio API)                      │  │
│  │    ├── Save/Load (localStorage)                   │  │
│  │    └── UI (dialogue, modals, controls)            │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  External: manifest.json, service worker, icons         │
│  Deploy: tools/patch_gate*.py (sha-verified)            │
│  Bridge: arenabridge_worker.py (MQTT optional)          │
└─────────────────────────────────────────────────────────┘
```

---

## 2. FILE LAYOUT

```
builds/arena_ai_simulator/
├── index.html              ← 11.7 MB, single-file game (NEVER hand-edit)
├── manifest.json           ← PWA manifest
├── sw.js                   ← Service worker (offline cache)
├── icon-192.png            ← PWA icon
├── icon-512.png            ← PWA icon (large)
├── assets/                 ← Generated sprite previews
│   ├── zillion.png
│   ├── cody.png
│   └── ... (10 personas)
└── qa/
    ├── QA_TEST_SUITE.json  ← QA test definitions
    ├── qa_visual.js        ← Visual regression
    ├── qa_g10.js           ← Gate 10 compliance
    ├── qa_g11.js           ← Gate 11 compliance
    ├── qa_facing.js        ← 4-direction walk validation
    ├── run_qa_audit.py     ← Orchestrator
    └── screenshots/         ← Evidence captures
```

---

## 3. CORE SYSTEMS

### 3.1 State Machine
```
gameState:
  0 = TITLE      — Title screen visible, canvas hidden
  1 = PLAYING    — Full simulation running
  2 = PAUSED     — Gate approval pending, time frozen
```

### 3.2 Main Render Loop
- `requestAnimationFrame` at 60fps
- `stepFrame` counter increments each frame (drives animation phases)
- Per-frame: process input → update agents → update physics → render → audio

### 3.3 Input Handler
- **Mouse/touch:** Click-to-interact (agent → dialogue, cabinet → action)
- **Boss movement:** WASD keys or tap-to-move
- **Modal triggers:** Store, Arcade, Settings buttons

### 3.4 Collision System
- **Map:** `WALL_GRID` — 2D array (23 rows × 52 cols), `"#"` = wall, `"."` or `" "` = open
- **Constants:** `GRID_CW` (cell width), `GRID_CH` (cell height), `GRID_COLS`, `GRID_ROWS`
- **Functions:**
  - `gridBlocked(gc, gy)` — check if cell is wall
  - `findPath(sx, sy, tx, ty)` — A* pathfinding, returns path array or null
  - `canMoveTo(x, y)` — pixel-to-grid collision check
- **Dynamic collision:** Boss + NPCs check before applying movement (Gate 15+)

### 3.5 Agent System

Each agent:
```javascript
{
  id, name, role,                    // Identity
  x, y, targetX, targetY,            // Position (pixels)
  speed, isWalking, facing,          // Movement state
  walkFrame,                         // Animation frame (0-2)
  energy, focus, happiness,          // Stats (0-100)
  schedule,                          // Daily routine
  currentAction,                     // What they're doing now
  phrase                             // Current dialogue
}
```

**State machine per agent:**
- `IDLE` → stand at station, occasional shuffle
- `WALK` — Move to target via A* path
- `WORK` — Regenerate focus at desk
- `SOCIAL` — Stand near another agent, chat bubbles
- `EVENT` — Attend standup/party
- `GATE_WAIT` — Strike approval pose (gameState=2)

**Scheduler:**
- Time-of-day driven (08:00–17:00)
- Zones mapped to actions (Dev Core → work, Lounge → social)
- Randomized within schedule for variety

### 3.6 Economy
```javascript
let studioCash = 48500;        // Starting cash
let inGameDay = 43;            // Day counter
let simMinutes = 9 * 60 + 30;  // Sim time (start 09:30)

const storeItems = [
  { id, name, price, bought, desc, icon },
  // 8 items, prices $2500-$10000
];
```

- Cash display updates via DOM (`cashDisplay`, `modalCashDisplay`)
- Save/load persists cash + items + agent stats

### 3.7 Time System
- 24-hour cycle, 1 sim-hour = 2 real-minutes
- `simMinutes` counter, wraps at 1440
- Clock display: `document.getElementById('clock-display')`
- Day counter increments at midnight
- Events triggered by time thresholds

### 3.8 Rendering Pipeline
1. Clear canvas
2. Draw floor/background
3. Draw zone furniture (desks, pool table, arcade cabinet)
4. Draw agents (spritesheet frame selection based on `facing` + `walkFrame`)
   - 4-direction spritesheet: 3 cols × 4 rows
   - Row 0 = down, 1 = up, 2 = left, 3 = right
   - Col 0 = stand, 1-2 = walk frames
   - Fallback: single front sprite (old behavior)
5. Draw Boss avatar (same system, custom sprite)
6. Draw static NPCs (office workers)
7. Draw shadows (ellipse under feet)
8. Draw name tags (monospace, 9px)
9. Draw UI overlays (dialogue bubble if active)

### 3.9 Audio
- Web Audio API
- BGM: Procedural/oscillator-based, time-of-day adaptive
- SFX: Footsteps, blips, cheer, save chime
- Controls: Mute toggle (`bgmBtn`), volume per channel

### 3.10 Save/Load
```javascript
// Save
const state = { cash, day, simMinutes, vertical, storeItems, agentStats };
localStorage.setItem('hermes_studio_save_clean', JSON.stringify(state));

// Load
const state = JSON.parse(localStorage.getItem('hermes_studio_save_clean'));
// Apply to globals
```

---

## 4. DATA FLOW

```
User Input (click/key/touch)
       │
       ▼
 Input Handler → Determine target (agent, zone, UI element)
       │
       ▼
 Action Resolver → What action? (walk, talk, open modal)
       │
       ├──→ Movement: A* path → collision check → apply position
       ├──→ Dialogue: set dialogue state → render comic bubble
       └──→ Modal: show/hide DOM element
              │
              ▼
         State Update (cash, stats, time)
              │
              ▼
         Persistence (localStorage on save)
```

---

## 5. PERFORMANCE CHARACTERISTICS

| Metric | Value |
|--------|-------|
| Canvas size | 1600×900 |
| Target FPS | 60 |
| Agent count | 10 (+ Boss + static NPCs) |
| Render budget | ~2ms per frame (DOM+Canvas) |
| Memory | < 100 MB (base64 assets in RAM) |
| Load time | 1-3s on mobile (cached via SW) |

---

## 6. CONSTRAINTS & INVARIANTS

1. **Never hand-edit `builds/arena_ai_simulator/index.html`** — only via `tools/patch_gate*.py`
2. **Idempotent patches** — every deploy script checks for existing patch markers
3. **Backwards-compatible save** — new fields added with defaults; old saves still load
4. **Mobile-first** — touch input, PWA installable, offline-capable
5. **No network dependency** — zero fetch/XHR after initial load
6. **Single-file** — all assets embedded; no external CDN

---

## 7. BRIDGE SYSTEM (Optional)

`arenabridge_worker.py` — MQTT-based remote control:
- Broker rotation: emqx → hivemq → mosquitto
- HMAC-SHA256 signed envelopes
- Ops: exec, note, put_file, get_file, manifest, del, approve
- Approval policy: Boss-only for destructive ops
- Not required for core gameplay; optional for phone remote control

---

## 8. DEPLOY PIPELINE

```
Developer (Zillion)
       │
       ├──→ Build script (tools/patch_gateN.py)
       │       └── sha256 verify before/after
       │       └── .bak_pre_gN backup
       │       └── Idempotency check
       │
       ├──→ Local test (run_qa_audit.py)
       │       └── Headless Chrome (PC)
       │       └── Mobile Chrome (phone :8888)
       │
       ├──→ Git commit (small, descriptive)
       │
       └──→ Push (once path enabled)
               └── Termux pull → deploy to phone
```

---

## 9. QA INFRASTRUCTURE

| File | Purpose |
|------|---------|
| `qa/qa_visual.js` | Pixel-level regression (screenshot compare) |
| `qa/qa_g10.js` | Gate 10 compliance (events, store) |
| `qa/qa_g11.js` | Gate 11 compliance (save/load, audio) |
| `qa/qa_facing.js` | 4-direction walk animation validation |
| `qa/QA_TEST_SUITE.json` | Test definitions, expected results |
| `qa/run_qa_audit.py` | Orchestrator — runs all tests, emits JSON |
| `qa/screenshots/` | Visual evidence |
| `qa/shots/` | Manual QA captures |

---

## 10. RISKS & MITIGATIONS

| Risk | Severity | Mitigation |
|------|----------|------------|
| 11.7 MB single-file regression surface | HIGH | sha-verified patches only; never hand-edit |
| Save format breakage | MED | Backward-compatible load with defaults |
| Mobile performance degradation | MED | Budget check per frame; sprite count cap |
| Audio context suspended (mobile) | LOW | Resume on first user interaction |
| Canvas flicker on old devices | LOW | requestAnimationFrame, no double-buffer |

---

*End of Architecture Document. Updates go to `memory/ARCHITECTURE.md`.*
