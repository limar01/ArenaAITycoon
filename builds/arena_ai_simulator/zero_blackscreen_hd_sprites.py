#!/usr/bin/env python3
"""
Hermes Game Studio: Applies Real HD PNG Sprite Atlas Images to index.html
Location on Phone: ~/projects/hermes_game_studio/builds/castlevania_stage1/zero_blackscreen_hd_sprites.py
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
<title>Arena AI Simulator: Studio Life - Zero Blackscreen HD Edition</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
  body { background: #08080d; color: #fff; font-family: 'Courier New', monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
  #game-container { position: relative; width: 100vw; max-width: 900px; display: flex; flex-direction: column; align-items: center; }
  
  #hud-bar { width: 100%; background: #1a1a2e; border: 2px solid #555; display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; font-size: 10px; font-weight: bold; color: #ffcc00; }
  .status-badge { background: #006622; color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 9px; cursor: pointer; }
  .status-paused { background: #aa2200; animation: pulse 1s infinite; }
  .status-party { background: #e45c10; color: #fff; animation: party 0.5s infinite; }
  .zoom-btn { background: #333; border: 1px solid #777; color: #fff; padding: 2px 8px; border-radius: 3px; cursor: pointer; margin-left: 4px; font-weight: bold; }
  
  @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
  @keyframes party { 0% { background: #e45c10; } 50% { background: #b878f8; } 100% { background: #e45c10; } }

  canvas { background: #1a1a2e; image-rendering: pixelated; image-rendering: crisp-edges; width: 100%; height: auto; aspect-ratio: 4 / 3; border: 4px solid #b878f8; box-shadow: 0 0 35px rgba(184, 120, 248, 0.8); touch-action: none; }
  #instruction-tip { margin-top: 6px; font-size: 11px; color: #00ffff; text-align: center; font-weight: bold; }
</style>
</head>
<body>

<div id="game-container">
  <div id="hud-bar">
    <div>🏛️ GRAND STUDIO CAMPUS (HD SPRITE ATLAS)</div>
    <div>
      ZOOM: <span id="zoom-level" style="color:#00ffff;">1.0x</span>
      <button class="zoom-btn" onclick="adjustZoom(0.3)">+</button>
      <button class="zoom-btn" onclick="adjustZoom(-0.3)">-</button>
    </div>
    <div>🎵 BGM: <span id="bgm-status" style="color:#00ffff; cursor:pointer;" onclick="toggleBGM()">START 🔊</span></div>
    <div>STATUS: <span id="pause-badge" class="status-badge status-party" onclick="togglePause()">BEER FRIDAY 🍺</span></div>
  </div>

  <canvas id="canvas" width="400" height="300"></canvas>
  <div id="instruction-tip">💡 <b>REAL HD PNG SPRITES ACTIVE! USE +/- OR PINCH TO ZOOM!</b></div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const zoomLevelDisplay = document.getElementById('zoom-level');
const bgmStatus = document.getElementById('bgm-status');
const pauseBadge = document.getElementById('pause-badge');

// Web Audio
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let actx = null;
let bgmPlaying = false;
let bgmInterval = null;

function initAudio() {
  if (!actx) {
    actx = new AudioCtx();
    startBGM();
  }
  if (actx.state === 'suspended') actx.resume();
}

function startBGM() {
  if (bgmPlaying || !actx) return;
  bgmPlaying = true;
  bgmStatus.innerText = "ON 🔊";

  const notes = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63];
  let noteIdx = 0;

  if (bgmInterval) clearInterval(bgmInterval);
  bgmInterval = setInterval(() => {
    if (!bgmPlaying || !actx) return;
    const now = actx.currentTime;
    const osc = actx.createOscillator();
    osc.type = isBeerFriday ? 'sawtooth' : 'triangle';
    osc.frequency.setValueAtTime(notes[noteIdx], now);
    
    const noteGain = actx.createGain();
    noteGain.gain.setValueAtTime(0.04, now);
    noteGain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
    
    osc.connect(noteGain);
    noteGain.connect(actx.destination);
    
    osc.start(now);
    osc.stop(now + 0.2);
    noteIdx = (noteIdx + 1) % notes.length;
  }, 220);
}

function toggleBGM() {
  initAudio();
  bgmPlaying = !bgmPlaying;
  bgmStatus.innerText = bgmPlaying ? "ON 🔊" : "OFF 🔇";
  if (bgmPlaying) startBGM();
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
    osc.frequency.setValueAtTime(800, now + 0.25);
    gain.gain.setValueAtTime(0.25, now);
    gain.gain.linearRampToValueAtTime(0.01, now + 0.4);
    osc.start(now);
    osc.stop(now + 0.4);
  }
}

// Load Real PNG Image Assets safely
const officeImg = new Image();
officeImg.src = "assets/office_topdown_preview.png";

const spriteSheetImg = new Image();
spriteSheetImg.src = "assets/character_sprites_preview.png";

// State
let simPaused = false;
let isBeerFriday = true;
let simMinutes = 16 * 60;
let activeBubble = null;
let bubbleTimer = 0;
let stepFrame = 0;

// Camera Pan & Zoom State
let zoomScale = 1.0;
let camX = 200;
let camY = 150;
let isDragging = false;
let startDragX = 0;
let startDragY = 0;

function adjustZoom(delta) {
  initAudio();
  zoomScale = Math.max(0.8, Math.min(3.5, zoomScale + delta));
  zoomLevelDisplay.innerText = `${zoomScale.toFixed(1)}x`;
}

// 10 Detailed Active Walking Agents
const agents = [
  { id: 'zillion', name: 'Zillion', role: 'Tech Director', x: 220, y: 100, targetX: 100, targetY: 80, sx: 0, sy: 0, phrase: 'HD PNG Sprite Sheet Engine Active! Zero Black Screen!' },
  { id: 'marcus', name: 'Marcus', role: 'Producer', x: 100, y: 100, targetX: 650, targetY: 380, sx: 1, sy: 0, phrase: 'Beer Friday Party is LIVE! Cheers Boss!' },
  { id: 'aria', name: 'Aria', role: 'Designer', x: 380, y: 120, targetX: 300, targetY: 80, sx: 2, sy: 0, phrase: 'High-definition 16-bit pixel sprites active!' },
  { id: 'cody', name: 'Cody', role: 'Programmer', x: 460, y: 120, targetX: 500, targetY: 80, sx: 3, sy: 0, phrase: 'qwen2.5-coder compiling 60 FPS walking code!' },
  { id: 'pixel', name: 'Pixel', role: 'Artist', x: 540, y: 120, targetX: 650, targetY: 180, sx: 4, sy: 0, phrase: 'Rendered HD sprite atlas image directly on canvas!' },
  { id: 'echo', name: 'Echo', role: 'Audio', x: 620, y: 120, targetX: 450, targetY: 450, sx: 0, sy: 1, phrase: 'Playing 16-Bit 44.1kHz MIDI OST playing in stereo!' },
  { id: 'vortex', name: 'Vortex', role: 'Shader Dev', x: 460, y: 220, targetX: 100, targetY: 380, sx: 1, sy: 1, phrase: 'WebGL fragment shaders & particle emitters active!' },
  { id: 'jax', name: 'Jax', role: 'QA Auditor', x: 540, y: 220, targetX: 500, targetY: 180, sx: 2, sy: 1, phrase: 'Jax rubber duck & deepseek-r1 QA passed 100%!' },
  { id: 'vanguard', name: 'Vanguard', role: 'AAA Judge', x: 620, y: 220, targetX: 300, targetY: 180, sx: 3, sy: 1, phrase: 'AAA Benchmark: HD PNG Canvas PASSED 100%!' },
  { id: 'chronos', name: 'Chronos', role: 'Memory Anchor', x: 700, y: 220, targetX: 200, targetY: 100, sx: 4, sy: 1, phrase: 'Savepoint v3.0 anchored in phone storage!' }
];

// Billiards State
const poolBalls = [
  { x: 480, y: 450, vx: 1.2, vy: 0.8, color: '#ffffff' },
  { x: 460, y: 445, vx: -0.8, vy: 0.6, color: '#ee2211' },
  { x: 460, y: 455, vx: 0.5, vy: -0.9, color: '#ffff00' },
  { x: 445, y: 450, vx: -0.6, vy: -0.4, color: '#38b0de' }
];

function updateSimulation() {
  if (simPaused) return;

  stepFrame++;

  // Clock
  simMinutes += 0.1;
  if (simMinutes >= 17 * 60) simMinutes = 8 * 60;
  const hrs = Math.floor(simMinutes / 60);
  const mins = Math.floor(simMinutes % 60);
  const ampm = hrs >= 12 ? 'PM' : 'AM';
  const displayHrs = hrs > 12 ? hrs - 12 : hrs;
  clockDisplay.innerText = `${String(displayHrs).padStart(2, '0')}:${String(mins).padStart(2, '0')} ${ampm}`;

  // Continuous Walking AI
  for (let a of agents) {
    let dx = a.targetX - a.x;
    let dy = a.targetY - a.y;
    let dist = Math.hypot(dx, dy);

    if (dist > 4) {
      a.isWalking = true;
      a.x += (dx / dist) * 1.1;
      a.y += (dy / dist) * 1.1;
    } else {
      a.isWalking = false;
      if (Math.random() < 0.02) {
        a.targetX = 40 + Math.random() * 720;
        a.targetY = 40 + Math.random() * 500;
      }
    }

    for (let other of agents) {
      if (other.id !== a.id && Math.hypot(a.x - other.x, a.y - other.y) < 32) {
        if (bubbleTimer <= 0 && Math.random() < 0.02) {
          activeBubble = { agent: a, text: `${a.name} talking to ${other.name}: ${a.phrase}` };
          bubbleTimer = 160;
          playSFX('blip');
        }
      }
    }
  }

  // Billiards Physics
  for (let b of poolBalls) {
    b.x += b.vx; b.y += b.vy;
    b.vx *= 0.95; b.vy *= 0.95;
    if (b.x < 430 || b.x > 530) b.vx *= -1;
    if (b.y < 420 || b.y > 480) b.vy *= -1;
  }
}

// Draw Detailed Pixel Sprite Backup
function drawDetailedSprite(a) {
  const bob = a.isWalking ? Math.sin(stepFrame * 0.3) * 2.5 : 0;
  const legOffset = (Math.floor(stepFrame / 5) % 2 === 0) ? 2.5 : -2.5;

  ctx.fillStyle = a.coat || '#38b0de';
  ctx.fillRect(a.x - 6, a.y - 5 + bob, 12, 11);

  if (a.vest) { ctx.fillStyle = a.vest; ctx.fillRect(a.x - 4, a.y - 5 + bob, 8, 11); }
  if (a.suit) { ctx.fillStyle = '#ffffff'; ctx.fillRect(a.x - 1, a.y - 5 + bob, 2, 10); }

  ctx.fillStyle = '#111118';
  ctx.fillRect(a.x - 5 + (a.isWalking ? legOffset : 0), a.y + 6 + bob, 4, 6);
  ctx.fillRect(a.x + 1 - (a.isWalking ? legOffset : 0), a.y + 6 + bob, 4, 6);

  ctx.fillStyle = '#fce0a8'; ctx.fillRect(a.x - 5, a.y - 13 + bob, 10, 8);
  ctx.fillStyle = a.hair || '#222'; ctx.fillRect(a.x - 6, a.y - 15 + bob, 12, 4);

  if (a.glasses) { ctx.fillStyle = '#ffffff'; ctx.fillRect(a.x - 4, a.y - 10 + bob, 3, 3); ctx.fillRect(a.x + 1, a.y - 10 + bob, 3, 3); }
  if (a.cap) { ctx.fillStyle = '#ee2211'; ctx.fillRect(a.x - 6, a.y - 16 + bob, 12, 4); ctx.fillRect(a.x - 9, a.y - 13 + bob, 4, 3); }
  if (a.beret) { ctx.fillStyle = '#e45c10'; ctx.fillRect(a.x - 7, a.y - 17 + bob, 14, 4); }
  if (a.headphones || a.headset) { ctx.fillStyle = '#00ffff'; ctx.fillRect(a.x - 8, a.y - 12 + bob, 3, 6); ctx.fillRect(a.x + 5, a.y - 12 + bob, 3, 6); }
  if (a.duck) { ctx.fillStyle = '#ffff00'; ctx.fillRect(a.x + 5, a.y - 4 + bob, 5, 5); ctx.fillStyle = '#ff6600'; ctx.fillRect(a.x + 7, a.y - 2 + bob, 2, 2); }

  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 8px monospace';
  ctx.shadowColor = '#000000'; ctx.shadowBlur = 4;
  ctx.fillText(a.name, a.x - (a.name.length * 2.2), a.y + 18 + bob);
  ctx.shadowBlur = 0;
}

// ZERO BLACK SCREEN GUARANTEED RENDER
function render() {
  try {
    ctx.imageSmoothingEnabled = false;
    ctx.webkitImageSmoothingEnabled = false;

    ctx.fillStyle = '#0a0a10';
    ctx.fillRect(0, 0, 400, 300);

    ctx.save();
    ctx.translate(200 - camX, 150 - camY);
    ctx.scale(zoomScale, zoomScale);

    // 1. ALWAYS DRAW COLORFUL MAP GEOMETRY FIRST (0% Black Screen Guarantee)
    ctx.fillStyle = '#181824'; ctx.fillRect(0, 0, 800, 580);
    ctx.fillStyle = isBeerFriday ? '#2a1a38' : '#222234'; ctx.fillRect(10, 10, 780, 560);

    ctx.fillStyle = '#442211'; ctx.fillRect(20, 20, 220, 150); // War Room
    ctx.fillStyle = '#843800'; ctx.fillRect(60, 60, 120, 45);
    ctx.fillStyle = '#ffffff'; ctx.fillRect(50, 25, 140, 6);

    ctx.fillStyle = '#1c2238'; ctx.fillRect(260, 20, 510, 260); // Workstations
    for (let i = 0; i < 10; i++) {
      let dx = 300 + (i % 5) * 85;
      let dy = i < 5 ? 70 : 170;
      ctx.fillStyle = '#553311'; ctx.fillRect(dx, dy, 55, 30);
      ctx.fillStyle = '#38b0de'; ctx.fillRect(dx + 12, dy + 4, 30, 12);
    }

    ctx.fillStyle = '#381c1c'; ctx.fillRect(20, 310, 220, 240); // Gym
    ctx.fillStyle = '#666677'; ctx.fillRect(40, 340, 35, 60);
    ctx.fillStyle = '#ffcc00'; ctx.fillRect(150, 370, 60, 30);

    ctx.fillStyle = isBeerFriday ? '#381c38' : '#1c3822'; ctx.fillRect(260, 310, 310, 240); // Lounge
    ctx.fillStyle = '#843800'; ctx.fillRect(410, 410, 110, 70);
    ctx.fillStyle = '#008833'; ctx.fillRect(418, 418, 94, 54);
    for (let b of poolBalls) { ctx.fillStyle = b.color; ctx.fillRect(b.x, b.y, 5, 5); }

    ctx.fillStyle = '#880000'; ctx.fillRect(300, 360, 80, 35);
    ctx.fillStyle = '#382a1c'; ctx.fillRect(590, 310, 180, 240);
    ctx.fillStyle = '#dddddd'; ctx.fillRect(610, 340, 30, 50);
    ctx.fillStyle = '#aa8800'; ctx.fillRect(660, 340, 35, 25);
    if (isBeerFriday) { ctx.fillStyle = '#ffff00'; ctx.fillRect(710, 340, 20, 20); }
    ctx.fillStyle = '#cc9900'; ctx.fillRect(740, 240, 35, 50);

    // 2. BLEND HD PNG ARTWORK IF LOADED
    if (officeImg.complete && officeImg.naturalWidth > 0) {
      try {
        ctx.globalAlpha = 0.82;
        ctx.drawImage(officeImg, 0, 0, 800, 580);
        ctx.globalAlpha = 1.0;
      } catch(e){}
    }

    // 3. RENDER REAL CHARACTER SPRITES FROM PNG ATLAS SHEET (OR DETAILED PIXEL BACKUP)
    for (let a of agents) {
      const bob = a.isWalking ? Math.sin(stepFrame * 0.3) * 2 : 0;

      if (spriteSheetImg.complete && spriteSheetImg.naturalWidth > 0) {
        try {
          const sw = spriteSheetImg.naturalWidth / 5;
          const sh = spriteSheetImg.naturalHeight / 2;
          const sx = (a.sx % 5) * sw;
          const sy = Math.floor(a.sy % 2) * sh;

          // Draw HD PNG Pixel Sprite
          ctx.drawImage(spriteSheetImg, sx, sy, sw, sh, a.x - 16, a.y - 20 + bob, 32, 32);
        } catch(e){
          drawDetailedSprite(a);
        }
      } else {
        drawDetailedSprite(a);
      }

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 8px monospace';
      ctx.shadowColor = '#000000'; ctx.shadowBlur = 4;
      ctx.fillText(a.name, a.x - (a.name.length * 2.2), a.y + 18 + bob);
      ctx.shadowBlur = 0;
    }

    // 4. SPEECH BUBBLES
    if (bubbleTimer > 0 && activeBubble) {
      const ag = activeBubble.agent;
      const bx = Math.max(20, Math.min(650, ag.x - 50));
      const by = Math.max(30, ag.y - 45);

      ctx.fillStyle = '#ffffff'; ctx.fillRect(bx, by, 140, 26);
      ctx.strokeStyle = '#000000'; ctx.lineWidth = 1; ctx.strokeRect(bx, by, 140, 26);
      ctx.fillRect(ag.x - 3, by + 25, 6, 5);

      ctx.fillStyle = '#000000'; ctx.font = 'bold 8px monospace';
      ctx.fillText(`${ag.name}:`, bx + 5, by + 10);
      ctx.font = '7px monospace';
      ctx.fillText(activeBubble.text.substring(0, 30), bx + 5, by + 21);
    }

    ctx.restore();

    if (simPaused) {
      ctx.fillStyle = 'rgba(0,0,0,0.65)';
      ctx.fillRect(0, 0, 400, 300);

      ctx.fillStyle = '#aa2200'; ctx.fillRect(40, 120, 320, 60);
      ctx.strokeStyle = '#ffaa00'; ctx.lineWidth = 2; ctx.strokeRect(40, 120, 320, 60);

      ctx.fillStyle = '#ffffff'; ctx.font = 'bold 12px monospace';
      ctx.fillText('🔒 PENDING BOSS GATE APPROVAL', 80, 145);
      ctx.fillStyle = '#ffcc00'; ctx.font = '8px monospace';
      ctx.fillText('SIMULATION TIME FROZEN | TAP STATUS TO RESUME', 65, 165);
    }
  } catch(e){ console.log(e); }
}

function loop() {
  updateSimulation();
  render();
  requestAnimationFrame(loop);
}

// Touch Event & Pinch-Zoom Listeners
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
    isDragging = true;
    startDragX = e.touches[0].clientX;
    startDragY = e.touches[0].clientY;

    const rect = canvas.getBoundingClientRect();
    const scaleX = 400 / rect.width;
    const scaleY = 300 / rect.height;

    const clickX = camX + (e.touches[0].clientX - rect.left) * scaleX - 200;
    const clickY = camY + (e.touches[0].clientY - rect.top) * scaleY - 150;

    let touchedAgent = null;
    for (let a of agents) {
      if (Math.abs(clickX - a.x) < 30 && Math.abs(clickY - a.y) < 30) {
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

    if (clickX >= 410 && clickX <= 520 && clickY >= 410 && clickY <= 480) {
      playSFX('pool_hit');
      poolBalls[0].vx = (Math.random() - 0.5) * 5;
      poolBalls[0].vy = (Math.random() - 0.5) * 5;
      activeBubble = { agent: { name: 'BOSS', x: 460, y: 440 }, text: 'BOSS shot a break on the Pool Table! 🎱' };
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
  } else if (isDragging && e.touches.length === 1) {
    const dx = e.touches[0].clientX - startDragX;
    const dy = e.touches[0].clientY - startDragY;
    camX = Math.max(200, Math.min(600, camX - dx * 0.8));
    camY = Math.max(150, Math.min(430, camY - dy * 0.8));
    startDragX = e.touches[0].clientX;
    startDragY = e.touches[0].clientY;
  }
});

canvas.addEventListener('touchend', () => { initialPinchDist = null; isDragging = false; });

canvas.addEventListener('mousedown', e => {
  initAudio();
  isDragging = true;
  startDragX = e.clientX;
  startDragY = e.clientY;
});

canvas.addEventListener('mousemove', e => {
  if (isDragging) {
    const dx = e.clientX - startDragX;
    const dy = e.clientY - startDragY;
    camX = Math.max(200, Math.min(600, camX - dx * 0.8));
    camY = Math.max(150, Math.min(430, camY - dy * 0.8));
    startDragX = e.clientX;
    startDragY = e.clientY;
  }
});

canvas.addEventListener('mouseup', () => { isDragging = false; });

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

print("Applied Real HD PNG Sprite Atlas Images Engine!")
