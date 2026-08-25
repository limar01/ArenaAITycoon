# 🏛️ HERMES GAME STUDIO: AAA MULTI-AGENT ROADMAP (V2)

## 1. 👥 COMPLETE STUDIO ROLES & HIERARCHY

```text
                     ┌──────────────────────────┐
                     │    BOSS (Studio Owner)   │
                     └─────────────┬────────────┘
                                   │
                     ┌─────────────▼────────────┐
                     │   ZILLION (Tech Director)│
                     └─────────────┬────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         │                                                   │
┌────────▼────────────────┐                         ┌────────▼────────────────┐
│   JUDGE VANGUARD        │                         │     KEEPER CHRONOS      │
│ (AAA Quality Orchestrator│                        │ (Memory & Context Anchor│
│  & Gauntlet Loop Engine)│                         │  Prevents Hallucinations│
└────────┬────────────────┘                         └────────┬────────────────┘
         │                                                   │
         └─────────────────────────┬─────────────────────────┘
                                   │
       ┌───────────────────────────┼───────────────────────────┐
       │                           │                           │
┌──────▼───────┐            ┌──────▼───────┐            ┌──────▼───────┐
│ DIRECTOR     │            │ ARIA         │            │ CODY         │
│ MARCUS       │            │ (Designer &  │            │ (Lead        │
│ (Producer)   │            │  Architect)  │            │  Programmer) │
└──────────────┘            └──────────────┘            └──────────────┘
       │                           │                           │
┌──────▼───────┐            ┌──────▼───────┐            ┌──────▼───────┐
│ PIXEL        │            │ ECHO         │            │ VORTEX       │
│ (Graphic     │            │ (Audio       │            │ (WebGL/Shader│
│  Artist)     │            │  Director)   │            │  Architect)  │
└──────────────┘            └──────────────┘            └──────────────┘
                                   │
                            ┌──────▼───────┐
                            │ JAX          │
                            │ (QA Auditor) │
                            └──────────────┘
```

### 🆕 Specialized Strategic Agents:
1. ⚖️ **Judge Vanguard (AAA Quality Judge & Gauntlet Loop Orchestrator)**:
   - **Soul**: Uncompromising AAA critic, ruthless quality judge.
   - **Skill**: Evaluates code, graphics, audio, and gameplay against strict AAA benchmarks. If quality fails, triggers the **Gauntlet Refinement Loop** (sends work back with actionable fix requirements) until 100% passed.

2. 📜 **Keeper Chronos (Memory Anchor & Context Reminder Agent)**:
   - **Soul**: Master archivist, context guardian, anti-hallucination engine.
   - **Skill**: Storing persistent sub-agent memories (`~/projects/hermes_game_studio/memory/`), fetching active project context, and injecting strict role directives before every agent execution so no sub-agent hallucinates or strays from their assigned role.

3. 🎵 **Echo (Audio & Sound Director)**:
   - **Skill**: Web Audio API synthesis, Howler.js, chiptune/orchestrated soundtracks, sound effect triggers.

4. ⚡ **Vortex (WebGL Graphics & Engine Shader Architect)**:
   - **Skill**: Phaser 3, PixiJS, WebGL 2D/3D shaders, sprite sheet compilation, particle emitters (fire, blood, sparks), screen-shake & hit-stop juice.

---

## 2. 🔄 THE GAUNTLET REFINEMENT LOOP & MEMORY ANCHORING

1. **Context Ingestion by Keeper Chronos**:
   - Before any agent speaks or codes, **Keeper Chronos** fetches the latest project state and agent memory file (`memory/<agent_name>.json`).
   - Injects the strict system prompt to ensure zero hallucination.

2. **Gauntlet Loop Execution by Judge Vanguard**:
   - Once Cody, Pixel, Echo, or Vortex complete a task, **Judge Vanguard** evaluates the output.
   - **IF FAIL**: Automatically assigns fix tasks back to the team. Max loop iteration = 3.
   - **IF PASS**: Hands off the verified deliverable to Zillion for Boss Approval Gate!

---

## 3. 🚧 AAA GAME DEVELOPMENT WORKFLOW (6 BOSS APPROVAL GATES)

Every project moves through 6 Boss Approval Gates:

1. **GATE 1: Concept & Pitch Proposal Gate** (Director Marcus + Boss Sign-off)
2. **GATE 2: Production GDD & Level Map Gate** (Aria + Boss Sign-off)
3. **GATE 3: Visual & Audio Style Guide Gate** (Pixel + Echo + Boss Sign-off)
4. **GATE 4: Core Engine Vertical Slice Gate** (Cody + Vortex + Boss Sign-off on S10+ Phone)
5. **GATE 5: Alpha Content Complete Gate** (Full stage, enemies, boss fight + Boss Sign-off on S10+ Phone)
6. **GATE 6: AAA Production Release Gate** (Final Boss Sign-off 🎉)
