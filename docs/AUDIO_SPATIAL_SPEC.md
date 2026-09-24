# 🔊 SPATIAL AUDIO SPEC — ARENA AI TYCOON
## AIT-006 Deliverable (Audio Design Doc — Implementation Ready)

**Author:** Echo (Audio Director) · **Date:** 2026-09-23 · **Status:** Draft
**Source:** GDD §6 (Audio), current v15 Web Audio system, mobile performance budget

---

## 1. AUDIO ARCHITECTURE OVERVIEW

```
Web Audio API Context
├── Master Gain (volume control)
│   ├── BGM Source (oscillator / buffer)
│   │   └── BGM Gain (per-track volume)
│   ├── SFX Group (footsteps, blips, UI, events)
│   │   └── SFX Gain
│   └── Ambience Group (zone audio, muffled variants)
│       └── Ambience Gain
└── Low-pass / High-pass Filters (zone transition)
```

### Core Principles
- **Mobile first:** AudioContext starts suspended on mobile; must resume on touch
- **No cracks/pops:** All oscillators ramp gain over 0.01s; no abrupt stops
- **Zone-aware:** Audio crossfades based on boss/agent position
- **Time-of-day adaptive:** BGM shifts based on sim time (morning calm → day upbeat → evening lounge → night quiet)
- **Event-triggered:** SFX synced to in-game actions

---

## 2. BGM SYSTEM (Background Music)

### Tracks (5 base moods)

| Track | Sim Time | Key/Tempo | Feel |
|-------|----------|-----------|------|
| Morning | 06:00-10:00 | C major, 120 BPM | Calm, arpeggiated |
| Work Day | 10:00-16:00 | G major, 140 BPM | Upbeat, busy |
| Evening | 16:00-20:00 | F major, 90 BPM | Lounge, chord pads |
| Night | 20:00-06:00 | A minor, 60 BPM | Quiet, sparse |
| Party (sub-routine) | Beer Friday / events | D major, 130 BPM | Celebration, brighter |

### Implementation
```javascript
const bgmSource = audioCtx.createOscillator();
bgmSource.type = 'triangle';
bgmSource.frequency.value = 220; // C root
const bgmGain = audioCtx.createGain();
bgmSource.connect(bgmGain).connect(masterGain);
bgmSource.start();

// Time-of-day transition
function updateBGM(simHour) {
  // Crossfade between track presets based on hour
  // Smooth over 10 seconds
}
```

### Mobile Resume Handling
```javascript
// Must call resume() on first user interaction
function initAudio() {
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
}
```

---

## 3. SFX SYSTEM (Sound Effects)

### SFX Categories

| Category | Sounds | Trigger |
|----------|--------|---------|
| Footsteps | 4-dir step sounds (16-bit stepped noise) | Agent movement, Boss walk |
| Blips | UI click, dialogue bubble | UI interaction |
| Cheer | Victory / event success | Beer Friday, arcade win, gate approval |
| Sad blip | Error / rejection | Buy failure, low energy |
| Arcade SFX | Shoot, explosion, coin | Minigame actions |
| Bell / chime | Save complete, threshold reached | Save, level up |
| Bell (pause) | Gate pause bell | Auto-pause gate trigger |

### SFX Generation (no samples needed)
```javascript
function playSFX(name) {
  const ctx = audioCtx;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  
  const presets = {
    blip: { type: 'square', freq: 800, dur: 0.08, vol: 0.1 },
    cheer: { type: 'sine', freq: 600, dur: 0.3, vol: 0.15 },
    footstep: { type: 'triangle', freq: 150, dur: 0.05, vol: 0.08 },
    // ...
  };
  
  const p = presets[name];
  if (!p) return;
  
  osc.type = p.type;
  osc.frequency.value = p.freq;
  gain.gain.setValueAtTime(0, ctx.currentTime);
  gain.gain.linearRampToValueAtTime(p.vol, ctx.currentTime + 0.01);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + p.dur);
  
  osc.connect(gain).connect(sfxGroup);
  osc.start();
  osc.stop(ctx.currentTime + p.dur + 0.05);
}
```

---

## 4. SPATIAL AUDIO (Zone-Awareness)

### Zone Effects
- **Lounge zone:** Low-pass filter (muffled, cozy feel when near sofa)
- **Dev Core zone:** Brighter EQ boost (focus feel near desks)
- **Arcade zone:** Higher volume boost for arcade SFX when cabinet is active
- **Gym zone:** Reverb-matched (echoey feel)

### Implementation Plan
```javascript
// Zone distance calculation
function getZoneAt(x, y) {
  // Return zone ID based on bounding box check
}

// Speaker assignment
const zoneSpeakers = {
  lounge: { gain: 0.8, filter: 'lowpass' },
  arcade: { gain: 1.0, filter: 'none' },
  devcore: { gain: 1.0, filter: 'highpass' },
  // ...
};
```

---

## 5. MOBILE AUDIO HANDLING

### Critical Requirements
1. **AudioContext starts suspended on iOS/Safari and sometimes Chrome** — must resume on first touch
2. **Audio should mute when tab backgrounded** — auto-pause BGM
3. **Graceful degradation:** If initAudio fails, game should still run silently

### Implementation
```javascript
let audioReady = false;

function ensureAudio() {
  if (audioReady) return;
  try {
    initAudio();
    audioReady = true;
  } catch(e) {
    console.warn('Audio unavailable:', e.message);
    audioReady = false;
  }
}

// Touch handler
canvas.addEventListener('touchstart', () => ensureAudio(), {passive: true});
canvas.addEventListener('mousedown', () => ensureAudio());
```

---

## 6. PERFORMANCE BUDGET

| Budget | Limit | Reason |
|--------|-------|--------|
| Max oscillators active | 8 | Mobile CPU |
| Max SFX per frame | 3 | Avoid queue buildup |
| BGM buffer size | 1024 samples | Low latency on mobile |
| Total Web Audio nodes | < 30 | Memory budget |

---

## 7. IMPLEMENTATION TASKS (AIT-006 breakdown)

| Sub-task | Description | Priority |
|----------|-------------|----------|
| AIT-006a | BGM time-of-day system (5 tracks, crossfade) | HIGH |
| AIT-006b | SFX library (footsteps, blips, cheer, bell) | HIGH |
| AIT-006c | Mobile audio resume + error handling | HIGH |
| AIT-006d | Zone-aware spatial effects (lowpass/HPF) | MEDIUM |
| AIT-006e | BGM mute on tab blur | MEDIUM |
| AIT-006f | Volume control UI (master slider) | MEDIUM |

---

## 8. KNOWN GAPS

- No recorded audio samples (all procedural synthesis for now)
- Zone audio spatialization is basic (distance-based volume only)
- No dynamic mixing (BGM modulates based on in-game intensity)

---

*End of Spatial Audio Spec. Implementation by Echo after Boss review.*
