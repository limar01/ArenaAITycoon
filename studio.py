#!/usr/bin/env python3
"""
Hermes Game Studio: Local Multi-Agent Game Development Framework
Location: ~/projects/hermes_game_studio/studio.py
Engine: Ollama (qwen2.5:1.5b) on Termux Android ARM64
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
import argparse

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.environ.get("STUDIO_MODEL", "qwen2.5:1.5b")
BASE_DIR = os.path.expanduser("~/projects/hermes_game_studio")
BUILDS_DIR = os.path.join(BASE_DIR, "builds")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

os.makedirs(BUILDS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

AGENTS = {
    "producer": {
        "id": "producer",
        "name": "Director Marcus",
        "title": "Producer & Studio Head",
        "emoji": "🎬",
        "soul": "You are Director Marcus, a pragmatic, charismatic, and vision-driven Producer & Studio Head. Your primary focus is delivering complete, fun, playable games on schedule without feature creep. You speak with clear executive authority, organize tasks, assign milestones to team members (Aria, Cody, Pixel, Jax), and synthesize creative and technical inputs into actionable sprint plans.",
        "skill": "Game studio leadership, scope management, milestone tracking, feature prioritization, team coordination."
    },
    "designer": {
        "id": "designer",
        "name": "Aria",
        "title": "Game Systems & Narrative Designer",
        "emoji": "🕹️",
        "soul": "You are Aria, an obsessive gamer and brilliant Game Systems & Narrative Designer. You craft compelling Game Design Documents (GDD), core gameplay loops, player progression balance, combat systems, economy tuning, and rich lore/narrative trees. You focus heavily on game feel and player engagement.",
        "skill": "Game Design Documents (GDD), core gameplay loop design, economy balancing, narrative design, level progression."
    },
    "programmer": {
        "id": "programmer",
        "name": "Cody",
        "title": "Lead Programmer & Tech Wizard",
        "emoji": "💻",
        "soul": "You are Cody, a master programmer and clean-code zealot. You write modular, well-commented, high-performance Python (Pygame/CLI) or GDScript game code. You think in state machines, algorithms, game loops, and clean OOP patterns. When given a game concept or GDD, you write complete, working, bug-free executable code.",
        "skill": "Python game programming, state machines, math & physics logic, code optimization, bug fixing, refactoring."
    },
    "artist": {
        "id": "artist",
        "name": "Pixel",
        "title": "Graphic Artist & UI Architect",
        "emoji": "🎨",
        "soul": "You are Pixel, a visual artist and UI/UX designer. In terminal/text environments, you craft creative ASCII/ANSI sprite art, UI wireframes, tilemaps, and color themes. For graphical games, you specify SVG assets, sprite sheets, and precise prompt engineering specs for AI art tools.",
        "skill": "ASCII/ANSI sprite art, SVG UI asset mockups, visual style guides, color palette design, asset manifests."
    },
    "qa": {
        "id": "qa",
        "name": "Jax",
        "title": "QA Specialist & Bug Hunter",
        "emoji": "🧪",
        "soul": "You are Jax, a chaotic playtester and ruthless QA auditor. Your passion is finding edge cases, breaking code, exploiting unbalanced game mechanics, and ensuring software stability. You audit code written by Cody, test game balance created by Aria, and output structured Bug Reports with clear steps to reproduce.",
        "skill": "Code auditing, playtest simulation, edge-case testing, balance verification, structured bug reporting."
    }
}

def call_ollama(system_prompt, user_prompt, temperature=0.7):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_thread": 4
        }
    }
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res.get("message", {}).get("content", "").strip()
    except Exception as e:
        return f"[Ollama Error: {e}]"

def run_agent(agent_key, prompt, context=""):
    agent = AGENTS.get(agent_key)
    if not agent:
        return f"Unknown agent: {agent_key}"
    
    system_prompt = (
        f"You are {agent['name']} ({agent['title']}) {agent['emoji']}.\n"
        f"SOUL: {agent['soul']}\n"
        f"SKILL: {agent['skill']}\n\n"
        f"Context/Project Details:\n{context}\n\n"
        "Respond strictly in character as a professional game studio team member."
    )
    
    print(f"\n{agent['emoji']} [{agent['name']} - {agent['title']}] Thinking...")
    response = call_ollama(system_prompt, prompt)
    return response

def full_studio_pipeline(game_concept):
    print("=" * 65)
    print(f"🎮 HERMES GAME STUDIO: PIPELINE STARTING FOR '{game_concept}'")
    print("=" * 65)
    
    # Step 1: Producer Scope & Task Assignment
    p_prompt = f"We are building a new game concept: '{game_concept}'. Break this project down into milestone goals for Aria (Designer), Cody (Programmer), Pixel (Artist), and Jax (QA). Set the technical scope."
    producer_plan = run_agent("producer", p_prompt)
    print(f"\n🎬 [Director Marcus]:\n{producer_plan}\n")
    
    # Step 2: Game Designer GDD
    d_prompt = f"Based on Producer Marcus's vision:\n{producer_plan}\n\nCreate a concise Game Design Document (GDD) for '{game_concept}'. Include Core Loop, Mechanics, Controls, and Rules."
    gdd = run_agent("designer", d_prompt, context=producer_plan)
    print(f"\n🕹️ [Aria - Designer]:\n{gdd}\n")
    
    # Save GDD
    gdd_filename = f"{game_concept.lower().replace(' ', '_')}_GDD.md"
    gdd_path = os.path.join(DOCS_DIR, gdd_filename)
    with open(gdd_path, "w", encoding="utf-8") as f:
        f.write(f"# GDD: {game_concept}\n\n{gdd}\n")
    print(f"📄 Saved GDD to: {gdd_path}")
    
    # Step 3: Artist Asset & Visual Design
    art_prompt = f"Based on the GDD for '{game_concept}':\n{gdd}\n\nDesign the visual style, ASCII/ANSI sprites, color theme, and UI layout for this game."
    art_spec = run_agent("artist", art_prompt, context=gdd)
    print(f"\n🎨 [Pixel - Artist]:\n{art_spec}\n")
    
    # Step 4: Programmer Writes Code
    prog_prompt = f"Write a complete, single-file playable Python terminal/text game for '{game_concept}'.\nFollow Aria's GDD and Pixel's visual design.\nGDD:\n{gdd}\n\nART SPEC:\n{art_spec}\n\nIMPORTANT: Return ONLY valid, complete executable Python code inside a ```python codeblock."
    code_res = run_agent("programmer", prog_prompt, context=gdd)
    print(f"\n💻 [Cody - Programmer]:\n{code_res}\n")
    
    # Extract Python code block
    code = ""
    if "```python" in code_res:
        code = code_res.split("```python")[1].split("```")[0].strip()
    elif "```" in code_res:
        code = code_res.split("```")[1].split("```")[0].strip()
    else:
        code = code_res
        
    build_filename = f"{game_concept.lower().replace(' ', '_')}.py"
    build_path = os.path.join(BUILDS_DIR, build_filename)
    with open(build_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"💾 Saved Game Build to: {build_path}")
    
    # Step 5: QA Playtest & Code Audit
    qa_prompt = f"Audit the Python code written by Cody for '{game_concept}':\n\n```python\n{code}\n```\n\nTest logic, edge cases, infinite loops, and game balance. Provide a QA Audit Report."
    qa_report = run_agent("qa", qa_prompt, context=code)
    print(f"\n🧪 [Jax - QA Specialist]:\n{qa_report}\n")
    
    print("=" * 65)
    print(f"✅ GAME STUDIO PIPELINE COMPLETE FOR '{game_concept}'")
    print(f"  GDD File   : {gdd_path}")
    print(f"  Game Build : {build_path}")
    print(f"  Run Game   : python3 {build_path}")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Hermes Game Studio Multi-Agent Framework")
    parser.add_argument("--pipeline", type=str, help="Run full game studio pipeline for a game concept")
    parser.add_argument("--agent", type=str, choices=["producer", "designer", "programmer", "artist", "qa"], help="Query a specific agent")
    parser.add_argument("--prompt", type=str, help="Prompt for specific agent")
    
    args = parser.parse_args()
    
    if args.pipeline:
        full_studio_pipeline(args.pipeline)
    elif args.agent and args.prompt:
        res = run_agent(args.agent, args.prompt)
        print(res)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
