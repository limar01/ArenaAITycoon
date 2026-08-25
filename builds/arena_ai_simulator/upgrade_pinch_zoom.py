#!/usr/bin/env python3
"""
Hermes Game Studio: Upgrades index.html with Pinch-to-Zoom & Pan Navigation Engine
Location on Phone: ~/projects/hermes_game_studio/builds/castlevania_stage1/upgrade_pinch_zoom.py
"""

import os
import sys
import json
import base64

BASE = os.path.expanduser("~/projects/hermes_game_studio/builds/castlevania_stage1")
SPRITES_DIR = os.path.expanduser("~/sprites")

char_b64 = ""
office_b64 = ""

char_path = os.path.join(SPRITES_DIR, "character_sprites_preview.png")
office_path = os.path.join(SPRITES_DIR, "office_topdown_preview.png")

if os.path.exists(char_path):
    with open(char_path, "rb") as f:
        char_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

if os.path.exists(office_path):
    with open(office_path, "rb") as f:
        office_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Arena AI Simulator: Studio Life - Pinch Zoom Edition</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
  body { background: #050508; color: #fff; font-family: 'Courier New', monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
  #game-container { position: relative; width: 100vw; max-width: 800px; display: flex; flex-direction: column; align-items: center; }
  canvas { background: #000; image-rendering: pixelated; image-rendering: crisp-edges; width: 100%; height: auto; aspect-ratio: 320 / 240; border: 4px solid #6820b0; box-shadow: 0 0 35px rgba(184, 120, 248, 0.7); touch-action: none; }
  
  #hud-bar { width: 100%; background: #12121c; border: 2px solid #333; display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; font-size: 10px; font-weight: bold; color: #ffcc00; }
  .status-badge { background: #006622; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 9px; cursor: pointer; }
  .status-paused { background: #aa2200; animation: pulse 1s infinite; }
  .status-party { background: #e45c10; color: #fff; animation: party 0.5s infinite; }
  
  @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
  @keyframes party { 0% { background: #e45c10; } 50% { background: #b878f8; } 100% { background: #e45c10; } }

  #instruction-tip { margin-top: 6px; font-size: 11px; color: #aaa; text-align: center; }
</style>
</head>
<body>

<div id="game-container">
  <div id="hud-bar">
    <div>🏛️ ARENA AI SIMULATOR (PINCH-ZOOM ENGINE)</div>
    <div>ZOOM: <span id="zoom-level" style="color:#00ffff;">1.0x</span></div>
    <div>STATUS: <span id="pause-badge" class="status-badge status-party" onclick="togglePause()">BEER FRIDAY 🍺</span></div>
  </div>

  <canvas id="canvas" width="320" height="240"></canvas>
  <div id="instruction-tip">🔍 <b>PINCH 2 FINGERS TO ZOOM IN/OUT | TOUCH SPRITES TO INTERACT!</b></div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const zoomLevelDisplay = document.getElementById('zoom-level');
const pauseBadge = document.getElementById('pause-badge');

// Web Audio Synth
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let actx = null;

function initAudio() {
  if (!actx) actx = new AudioCtx();
  if (actx.state === 'suspended') actx.resume();
}

function playSFX(type) {
  if (!actx) return;
  const now = actx.currentTime;
  const osc = actx.createOscillator();
  const gain = actx.createGain();
  osc.connect(gain);
  gain.connect(actx.destination);

  if (type === 'blip') {
    osc.type = 'square';
    osc.frequency.setValueAtTime(520, now);
    osc.frequency.setValueAtTime(680, now + 0.04);
    gain.gain.setValueAtTime(0.15, now);
    gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
    osc.start(now);
    osc.stop(now + 0.08);
  } else if (type === 'pool_hit') {
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(900, now);
    osc.frequency.exponentialRampToValueAtTime(150, now + 0.06);
    gain.gain.setValueAtTime(0.3, now);
    gain.gain.linearRampToValueAtTime(0.01, now + 0.06);
    osc.start(now);
    osc.stop(now + 0.06);
  } else if (type === 'cheer') {
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(400, now);
    osc.frequency.setValueAtTime(600, now + 0.1);
    osc.frequency.setValueAtTime(800, now + 0.2);
    gain.gain.setValueAtTime(0.2, now);
    gain.gain.linearRampToValueAtTime(0.01, now + 0.3);
    osc.start(now);
    osc.stop(now + 0.3);
  }
}

// Load Real PNG Sprite Assets
const officeImg = new Image();
officeImg.src = '""" + office_b64 + """';

const spriteSheetImg = new Image();
spriteSheetImg.src = '""" + char_b64 + """';

// State
let simPaused = false;
let isBeerFriday = true;
let simMinutes = 16 * 60;
let activeBubble = null;
let bubbleTimer = 0;

// Zoom & Pan State
let zoomScale = 1.0;
let panX = 0;
let panY = 0;
let initialPinchDist = null;
let initialZoom = 1.0;
let isPanning = false;
let lastPanX = 0;
let lastPanY = 0;

// Detailed Agent Objects
const agents = [
  { id: 'zillion', name: 'Zillion', role: 'Tech Director', x: 125, y: 40, sx: 0, sy: 0, phrase: 'Pinch-To-Zoom Engine is LIVE! Zoom in to inspect HD sprites!' },
  { id: 'marcus', name: 'Marcus', role: 'Producer', x: 45, y: 50, sx: 1, sy: 0, phrase: 'Beer Friday Party is LIVE! Cheers Boss!' },
  { id: 'aria', name: 'Aria', role: 'Designer', x: 165, y: 40, sx: 2, sy: 0, phrase: 'High-definition 16-bit pixel sprites active!' },
  { id: 'cody', name: 'Cody', role: 'Programmer', x: 205, y: 40, sx: 3, sy: 0, phrase: 'qwen2.5-coder model loaded for WebGL code!' },
  { id: 'pixel', name: 'Pixel', role: 'Artist', x: 245, y: 40, sx: 4, sy: 0, phrase: 'Zoom in to see my beret and Cody backward cap!' },
  { id: 'echo', name: 'Echo', role: 'Audio', x: 285, y: 40, sx: 0, sy: 1, phrase: '16-Bit 44.1kHz MIDI OST playing in stereo!' },
  { id: 'vortex', name: 'Vortex', role: 'Shader Dev', x: 165, y: 85, sx: 1, sy: 1, phrase: 'WebGL fragment shaders & particle emitters active!' },
  { id: 'jax', name: 'Jax', role: 'QA Auditor', x: 205, y: 85, sx: 2, sy: 1, phrase: 'Pinch zoom into Jax yellow rubber duck on shoulder!' },
  { id: 'vanguard', name: 'Vanguard', role: 'AAA Judge', x: 245, y: 85, sx: 3, sy: 1, phrase: 'AAA Benchmark: Pinch Zoom 100% PASSED!' },
  { id: 'chronos', name: 'Chronos', role: 'Memory Anchor', x: 285, y: 85, sx: 4, sy: 1, phrase: 'Savepoint v3.0 anchored in phone storage!' }
];

// Billiards Minigame State
const poolBalls = [
  { x: 160, y: 170, vx: 0, vy: 0, color: '#ffffff' },
  { x: 145, y: 168, vx: 0, vy: 0, color: '#ee2211' },
  { x: 145, y: 172, vx: 0, vy: 0, color: '#ffff00' },
  { x: 138, y: 170, vx: 0, vy: 0, color: '#38b0de' }
];

function updateSimulation() {
  if (simPaused) return;

  // Wander AI
  if (Math.random() < 0.02) {
    const talker = agents[Math.floor(Math.random() * agents.length)];
    if (isBeerFriday) {
      talker.x = 130 + Math.random() * 110;
      talker.y = 145 + Math.random() * 55;
    } else {
      talker.x = 125 + (agents.indexOf(talker) % 5) * 40;
      talker.y = agents.indexOf(talker) < 5 ? 40 : 85;
    }
  }

  // Random Speech Bubbles
  if (bubbleTimer > 0) {
    bubbleTimer--;
  } else if (Math.random() < 0.015) {
    const talker = agents[Math.floor(Math.random() * agents.length)];
    activeBubble = { agent: talker, text: talker.phrase };
    bubbleTimer = 150;
    playSFX('blip');
  }

  // Billiards Physics
  for (let b of poolBalls) {
    b.x += b.vx;
    b.y += b.vy;
    b.vx *= 0.95;
    b.vy *= 0.95;
    if (b.x < 138 || b.x > 180) b.vx *= -1;
    if (b.y < 158 || b.y > 180) b.vy *= -1;
  }
}

// Render Engine with Pinch-Zoom Transform Matrix
function render() {
  ctx.fillStyle = '#0a0a10';
  ctx.fillRect(0, 0, 320, 240);

  ctx.save();
  // Apply Pinch Zoom & Pan Transformation
  ctx.translate(160 + panX, 120 + panY);
  ctx.scale(zoomScale, zoomScale);
  ctx.translate(-160, -120);

  if (officeImg.complete && officeImg.naturalWidth > 0) {
    ctx.drawImage(officeImg, 0, 0, 320, 240);
  } else {
    ctx.fillStyle = '#1c1c2b'; ctx.fillRect(5, 18, 310, 217);
    ctx.fillStyle = isBeerFriday ? '#2a1a38' : '#2a2a3e'; ctx.fillRect(8, 21, 304, 211);
  }

  // Render Character Sprites
  for (let a of agents) {
    if (spriteSheetImg.complete && spriteSheetImg.naturalWidth > 0) {
      const sw = spriteSheetImg.naturalWidth / 5;
      const sh = spriteSheetImg.naturalHeight / 2;
      const sx = (a.sx % 5) * sw;
      const sy = Math.floor(a.sy % 2) * sh;

      ctx.drawImage(spriteSheetImg, sx, sy, sw, sh, a.x - 14, a.y - 18, 28, 28);
    } else {
      ctx.fillStyle = a.coat || '#38b0de';
      ctx.fillRect(a.x - 6, a.y - 6, 12, 12);
    }

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 7px monospace';
    ctx.shadowColor = '#000000';
    ctx.shadowBlur = 3;
    ctx.fillText(a.name, a.x - (a.name.length * 2), a.y + 14);
    ctx.shadowBlur = 0;
  }

  // Speech Bubbles
  if (bubbleTimer > 0 && activeBubble) {
    const ag = activeBubble.agent;
    const bx = Math.max(10, Math.min(190, ag.x - 40));
    const by = Math.max(25, ag.y - 36);

    ctx.fillStyle = '#ffffff'; ctx.fillRect(bx, by, 120, 22);
    ctx.strokeStyle = '#000000'; ctx.lineWidth = 1; ctx.strokeRect(bx, by, 120, 22);
    ctx.fillRect(ag.x - 2, by + 21, 5, 4);

    ctx.fillStyle = '#000000'; ctx.font = 'bold 7px monospace';
    ctx.fillText(`${ag.name}:`, bx + 4, by + 8);
    ctx.font = '6px monospace';
    ctx.fillText(activeBubble.text.substring(0, 26), bx + 4, by + 18);
  }

  ctx.restore();

  // Paused Overlay
  if (simPaused) {
    ctx.fillStyle = 'rgba(0,0,0,0.65)';
    ctx.fillRect(0, 0, 320, 240);

    ctx.fillStyle = '#aa2200'; ctx.fillRect(30, 95, 260, 50);
    ctx.strokeStyle = '#ffaa00'; ctx.lineWidth = 2; ctx.strokeRect(30, 95, 260, 50);

    ctx.fillStyle = '#ffffff'; ctx.font = 'bold 10px monospace';
    ctx.fillText('🔒 PENDING BOSS GATE APPROVAL', 65, 115);
    ctx.fillStyle = '#ffcc00'; ctx.font = '8px monospace';
    ctx.fillText('SIMULATION TIME FROZEN | TAP STATUS TO RESUME', 44, 132);
  }
}

function loop() {
  updateSimulation();
  render();
  requestAnimationFrame(loop);
}

// Pinch-to-Zoom & Pan Gesture Event Listeners
function getTouchDist(e) {
  return Math.hypot(
    e.touches[0].clientX - e.touches[1].clientX,
    e.touches[0].clientY - e.touches[1].clientY
  );
}

canvas.addEventListener('touchstart', e => {
  initAudio();
  if (e.touches.length === 2) {
    initialPinchDist = getTouchDist(e);
    initialZoom = zoomScale;
  } else if (e.touches.length === 1) {
    isPanning = true;
    lastPanX = e.touches[0].clientX;
    lastPanY = e.touches[0].clientY;

    const rect = canvas.getBoundingClientRect();
    const scaleX = 320 / rect.width;
    const scaleY = 240 / rect.height;

    let clickX = (e.touches[0].clientX - rect.left) * scaleX;
    let clickY = (e.touches[0].clientY - rect.top) * scaleY;
    clickX = 160 + (clickX - 160 - panX) / zoomScale;
    clickY = 120 + (clickY - 120 - panY) / zoomScale;

    // Check Agent Touches
    let touchedAgent = null;
    for (let a of agents) {
      if (Math.abs(clickX - a.x) < 20 && Math.abs(clickY - a.y) < 20) {
        touchedAgent = a;
        break;
      }
    }

    if (touchedAgent) {
      activeBubble = { agent: touchedAgent, text: `BOSS touched ${touchedAgent.name}! ${touchedAgent.phrase}` };
      bubbleTimer = 180;
      playSFX('cheer');
      return;
    }

    // Check Billiards Touch
    if (clickX >= 130 && clickX <= 190 && clickY >= 145 && clickY <= 195) {
      playSFX('pool_hit');
      poolBalls[0].vx = (Math.random() - 0.5) * 4;
      poolBalls[0].vy = (Math.random() - 0.5) * 4;
      activeBubble = { agent: { name: 'BOSS', x: 160, y: 170 }, text: 'BOSS shot a break on the Pool Table! 🎱' };
      bubbleTimer = 180;
      return;
    }
  }
});

canvas.addEventListener('touchmove', e => {
  e.preventDefault();
  if (e.touches.length === 2 && initialPinchDist) {
    const currentDist = getTouchDist(e);
    const zoomFactor = currentDist / initialPinchDist;
    zoomScale = Math.max(0.8, Math.min(3.5, initialZoom * zoomFactor));
    zoomLevelDisplay.innerText = `${zoomScale.toFixed(1)}x`;
  } else if (e.touches.length === 1 && isPanning) {
    const dx = e.touches[0].clientX - lastPanX;
    const dy = e.touches[0].clientY - lastPanY;
    panX += dx * 0.5;
    panY += dy * 0.5;
    lastPanX = e.touches[0].clientX;
    lastPanY = e.touches[0].clientY;
  }
});

canvas.addEventListener('touchend', e => {
  if (e.touches.length < 2) initialPinchDist = null;
  if (e.touches.length === 0) isPanning = false;
});

canvas.addEventListener('wheel', e => {
  e.preventDefault();
  if (e.deltaY < 0) zoomScale = Math.min(3.5, zoomScale + 0.2);
  else zoomScale = Math.max(0.8, zoomScale - 0.2);
  zoomLevelDisplay.innerText = `${zoomScale.toFixed(1)}x`;
});

function togglePause() {
  initAudio();
  simPaused = !simPaused;
  if (simPaused) {
    pauseBadge.innerText = 'SIM PAUSED';
    pauseBadge.className = 'status-badge status-paused';
  } else {
    pauseBadge.innerText = isBeerFriday ? 'BEER FRIDAY 🍺' : 'GATE 5 ACTIVE';
    pauseBadge.className = isBeerFriday ? 'status-badge status-party' : 'status-badge';
    playSFX('cheer');
  }
}

requestAnimationFrame(loop);
</script>

</body>
</html>
"""

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Upgraded Game Engine with Pinch-To-Zoom & Pan Engine!")
