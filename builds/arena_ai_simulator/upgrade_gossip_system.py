#!/usr/bin/env python3
"""
Hermes Game Studio: Secret News Spreading & Overtime Engine
Location on Phone: ~/projects/hermes_game_studio/builds/castlevania_stage1/upgrade_gossip_system.py
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
<title>Arena AI Simulator: Studio Life - Gossip & Overtime Edition</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
  body { background: #050508; color: #fff; font-family: 'Courier New', monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
  #game-container { position: relative; width: 100vw; max-width: 900px; display: flex; flex-direction: column; align-items: center; }
  canvas { background: #000; image-rendering: pixelated; image-rendering: crisp-edges; width: 100%; height: auto; aspect-ratio: 4 / 3; border: 4px solid #6820b0; box-shadow: 0 0 35px rgba(184, 120, 248, 0.7); touch-action: none; }
  
  #hud-bar { width: 100%; background: #12121c; border: 2px solid #333; display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; font-size: 10px; font-weight: bold; color: #ffcc00; }
  .status-badge { background: #006622; color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 9px; cursor: pointer; }
  .status-paused { background: #aa2200; animation: pulse 1s infinite; }
  .status-party { background: #e45c10; color: #fff; animation: party 0.5s infinite; }
  .status-gossip { background: #ff0077; color: #fff; animation: pulse 0.8s infinite; }
  .zoom-btn { background: #333; border: 1px solid #777; color: #fff; padding: 2px 8px; border-radius: 3px; cursor: pointer; margin-left: 4px; font-weight: bold; }
  
  @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
  @keyframes party { 0% { background: #e45c10; } 50% { background: #b878f8; } 100% { background: #e45c10; } }

  #instruction-tip { margin-top: 6px; font-size: 11px; color: #aaa; text-align: center; }
</style>
</head>
<body>

<div id="game-container">
  <div id="hud-bar">
    <div>🏛️ GRAND STUDIO CAMPUS (GOSSIP ENGINE)</div>
    <div>🤫 GOSSIP SPREAD: <span id="gossip-count" style="color:#ff0077;">2/10 Members</span></div>
    <div>🎵 BGM: <span id="bgm-status" style="color:#00ffff; cursor:pointer;" onclick="toggleBGM()">START 🔊</span></div>
    <div>STATUS: <span id="pause-badge" class="status-badge status-gossip" onclick="triggerWhisperSecret()">WHISPER SECRET 🤫</span></div>
  </div>

  <canvas id="canvas" width="400" height="300"></canvas>
  <div id="instruction-tip">🤫 <b>TAP "WHISPER SECRET" TO WHISPER OPENING PARTY NEWS TO ARIA & WATCH GOSSIP SPREAD!</b></div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const gossipCountDisplay = document.getElementById('gossip-count');
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
  } else if (type === 'whisper') {
    osc.type = 'sine';
    osc.frequency.setValueAtTime(800, now);
    osc.frequency.exponentialRampToValueAtTime(1200, now + 0.12);
    gain.gain.setValueAtTime(0.1, now);
    gain.gain.linearRampToValueAtTime(0.01, now + 0.12);
    osc.start(now);
    osc.stop(now + 0.12);
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

// Load Real PNG Image Assets directly
const officeImg = new Image();
officeImg.src = "assets/office_topdown_preview.png";

const spriteSheetImg = new Image();
spriteSheetImg.src = "assets/character_sprites_preview.png";

// State
let simPaused = false;
let isBeerFriday = false;
let isOvertime = false;
let simMinutes = 9 * 60; // 09:00 AM
let activeBubble = null;
let bubbleTimer = 0;
let stepFrame = 0;

// Secret News Gossip Tracking Engine
let secretInformed = new Set(['zillion', 'aria']); // Zillion whispered to Aria first!
const secretPhrases = {
  zillion: '(Psst... Aria, Boss is planning a massive Grand Opening Party!)',
  aria: '(Cody! Zillion told me Boss is throwing a Grand Opening Party!)',
  cody: '(Pixel! Did you hear?! Boss is throwing a Grand Opening Party!)',
  pixel: '(Echo, Jax! Boss is throwing a huge Opening Party!)',
  echo: '(Vortex! Grand Opening Party is happening!)',
  vortex: '(Jax, Marcus! Opening Party confirmed!)',
  jax: '(Vanguard! Boss is throwing a Grand Opening Party!)',
  marcus: '(Chronos! Opening party budget approved by Boss!)',
  vanguard: '(AAA Quality Opening Party Benchmark PASSED!)',
  chronos: '(Archived: 10/10 Members know about Boss Opening Party!)'
};

// Camera Pan State
let zoomScale = 1.0;
let camX = 200;
let camY = 150;
let isDragging = false;
let startDragX = 0;
let startDragY = 0;

// 10 Detailed Agents
const agents = [
  { id: 'zillion', name: 'Zillion', role: 'Tech Director', x: 220, y: 100, coat: '#222233', glasses: true },
  { id: 'marcus', name: 'Marcus', role: 'Producer', x: 100, y: 100, coat: '#ffffff', vest: '#843800' },
  { id: 'aria', name: 'Aria', role: 'Designer', x: 380, y: 120, hair: '#b878f8', coat: '#6820b0', headphones: true },
  { id: 'cody', name: 'Cody', role: 'Programmer', x: 460, y: 120, coat: '#00cc66', cap: true },
  { id: 'pixel', name: 'Pixel', role: 'Artist', x: 540, y: 120, coat: '#e45c10', beret: true },
  { id: 'echo', name: 'Echo', role: 'Audio', x: 620, y: 120, coat: '#442211', headset: true },
  { id: 'vortex', name: 'Vortex', role: 'Shader Dev', x: 460, y: 220, hair: '#00ffff', coat: '#113344' },
  { id: 'jax', name: 'Jax', role: 'QA Auditor', x: 540, y: 220, coat: '#005888', duck: true },
  { id: 'vanguard', name: 'Vanguard', role: 'AAA Judge', x: 620, y: 220, coat: '#22222b', suit: true },
  { id: 'chronos', name: 'Chronos', role: 'Memory Anchor', x: 700, y: 220, coat: '#554422' }
];

function triggerWhisperSecret() {
  initAudio();
  playSFX('whisper');
  secretInformed.add('aria');
  activeBubble = { agent: agents[0], text: secretPhrases['zillion'] };
  bubbleTimer = 200;
  gossipCountDisplay.innerText = `${secretInformed.size}/10 Members`;
}

function updateSimulation() {
  if (simPaused) return;
  stepFrame++;

  // Clock Progression
  simMinutes += 0.15;
  if (simMinutes >= 20 * 60) simMinutes = 8 * 60; // 08:00 AM to 08:00 PM (Overtime)

  const hrs = Math.floor(simMinutes / 60);
  const mins = Math.floor(simMinutes % 60);
  const ampm = hrs >= 12 ? 'PM' : 'AM';
  const displayHrs = hrs > 12 ? hrs - 12 : hrs;
  clockDisplay.innerText = `${String(displayHrs).padStart(2, '0')}:${String(mins).padStart(2, '0')} ${ampm}`;

  // Overtime Mode Check (> 17:00 PM)
  isOvertime = hrs >= 17;

  // Wander & Gossip Spreading AI Loop
  if (Math.random() < 0.03) {
    const talker = agents[Math.floor(Math.random() * agents.length)];
    
    // Proximity Gossip Spread
    for (let other of agents) {
      if (other.id !== talker.id && Math.hypot(talker.x - other.x, talker.y - other.y) < 60) {
        if (secretInformed.has(talker.id) && !secretInformed.has(other.id)) {
          secretInformed.add(other.id);
          activeBubble = { agent: talker, text: secretPhrases[talker.id] || '(Boss Opening Party is happening!)' };
          bubbleTimer = 180;
          playSFX('whisper');
          gossipCountDisplay.innerText = `${secretInformed.size}/10 Members`;
          if (secretInformed.size >= 10) playSFX('cheer');
          break;
        }
      }
    }

    // Move towards each other to spread gossip
    if (Math.random() < 0.4) {
      talker.x += (Math.random() - 0.5) * 40;
      talker.y += (Math.random() - 0.5) * 30;
    }
  }

  // Random Speech Bubbles
  if (bubbleTimer > 0) {
    bubbleTimer--;
  } else if (Math.random() < 0.012) {
    const talker = agents[Math.floor(Math.random() * agents.length)];
    const text = secretInformed.has(talker.id) 
      ? secretPhrases[talker.id] 
      : `${talker.name}: Working hard on the studio engine!`;
    activeBubble = { agent: talker, text: text };
    bubbleTimer = 150;
    playSFX('blip');
  }
}

function drawDetailedSprite(a) {
  const legOffset = (Math.floor(stepFrame / 8) % 2 === 0) ? 1 : -1;

  ctx.fillStyle = a.coat || '#333'; ctx.fillRect(a.x - 6, a.y - 5, 12, 12);
  if (a.vest) { ctx.fillStyle = a.vest; ctx.fillRect(a.x - 4, a.y - 5, 8, 11); }
  if (a.suit) { ctx.fillStyle = '#ffffff'; ctx.fillRect(a.x - 1, a.y - 5, 2, 10); }

  ctx.fillStyle = '#111118';
  ctx.fillRect(a.x - 5 + legOffset, a.y + 7, 4, 5);
  ctx.fillRect(a.x + 1 - legOffset, a.y + 7, 4, 5);

  ctx.fillStyle = '#fce0a8'; ctx.fillRect(a.x - 5, a.y - 13, 10, 8);
  ctx.fillStyle = a.hair || '#222'; ctx.fillRect(a.x - 6, a.y - 15, 12, 4);

  if (a.glasses) { ctx.fillStyle = '#ffffff'; ctx.fillRect(a.x - 4, a.y - 10, 3, 3); ctx.fillRect(a.x + 1, a.y - 10, 3, 3); }
  if (a.cap) { ctx.fillStyle = '#ee2211'; ctx.fillRect(a.x - 6, a.y - 16, 12, 4); ctx.fillRect(a.x - 9, a.y - 13, 4, 3); }
  if (a.beret) { ctx.fillStyle = '#e45c10'; ctx.fillRect(a.x - 7, a.y - 17, 14, 4); }
  if (a.headphones || a.headset) { ctx.fillStyle = '#00ffff'; ctx.fillRect(a.x - 8, a.y - 12, 3, 6); ctx.fillRect(a.x + 5, a.y - 12, 3, 6); }
  if (a.duck) { ctx.fillStyle = '#ffff00'; ctx.fillRect(a.x + 5, a.y - 4, 5, 5); ctx.fillStyle = '#ff6600'; ctx.fillRect(a.x + 9, a.y - 3, 2, 2); }

  // Secret Indicator (Gossip Icon over head)
  if (secretInformed.has(a.id)) {
    ctx.fillStyle = '#ff0077';
    ctx.font = 'bold 8px monospace';
    ctx.fillText('🤫', a.x - 4, a.y - 20);
  }

  // Name Label
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 8px monospace';
  ctx.shadowColor = '#000000'; ctx.shadowBlur = 4;
  ctx.fillText(a.name, a.x - (a.name.length * 2.2), a.y + 18);
  ctx.shadowBlur = 0;
}

function render() {
  ctx.fillStyle = '#0a0a10';
  ctx.fillRect(0, 0, 400, 300);

  ctx.save();
  ctx.translate(200 - camX, 150 - camY);

  // Background map with Overtime Sunset / Night Tinting
  ctx.fillStyle = '#181824'; ctx.fillRect(0, 0, 800, 580);
  ctx.fillStyle = isOvertime ? '#111122' : (isBeerFriday ? '#2a1a38' : '#222234');
  ctx.fillRect(10, 10, 780, 560);

  // Zones
  ctx.fillStyle = '#442211'; ctx.fillRect(20, 20, 220, 150); // Executive
  ctx.fillStyle = '#1c2238'; ctx.fillRect(260, 20, 510, 260); // Engineering
  ctx.fillStyle = '#381c1c'; ctx.fillRect(20, 310, 220, 240); // Gym
  ctx.fillStyle = isBeerFriday ? '#381c38' : '#1c3822'; ctx.fillRect(260, 310, 310, 240); // Lounge
  ctx.fillStyle = '#382a1c'; ctx.fillRect(590, 310, 180, 240); // Pantry

  // Desks & Overtime Lamps
  for (let i = 0; i < 10; i++) {
    let dx = 300 + (i % 5) * 85;
    let dy = i < 5 ? 70 : 170;
    ctx.fillStyle = '#553311'; ctx.fillRect(dx, dy, 55, 30);
    ctx.fillStyle = isOvertime ? '#ffaa00' : '#38b0de'; ctx.fillRect(dx + 12, dy + 4, 30, 12);
  }

  // Render Agents
  for (let a of agents) {
    drawDetailedSprite(a);
  }

  // Speech Bubbles
  if (bubbleTimer > 0 && activeBubble) {
    const ag = activeBubble.agent;
    const bx = Math.max(20, Math.min(630, ag.x - 55));
    const by = Math.max(30, ag.y - 48);

    ctx.fillStyle = '#ffffff'; ctx.fillRect(bx, by, 150, 28);
    ctx.strokeStyle = secretInformed.has(ag.id) ? '#ff0077' : '#000000'; ctx.lineWidth = 2; ctx.strokeRect(bx, by, 150, 28);
    ctx.fillRect(ag.x - 3, by + 27, 6, 5);

    ctx.fillStyle = secretInformed.has(ag.id) ? '#ff0077' : '#000000'; ctx.font = 'bold 8px monospace';
    ctx.fillText(`${ag.name} (Gossip 🤫):`, bx + 5, by + 10);
    ctx.fillStyle = '#000000'; ctx.font = '7px monospace';
    ctx.fillText(activeBubble.text.substring(0, 32), bx + 5, by + 22);
  }

  ctx.restore();

  // Overtime Banner Overlay
  if (isOvertime) {
    ctx.fillStyle = 'rgba(255, 100, 0, 0.15)';
    ctx.fillRect(0, 0, 400, 300);
  }
}

function loop() {
  updateSimulation();
  render();
  requestAnimationFrame(loop);
}

// Touch Drag Navigation
canvas.addEventListener('touchstart', e => {
  initAudio();
  if (e.touches.length === 1) {
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
      if (Math.abs(clickX - a.x) < 25 && Math.abs(clickY - a.y) < 25) {
        touchedAgent = a;
        break;
      }
    }

    if (touchedAgent) {
      const text = secretInformed.has(touchedAgent.id) 
        ? secretPhrases[touchedAgent.id] 
        : `BOSS touched ${touchedAgent.name}! Working hard on studio engine!`;
      activeBubble = { agent: touchedAgent, text: text };
      bubbleTimer = 180;
      playSFX(secretInformed.has(touchedAgent.id) ? 'whisper' : 'cheer');
      return;
    }
  }
});

canvas.addEventListener('touchmove', e => {
  e.preventDefault();
  if (isDragging && e.touches.length === 1) {
    const dx = e.touches[0].clientX - startDragX;
    const dy = e.touches[0].clientY - startDragY;
    camX = Math.max(200, Math.min(600, camX - dx * 0.8));
    camY = Math.max(150, Math.min(430, camY - dy * 0.8));
    startDragX = e.touches[0].clientX;
    startDragY = e.touches[0].clientY;
  }
});

canvas.addEventListener('touchend', () => { isDragging = false; });

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

requestAnimationFrame(loop);
</script>

</body>
</html>
"""

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Upgraded Game Engine with Gossip Spreading Engine & Overtime Mode!")
