#!/usr/bin/env python3
"""
Hermes Game Studio Interactive CLI
Run on Termux: python3 ~/projects/hermes_game_studio/cli.py
"""

import sys
import os
from studio import AGENTS, run_agent, full_studio_pipeline

def main():
    print("=" * 60)
    print("🎮 HERMES GAME STUDIO - MULTI-AGENT INTERACTIVE CONSOLE")
    print("   Engine: Ollama (qwen2.5:1.5b) | S10+ Local AI Studio")
    print("=" * 60)
    print("Available Agents:")
    for k, a in AGENTS.items():
        print(f"  @{k:<10} -> {a['emoji']} {a['name']} ({a['title']})")
    print("\nCommands:")
    print("  @pipeline <concept>   -> Run full studio pipeline to build a game")
    print("  @<agent> <message>    -> Chat with specific agent")
    print("  exit / quit           -> Exit studio")
    print("=" * 60 + "\n")
    
    while True:
        try:
            cmd = input("GameStudio> ").strip()
            if not cmd:
                continue
            if cmd.lower() in ["exit", "quit"]:
                print("Closing Hermes Game Studio. Goodbye!")
                break
            
            if cmd.startswith("@pipeline "):
                concept = cmd[10:].strip()
                if concept:
                    full_studio_pipeline(concept)
            elif cmd.startswith("@"):
                parts = cmd[1:].split(" ", 1)
                agent_key = parts[0].lower()
                msg = parts[1] if len(parts) > 1 else ""
                if agent_key in AGENTS:
                    if not msg:
                        msg = input(f"Message for {AGENTS[agent_key]['name']}: ")
                    resp = run_agent(agent_key, msg)
                    print(f"\n{resp}\n")
                else:
                    print(f"Unknown agent @{agent_key}. Choose from: {list(AGENTS.keys())}")
            else:
                resp = run_agent("producer", cmd)
                print(f"\n{resp}\n")
        except KeyboardInterrupt:
            print("\nStudio paused. Type 'exit' to quit.")
        except Exception as e:
            print(f"\n[Error: {e}]")

if __name__ == "__main__":
    main()
