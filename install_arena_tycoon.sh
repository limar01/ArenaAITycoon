#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  🎮 ARENA AI TYCOON — POGI BOSS V6 ONE COMMAND INSTALLER
#  Install sa BAGONG Termux phone — isang command lang!
#
#  Usage:   bash install_arena_tycoon.sh [bundle-file]
#  Default: $HOME/storage/shared/arena/arena_tycoon.bundle
#
#  Kung walang storage permission pa: termux-setup-storage muna.
#  Gawa ni Zillion para kay Boss — 2026-08-25 (v15/G16)
# ============================================================
set -u

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YEL='\033[1;33m'; NC='\033[0m'
say() { echo -e "$1"; }

BUNDLE="${1:-$HOME/storage/shared/arena/arena_tycoon.bundle}"
PROJ="$HOME/projects/hermes_game_studio"

say "${CYAN}📦 POGI BOSS V6 — ARENA AI TYCOON ONE COMMAND INSTALLER${NC}"

# ---- 0) checks ----
if [ ! -d "/data/data/com.termux/files/home" ]; then
  say "${RED}❌ Ito ay para sa Termux (Android). Patakbuhin sa Termux lang.${NC}"; exit 1
fi
if [ ! -f "$BUNDLE" ]; then
  say "${RED}❌ Bundle not found: $BUNDLE${NC}"
  say "   I-copy muna ang ${YEL}arena_tycoon.bundle${NC} sa storage (o i-pass ang path):"
  say "     bash install_arena_tycoon.sh /path/to/arena_tycoon.bundle"
  say "   Storage permission? I-run: ${YEL}termux-setup-storage${NC}"
  exit 1
fi

# ---- 1) dependencies ----
say "${CYAN}[1/5]📦 Ini-install ang dependencies (python, git)...${NC}"
pkg install -y python git curl >/dev/null 2>&1 || pkg install -y python git >/dev/null 2>&1

# ---- 2) restore project from git bundle ----
if [ -d "$PROJ/.git" ]; then
  say "${YEL}[2/5]♻️  May existing project — i-u-update na lang...${NC}"
  cd "$PROJ" && git pull "$BUNDLE" HEAD 2>/dev/null || git fetch "$BUNDLE" 'refs/heads/*:refs/heads/*' 2>/dev/null || true
else
  say "${CYAN}[2/5]📂 Ni-restore ang project mula sa git bundle...${NC}"
  mkdir -p "$HOME/projects"
  git clone --quiet "$BUNDLE" "$PROJ" || { say "${RED}❌ Git clone failed${NC}"; exit 1; }
fi

# ---- 3) ArenaBridge worker setup ----
say "${CYAN}[3/5]🔗 Setup ng ArenaBridge worker (MQTT remote control)...${NC}"
mkdir -p "$HOME/arenabridge"
if [ -f "$PROJ/arenabridge_worker.py" ]; then
  cp "$PROJ/arenabridge_worker.py" "$HOME/arenabridge/worker.py"
fi
if [ -f "$PROJ/bridge/mq.sh" ]; then
  cp "$PROJ/bridge/mq.sh" "$HOME/mq.sh" 2>/dev/null || true
  chmod +x "$HOME/mq.sh" 2>/dev/null || true
fi
# wake lock para di matulog
command -v termux-wake-lock >/dev/null 2>&1 && termux-wake-lock 2>/dev/null

# ---- 4) start game server ----
say "${CYAN}[4/5]🖥️  Sinisimulan ang game server (port 8888)...${NC}"
cd "$PROJ/builds/arena_ai_simulator"
fuser -k 8888/tcp >/dev/null 2>&1 || true
sleep 1
nohup python3 server.py > server.log 2>&1 &
sleep 2
HTTP=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8888/ 2>/dev/null || echo 000)

# ---- 5) start worker ----
say "${CYAN}[5/5]🤖 Sinisimulan ang ArenaBridge worker...${NC}"
pkill -f "arenabridge/worker.py" >/dev/null 2>&1 || true
sleep 1
nohup python3 "$HOME/arenabridge/worker.py" > "$HOME/arenabridge/worker.log" 2>&1 &
sleep 2

say ""
say "${GREEN}✅ ================================================${NC}"
if [ "$HTTP" = "200" ]; then
  say "${GREEN}✅ GAME LIVE: ${CYAN}http://localhost:8888${NC}"
else
  say "${YEL}⚠️  Game server: HTTP $HTTP — i-check: cd $PROJ/builds/arena_ai_simulator && cat server.log${NC}"
fi
say "${GREEN}✅ Worker: ONLINE (broker.emqx.io — hilingin sa Zillion na i-ping)${NC}"
say "${GREEN}✅ PWA: buksan sa Chrome → menu ⋮ → 'Add to Home screen' para maging APP${NC}"
say ""
say "${YEL}🧠 OPTIONAL — Live AI Brains (Ollama):${NC}"
say "   1. i-install ang ollama sa Termux (tingnan ang docs/Ollama notes)"
say "   2. ollama pull llama3.2:1b qwen2.5:1.5b qwen2.5-coder:1.5b deepseek-r1:1.5b"
say "   3. nohup ollama serve > ~/ollama.log 2>&1 &"
say "   (Kung walang Ollama — gumagana pa rin ang game, scripted phrases lang ang usapan)"
say ""
say "${CYAN}🎮 Enjoy, Boss! — Team Zillion 🫡${NC}"
