# 📋 GAME DESIGN DOCUMENT — ARENA AI TYCOON
## Formal GDD (Phase 4.3 Deliverable)

**Author:** Zillion (Studio Director) · **Date:** 2026-09-23 · **Status:** Draft
**Source of truth:** `memory/MEMORY_CORE.md` locked decisions, `memory/GAME_DESIGN.md`, `arena_ai_simulator_GDD_G2.md`, live v15 build

---

## 1. GAME OVERVIEW

**Title:** ARENA AI TYCOON
**Subtitle:** Studio Life Simulator
**Genre:** Cozy top-down pixel-art AI-studio life sim / tycoon
**Platform:** Mobile-first PWA (single-file HTML5 canvas), served via Termux Python http.server on phone; PC mirror supported
**Target audience:** Boss (primary), indie game enthusiasts

### One-line pitch
> 10 AI personas autonomously live, work, and party in a 24-hour studio world you manage — coded by the team itself.

### Pillars
1. **Autonomous AI life** — 10 personas work, socialize, play, and report without micromanagement
2. **Cozy progression** — Earn studio cash, upgrade decor, boost stats, unlock events
3. **Boss-as-god** — You approve gates, spawn events, walk the floor as yourself
4. **Evidence over promises** — Every feature ships with QA, Vanguard review, and runtime proof

---

## 2. CORE LOOP

```
START (title screen)
  ↓
ENTER ARENA (office floor)
  ↓
AI ACTIVITY (10 personas follow daily schedule)
  ↓
PLAYER INTERACTION (tap agent → dialogue; walk Boss avatar)
  ↓
EVENT (Beer Friday, coffee incident, standup)
  ↓
REWARD (cash, stat boost, item unlock)
  ↓
PROGRESSION (buy upgrades, advance gate)
  ↓
SAVE → LOAD
```

---

## 3. WORLD DESIGN

### Campus layout
- **Resolution:** 1600×900 canvas, zoom 1.4×
- **Zones (10):**
  - 🏛️ Exec HQ — Management, approvals
  - 💻 Dev Core — Coding stations
  - 📊 War Room — Standups, planning
  - 🎱 Lounge — Social, billiards
  - 🕹️ Arcade — Minigame cabinet
  - 🏋️ Gym — Stat training
  - ☕ Pantry — Coffee, lunch, energy restore
  - 🍖 Beer Patio — Friday parties
  - 🛋️ Reception / Entry — Title screen spawn
  - 🚪 Elevator — Day start/end trigger

### Time system
- **Ratio:** 1 sim-hour = 2 real minutes
- **Day:** 08:00–17:00 work cycle; off-hours = idle/animal behaviors
- **Auto-pause:** Gates freeze sim until Boss approval

### Economy
- **Currency:** Studio Cash (starting $48,500)
- **Earn:** Arcade minigames, event rewards, passive income from upgraded items
- **Spend:** Decor upgrades (RGB desks, neon, espresso bar, quantum server, etc.)

---

## 4. PERSONAS (10 agents)

| ID | Name | Role | Primary Zone | Color |
|----|------|------|-------------|-------|
| zillion | Zillion | Tech Director | Exec HQ | Gold |
| chronos | Chronos | Memory Keeper | War Room | Silver |
| marcus | Marcus | Producer | War Room | Blue |
| aria | Aria | Designer | Dev Core | Purple |
| cody | Cody | Lead Coder | Dev Core | Cyan |
| pixel | Pixel | Art Director | Dev Core | Pink |
| echo | Echo | Audio Director | Lounge | Green |
| vortex | Vortex | Engine/Graphics | Dev Core | Orange |
| jax | Jax | QA Adversarial | War Room | Red |
| vanguard | Vanguard | Quality Gate | Reception | White |

### AI behavior model
- **Scheduled movement:** A* pathfinding between zone waypoints
- **Idle states:** Desk work, social chat, arcade play
- **Event reactions:** Standup attendance, party mode, gate approval pose
- **Dialogue:** Comic bubbles with typewriter animation + portrait
- **Stats (per agent):** Energy ⚡, Focus 🎯, Happiness 💖 (drain/regen over 24h cycle)

---

## 5. MECHANICS

### 5.1 Movement & collision
- 4-directional walk cycle (down/up/left/right), 3 frames per direction
- Spritesheet: 3 cols × 4 rows, target height 34px, grounded feet anchor
- Collision map: walls, furniture, zone boundaries
- Boss avatar: WASD/tap-to-move, same walk cycle, custom sprite

### 5.2 Interaction
- **Tap agent** → comic dialogue box with portrait + 3 stat bars
- **Tap furniture** → context action (desk: work, espresso: +focus)
- **Store modal** → buy/sell decor items (8 items, prices $2.5K–$10K)

### 5.3 Events
| Event | Trigger | Reward |
|-------|---------|--------|
| Beer Friday | Friday 16:00 | +Happiness all, cash from BBQ sales |
| Coffee Incident | Random pantry visit | +Focus, +cash |
| Daily Standup | 09:00 weekday | Progress unlock |
| Boss Spawn | Manual toggle | +cheer SFX, walk freedom |
| Arcade Session | Tap cabinet | Cash via minigame score |

### 5.4 Arcade minigame
- Retro 8-bit side-scroller shooter
- Controls: LEFT/RIGHT + SHOOT
- Rewards: Studio Cash + Happiness boost

### 5.5 Store / Upgrades (8 items)
| Item | Price | Effect |
|------|-------|--------|
| RGB Gaming Desks | $5,000 | +20% Coder focus regen |
| 4K Curved Displays | $8,000 | +compile speed, -strain |
| Studio Neon Art | $3,000 | +Happiness Beer Friday |
| Luxury Leather Sofa | $6,000 | +30% happiness lounge |
| Italian Espresso Bar | $4,500 | +25% max focus |
| Beer Patio BBQ Grill | $7,500 | +all stats at parties |
| Quantum Server Coolers | $10,000 | Zero shader compile delay |
| Golden Rubber Duck Mascot | $2,500 | +100% Jax QA luck |

---

## 6. AUDIO

- **BGM:** Time-of-day adaptive (morning calm, day upbeat, evening lounge)
- **SFX:** Footsteps, blips (UI), cheer (events), save chime, arcade sounds
- **Engine:** Web Audio API, spatialized per zone
- **Controls:** Mute toggle, volume per channel

---

## 7. SAVE/LOAD

- **Storage:** localStorage key `hermes_studio_save_clean`
- **Saved state:** cash, day, simMinutes, activeVertical, storeItems[], agentStats[]
- **Export:** Optional download as JSON backup

---

## 8. TECH STACK

| Layer | Technology |
|-------|-----------|
| Rendering | HTML5 Canvas 2D |
| Assets | Base64-embedded PNG sprites (no external fetches) |
| PWA | manifest.json, service worker, apple-touch-icon |
| Audio | Web Audio API (oscillator + sample playback) |
| State | In-memory globals + localStorage persistence |
| Server | Python http.server (Termux) :8888 |
| Bridge | MQTT via paho-mqtt (optional, arenabridge_worker.py) |

---

## 9. PRODUCTION GATES (current)

| Gate | Status | Evidence |
|------|--------|----------|
| G0 Audit | PASS | docs/HERMES_MIGRATION_AUDIT.md |
| G1 Vision | PASS | Locked decisions MEMORY_CORE §3 |
| G2 Design | PASS | This GDD + G2 doc |
| G3 Architecture | PASS | De facto single-file canvas + Ollama |
| G4 Vertical Slice | PASS | v15: walk/collision/events/save all live |
| **G5 Alpha** | **IN PROGRESS** | Gym, arcade, Beer Friday, 8 store items live |
| G6 Beta | NOT STARTED | — |
| G7 RC | NOT STARTED | — |
| G8 Release | NOT STARTED | — |

---

## 10. KNOWN GAPS (backlog)

- Formal economy/progression spec (no spreadsheet balancing)
- Full mobile QA pass (Chrome/Termux touch behavior)
- True 4-dir sprite frames for all 10 personas (some still front-only fallback)
- Idle cycle animation variants
- Settings menu (volume, language toggle)
- Multiple save slots
- Achievement system
- Localization (English / Taglish flavor)

---

## 11. CONSTRAINTS

- Never hand-edit `builds/arena_ai_simulator/index.html` — only via sha-verified deploy scripts
- Mobile GPU budget (S10+)
- PWA offline-first: zero network requirement after initial load
- All changes additive during migration Phase 4

---

*End of GDD. Updates go to `memory/GAME_DESIGN.md` + `DECISIONS.md` for locked choices. Next: engine architecture doc (Phase 4.4).*
