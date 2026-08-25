# 🎮 ARENA AI TYCOON

> A cozy top-down pixel-art **AI studio life sim** — 10 AI personas live and work in a canvas office, with **live LLM brains (Ollama)**, real collision, dynamic events, PWA install, and a full agentic dev pipeline.

![status](https://img.shields.io/badge/status-v15%20LIVE-brightgreen) ![platform](https://img.shields.io/badge/platform-Android%20%2B%20Termux-blue) ![engine](https://img.shields.io/badge/engine-HTML5%20Canvas-orange)

## ✨ Features

- 🧠 **Live LLM Brains** — every character thinks & speaks with real AI (local Ollama models: `llama3.2`, `qwen2.5`, `qwen2.5-coder`, `deepseek-r1`). Tap any agent → live Taglish reply. Graceful fallback to scripted phrases when Ollama is off.
- 🚶 **True 4-direction animation** — real walk cycles (3-frame), front/back/side views, idle breathing
- 🧱 **Full collision** — walls + furniture (A* pathfinding, agents walk *around* the pool table, not through it)
- 🎬 **Living office events** — auto **Beer Friday** (4PM Fri), random **Coffee Machine Incidents** (with smoke + AI complaints), event-aware AI chatter
- 🎵 **Dynamic soundtrack** — time-of-day BGM (morning / midday / evening / night / party)
- 📦 **PWA** — installable as a real app, works **offline** (service worker)
- 🗺️ 1080p widescreen campus, 10 zones, billiards physics, arcade, gym, 24h clock, save/load

## 🚀 Install (Android / Termux)

One command, if you have the private bundle:

```bash
bash install_arena_tycoon.sh /path/to/arena_tycoon.bundle
```

Manual:

```bash
pkg install python git -y
git clone <this-repo> ~/projects/hermes_game_studio
cd ~/projects/hermes_game_studio/builds/arena_ai_simulator
python3 server.py &
# open http://localhost:8888 in Chrome
```

Optional (live AI brains): install [Ollama](https://ollama.com) on Termux, then:
```bash
ollama pull llama3.2:1b qwen2.5:1.5b qwen2.5-coder:1.5b deepseek-r1:1.5b
nohup ollama serve > ~/ollama.log 2>&1 &
```

## 🤖 The Agentic Pipeline (how this was built)

This game was built **by an AI team, for an AI studio sim** — a real dogfooding project:

| Persona | Role | Model |
|---|---|---|
| Zillion | Tech Director (lead) | qwen2.5 |
| Marcus | Producer | llama3.2 |
| Aria | Systems Designer | llama3.2 |
| Cody | Lead Programmer | qwen2.5-coder |
| Pixel | Graphic Artist | qwen2.5 |
| Echo | Audio Director | qwen2.5 |
| Vortex | Shader Architect | qwen2.5-coder |
| Jax | QA Bug Hunter | deepseek-r1 |
| Vanguard | AAA Quality Judge | deepseek-r1 |
| Chronos | Memory Anchor | qwen2.5 |

Development runs through **gates** (Boss-approved milestones), remote-controlled over MQTT from a chat agent (`arenabridge` — see `arenabridge_worker.py`), with automated headless-browser QA, sha-verified deploys, and a persistent **Memory Core** (`docs/ARENA_AI_TYCOON_MEMORY_CORE.md`) that documents every gate.

## 📁 Repo Layout

```
builds/arena_ai_simulator/   ← the game (single-file HTML, base64 assets)
  versions/                  ← release history v11..v15
docs/                        ← GDDs, memory core, audits
tools/                       ← gate deploy scripts (patch_gate7..15.py)
qa/                          ← headless QA rig + evidence
anim_sheets_master/          ← source sprite sheets
bridge/                      ← MQTT remote-control client
install_arena_tycoon.sh      ← one-command installer
```

## ⚠️ Security Note

Bridge credentials are **not** in this repo (redacted). The ArenaBridge worker reads its key from `~/arenabridge/arenabridge.key` or the `ARENABRIDGE_KEY` env var.

---

*Built by **Team Zillion** for **Boss** — 2026. Mabuhay! 🇵🇭*
