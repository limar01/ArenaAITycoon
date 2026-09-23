#!/usr/bin/env bash
cd ~/Projects/workspace/ArenaAITycoon
echo "[1/3] Pulling qwen2.5-coder:1.5b for Cody & Vortex..." > model_pull_status.log
ollama pull qwen2.5-coder:1.5b >> model_pull_status.log 2>&1

echo "[2/3] Pulling deepseek-r1:1.5b for Jax & Vanguard..." >> model_pull_status.log
ollama pull deepseek-r1:1.5b >> model_pull_status.log 2>&1

echo "[3/3] Pulling llama3.2:1b for Marcus & Aria..." >> model_pull_status.log
ollama pull llama3.2:1b >> model_pull_status.log 2>&1

echo "ALL SPECIALIZED MODELS DOWNLOADED AND LOADED SUCCESSFULLY!" >> model_pull_status.log
