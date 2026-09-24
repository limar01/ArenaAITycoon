# 📈 ECONOMY & PROGRESSION SPEC — ARENA AI TYCOON
## AIT-004 Deliverable (Design Doc — Implementation Ready)

**Author:** Aria (Game Designer) · **Date:** 2026-09-23 · **Status:** Draft for Boss review
**Source:** GDD §3.3, MEMORY_CORE locked decisions, v15 build store system analysis

---

## 1. DESIGN GOALS

| Goal | Metric |
|------|--------|
| Meaningful choices | No dominant strategy; multiple viable paths |
| Cozy pace | No punishing failure state; slow recovery always possible |
| Clear progression | Player understands "what to do next" at all times |
| Balance | No infinite cash exploit; no unwinnable state |
| Mobile session友好 | 5-15 min sessions produce visible progress |

---

## 2. CURRENCY SYSTEM

### Primary Currency: Studio Cash ($)
- Starting: $48,500
- Earn through: arcade minigames, event rewards, passive income from decor
- Spend on: decor upgrades, event triggers, progression unlocks

### Secondary Currency: Team Morale (🔴)
- Aggregate of all 10 agents' happiness average
- 0-100 scale
- Unlocks: bonus events, visual flourishes, audio variations
- No "game over" at 0 — just fewer bonuses

### Tertiary Currency: Reputation (⭐)
- Earn by completing gates, hosting successful events
- Unlocks: new decor tiers, new events, new zones
- Does not decay

---

## 3. INCOME SOURCES

| Source | Type | Base Value | Variance |
|--------|------|------------|----------|
| Arcade minigame (shooter) | Active | $50-200/session | Skill-based |
| Arcade minigame (pool) | Active | $20-80/session | Skill-based |
| Beer Friday event | Passive (weekly) | $500-1500 | Team happiness modifier |
| Coffee incident (random) | Passive | $100-300 | Random trigger |
| Passive income (per in-game hour) | Passive | $50-150/hour | Decor multiplier |
| Daily standup completion | Passive | $200/day | Attendance-based |
| Boss avatar interaction | Active | $10-50/tap | Random gift |

### Passive Income Formula
```
hourly_income = BASE_RATE(100) * decor_multiplier * morale_multiplier

decor_multiplier = 1.0 + sum of owned item bonuses (max +2.0)
morale_multiplier = team_morale / 100  (range 0.0-1.0)
```

---

## 4. EXPENSE ITEMS (Store)

### Current Store Items (8 items)

| Item | Price | Bonus Type | Bonus Value |
|------|-------|------------|-------------|
| RGB Gaming Desks | $5,000 | Coder focus regen | +20% |
| 4K Curved Displays | $8,000 | Compile speed / strain | +15% work efficiency |
| Studio Neon Art | $3,000 | Beer Friday happiness | +30% event happiness |
| Luxury Leather Sofa | $6,000 | Lounge happiness regen | +30% |
| Italian Espresso Bar | $4,500 | Max focus cap | +25% |
| Beer Patio BBQ Grill | $7,500 | All stats at parties | +all +20% |
| Quantum Server Coolers | $10,000 | Passive income | +25% hourly |
| Golden Rubber Duck | $2,500 | Arcade luck (score boost) | +100% arcade rewards |

### Unlock Tiers

| Reputation | Tier | New Items Unlocked |
|------------|------|--------------------|
| 0 | Starter | All 8 current items |
| 50 | Growing | Home theater ($12K, +happiness), Gym equipment ($15K, +energy) |
| 100 | Established | Roof garden ($20K, +morale cap), Recording studio ($18K, audio events) |
| 200 | Prestige | Second floor expansion, outdoor BBQ area, pool table upgrade |

---

## 5. PROGRESSION SYSTEM

### Gate Progression (drives main narrative)

```
G5 Alpha (current)
  → Complete AIT-001..006 (sprite work, QA, deploy)
  → Boss review
  → G6 Beta
     → Full mobile QA pass
     → Economy balance verified
     → Boss review
  → G7 Release Candidate
     → Performance verified
     → All zones complete
     → Boss review
  → G8 Release
     → Vanguard final PASS
     → Boss approval
     → Deploy to phone + public
```

### Side Progression (optional, repeatable)

| System | Description |
|--------|-------------|
| Decor collection | Buy all items across all tiers |
| Event log | Trigger all event types |
| Agent bonds | Tap all agents 100 times each |
| Arcade high score | Beat 1000 points in shooter |
| Speed run | Reach G8 in under 5 hours playtime |

---

## 6. AGENT STAT SYSTEM

Each agent has 3 stats:

| Stat | Range | Drain Rate | Restore Source |
|------|-------|------------|----------------|
| Energy ⚡ | 0-100 | -2/hour work, -0.5/hour idle | Sleep (night), Espresso bar (+25% cap) |
| Focus 🎯 | 0-100 | -3/hour work, -0.5/hour idle | Desk break, RGB desks (+20% regen) |
| Happiness 💖 | 0-100 | -1/hour work, +0.5/hour lounge | Arcade, parties, sofa (+30%), neon art |

### Stat Thresholds

| Range | Effect |
|-------|--------|
| 70-100 | Thriving: full speed, bonus dialogue |
| 40-69 | Content: normal speed |
| 10-39 | Struggling: half speed, complaints |
| 0-9 | Burned out: stationary, recovery mode (no drain) |

### Team Morale Calculation
```
team_morale = average(all 10 agents' happiness)

Effects:
  morale >= 70: +10% passive income, rare bonus events
  morale 40-69: Normal
  morale 10-39: -10% income, agents complain
  morale < 10:  -25% income, recovery mode (no drain until 20+)
```

---

## 7. BALANCE PARAMETERS

### Session Length Targets

| Session | Expected Actions | Cash Earned | Progress |
|---------|------------------|-------------|----------|
| 5 min | 1-2 arcade games, 1 interaction | $100-400 | Small |
| 15 min | 3-5 games, buy 1 item, events | $500-1500 | Medium |
| 1 hour | Full day cycle, multiple items | $2000-5000 | Major |

### Balance Safeguards

| Exploit | Safeguard |
|---------|-----------|
| Arcade farming | Diminishing returns: score multiplier drops 10% per game in 10-min window |
| Save scumming | Save includes RNG seed; reloading doesn't re-randomize |
| Idle income cap | Max 8 hours offline income; requires interaction to claim |
| Rapid buy/sell | No sell value (items are permanent); prevents flipping |

---

## 8. IMPLEMENTATION NOTES

### Save Format Extension
```javascript
// Current save fields: cash, day, simMinutes, vertical, storeItems, agentStats
// New fields to add:

state.reputation = state.reputation || 0;        // New: reputation points
state.totalEarned = state.totalEarned || 0;      // New: lifetime earnings
state.eventsTriggered = state.eventsTriggered || {}; // New: event history
state.arcadeHighScore = state.arcadeHighScore || 0;  // New: best shooter score
state.bondCounts = state.bondCounts || {};       // New: per-agent tap counts
```

### Agent Stat Extension
```javascript
// Current: energy, focus, happiness
// New methods needed:

class Agent {
  updateStats(dt) {
    const workMult = this.currentAction === 'work' ? 1.0 : 0.2;
    this.energy -= 2.0 * workMult * dt;
    this.focus  -= 3.0 * workMult * dt;
    this.happiness -= 1.0 * workMult * dt;
    
    // Decay bounds
    this.energy = Math.max(0, Math.min(100, this.energy));
    this.focus  = Math.max(0, Math.min(100, this.focus + this.focusRegenBonus));
    this.happiness = Math.max(0, Math.min(100, this.happiness));
  }
}
```

---

## 9. OPEN QUESTIONS FOR BOSS

1. **Prestige mechanic:** After G8, should there be a "New Game+" with multipliers or is one playthrough the complete experience?
2. **Free-to-play:** Should the game remain completely free, or is a "support the studio" cosmetic shop acceptable?
3. **Multiplayer:** Any desire for async features (competing studios, shared high scores)?

---

*End of Economy Spec. Implementation tasks (AIT-004a..d) will be created after Boss review.*
