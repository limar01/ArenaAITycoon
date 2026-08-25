#!/usr/bin/env python3
"""
Hermes Game Studio: Inner Mind Thought Reader & Personality Traits Engine
Location on Phone: ~/projects/hermes_game_studio/builds/castlevania_stage1/upgrade_inner_mind.py
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
<title>Arena AI Simulator: Studio Life - Inner Mind Reader</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
  body { background: #050508; color: #fff; font-family: 'Courier New', monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
  #game-container { position: relative; width: 100vw; max-width: 900px; display: flex; flex-direction: column; align-items: center; }
  canvas { background: #000; image-rendering: pixelated; image-rendering: crisp-edges; width: 100%; height: auto; aspect-ratio: 4 / 3; border: 4px solid #6820b0; box-shadow: 0 0 35px rgba(184, 120, 248, 0.7); touch-action: none; }
  
  #hud-bar { width: 100%; background: #12121c; border: 2px solid #333; display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; font-size: 10px; font-weight: bold; color: #ffcc00; }
  .status-badge { background: #006622; color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 9px; cursor: pointer; }
  .status-mind { background: #6820b0; color: #fff; animation: pulse 1.2s infinite; }
  
  @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }

  #instruction-tip { margin-top: 6px; font-size: 11px; color: #aaa; text-align: center; }
</style>
</head>
<body>

<div id="game-container">
  <div id="hud-bar">
    <div>🏛️ GRAND STUDIO (INNER MIND READER)</div>
    <div>🧠 VIEW MODE: <span id="view-mode-label" style="color:#00ffff; cursor:pointer;" onclick="toggleViewMode()">💬 SPEECH BUBBLES</span></div>
    <div>🎵 BGM: <span id="bgm-status" style="color:#00ffff; cursor:pointer;" onclick="toggleBGM()">START 🔊</span></div>
  </div>

  <canvas id="canvas" width="400" height="300"></canvas>
  <div id="instruction-tip">🧠 <b>TAP ANY AGENT TO READ THEIR INNER THOUGHTS, CRUSHES, & EMOTIONS!</b></div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const viewModeLabel = document.getElementById('view-mode-label');
const bgmStatus = document.getElementById('bgm-status');

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
    osc.type = 'triangle';
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

  if (type === 'mind') {
    osc.type = 'sine';
    osc.frequency.setValueAtTime(600, now);
    osc.frequency.exponentialRampToValueAtTime(1400, now + 0.15);
    gain.gain.setValueAtTime(0.15, now);
    gain.gain.linearRampToValueAtTime(0.01, now + 0.15);
    osc.start(now);
    osc.stop(now + 0.15);
  } else if (type === 'blip') {
    osc.type = 'square';
    osc.frequency.setValueAtTime(520, now);
    osc.frequency.setValueAtTime(680, now + 0.04);
    gain.gain.setValueAtTime(0.15, now);
    gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
    osc.start(now);
    osc.stop(now + 0.08);
  }
}

// Load PNG Images
const officeImg = new Image();
officeImg.src = "assets/office_topdown_preview.png";

const spriteSheetImg = new Image();
spriteSheetImg.src = "assets/character_sprites_preview.png";

// Modes: 'speech' or 'thought'
let viewMode = 'thought'; 
let simPaused = false;
let simMinutes = 10 * 60;
let activeBubble = null;
let bubbleTimer = 0;
let stepFrame = 0;

// 10 Detailed Agents with Personality Traits, Hobbies, Crushes & Inner Thoughts
const agents = [
  { id: 'zillion', name: 'Zillion', role: 'Tech Director', x: 220, y: 100, coat: '#222233', glasses: true, 
    speech: 'Boss approved Gate 3! Gate 4 Core Engine is LIVE!',
    thought: '🧠 THOUGHT: Boss vision is 100x ahead of Silicon Valley! I must protect this team.' },
  { id: 'marcus', name: 'Marcus', role: 'Producer', x: 100, y: 100, coat: '#ffffff', vest: '#843800',
    speech: 'Milestone on track! Beer Friday is at 04:00 PM!',
    thought: '🧠 THOUGHT: If we hit Gate 6, I am buying draft beers and pizza for everyone!' },
  { id: 'aria', name: 'Aria', role: 'Designer', x: 380, y: 120, hair: '#b878f8', coat: '#6820b0', headphones: true,
    speech: 'Designing level tilemaps & narrative dialogue trees!',
    thought: '🧠 THOUGHT (CRUSH 💕): Echo guitar solos are so romantic... Hope he plays my favorite song!' },
  { id: 'cody', name: 'Cody', role: 'Programmer', x: 460, y: 120, coat: '#00cc66', cap: true,
    speech: 'Compiling 60FPS Phaser 3 WebGL multi-scene code!',
    thought: '🧠 THOUGHT (CRUSH 💕): Pixel looks so cute in her beret today... I hope she likes my RGB desk code!' },
  { id: 'pixel', name: 'Pixel', role: 'Artist', x: 540, y: 120, coat: '#e45c10', beret: true,
    speech: 'Drawing crisp 16-bit character sprite atlases!',
    thought: '🧠 THOUGHT (CRUSH 💕): Cody gets so flustered when I ask for code help! I should draw him a cap sticker!' },
  { id: 'echo', name: 'Echo', role: 'Audio', x: 620, y: 120, coat: '#442211', headset: true,
    speech: 'Synthesizing 16-Bit 44.1kHz Retro MIDI Party OST!',
    thought: '🧠 THOUGHT: Composing a special 16-bit acoustic track for Boss Opening Party!' },
  { id: 'vortex', name: 'Vortex', role: 'Shader Dev', x: 460, y: 220, hair: '#00ffff', coat: '#113344',
    speech: 'WebGL particle emitters & dynamic light shaders!',
    thought: '🧠 THOUGHT: I will unleash neon particle fireworks during Boss Grand Opening Party!' },
  { id: 'jax', name: 'Jax', role: 'QA Auditor', x: 540, y: 220, coat: '#005888', duck: true,
    speech: 'Squeak! Yellow rubber duck passed 10 QA tests!',
    thought: '🧠 THOUGHT: Hehe, I am going to tease Cody about Pixel at lunch break today!' },
  { id: 'vanguard', name: 'Vanguard', role: 'AAA Judge', x: 620, y: 220, coat: '#22222b', suit: true,
    speech: 'AAA Benchmark: Commercial Indie Standard 100%!',
    thought: '🧠 THOUGHT: Quality is impressive. Stardew Valley & Celeste tier benchmarks achieved.' },
  { id: 'chronos', name: 'Chronos', role: 'Memory Anchor', x: 700, y: 220, coat: '#554422',
    speech: 'Context anchored! Zero hallucinations logged.',
    thought: '🧠 THOUGHT: All 10 members feelings, crushes, and news logged in memory archives.' }
];

// Camera Pan
let camX = 200;
let camY = 150;
let isDragging = false;
let startDragX = 0;
let startDragY = 0;

function toggleViewMode() {
  initAudio();
  playSFX('mind');
  viewMode = (viewMode === 'speech') ? 'thought' : 'speech';
  viewModeLabel.innerText = (viewMode === 'speech') ? '💬 SPEECH BUBBLES' : '🧠 INNER THOUGHTS';
  viewModeLabel.style.color = (viewMode === 'speech') ? '#00ffff' : '#b878f8';
}

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

  // Wander AI
  if (Math.random() < 0.02) {
    const talker = agents[Math.floor(Math.random() * agents.length)];
    talker.x = 220 + (agents.indexOf(talker) % 5) * 80;
    talker.y = agents.indexOf(talker) < 5 ? 120 : 220;
  }

  // Random Thought/Speech Bubbles
  if (bubbleTimer > 0) {
    bubbleTimer--;
  } else if (Math.random() < 0.018) {
    const talker = agents[Math.floor(Math.random() * agents.length)];
    const text = (viewMode === 'thought') ? talker.thought : talker.speech;
    activeBubble = { agent: talker, text: text, mode: viewMode };
    bubbleTimer = 160;
    playSFX(viewMode === 'thought' ? 'mind' : 'blip');
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

  // Heart Icon over Cody/Pixel/Aria for Crush mechanics!
  if (a.id === 'cody' || a.id === 'pixel' || a.id === 'aria') {
    ctx.fillStyle = '#ff0055';
    ctx.font = 'bold 8px monospace';
    ctx.fillText('💕', a.x - 4, a.y - 19);
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

  if (officeImg.complete && officeImg.naturalWidth > 0) {
    ctx.drawImage(officeImg, 0, 0, 800, 580);
  } else {
    ctx.fillStyle = '#181824'; ctx.fillRect(0, 0, 800, 580);
    ctx.fillStyle = '#222234'; ctx.fillRect(10, 10, 780, 560);
  }

  // Render Agents
  for (let a of agents) {
    drawDetailedSprite(a);
  }

  // Speech / Thought Bubbles
  if (bubbleTimer > 0 && activeBubble) {
    const ag = activeBubble.agent;
    const isThought = activeBubble.mode === 'thought';
    const bx = Math.max(20, Math.min(620, ag.x - 60));
    const by = Math.max(30, ag.y - 50);

    ctx.fillStyle = isThought ? '#f5e8ff' : '#ffffff';
    ctx.fillRect(bx, by, 160, 30);
    ctx.strokeStyle = isThought ? '#b878f8' : '#000000';
    ctx.lineWidth = 2;
    ctx.strokeRect(bx, by, 160, 30);

    // Thought Cloud Circles
    if (isThought) {
      ctx.fillStyle = '#f5e8ff';
      ctx.beginPath(); ctx.arc(ag.x, by + 32, 3, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(ag.x + 4, by + 36, 2, 0, Math.PI * 2); ctx.fill();
    } else {
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(ag.x - 3, by + 29, 6, 5);
    }

    ctx.fillStyle = isThought ? '#6820b0' : '#000000';
    ctx.font = 'bold 8px monospace';
    ctx.fillText(`${ag.name} ${isThought ? '(INNER MIND 🧠)' : '(SPEECH 💬)'}:`, bx + 5, by + 10);
    ctx.fillStyle = '#111118';
    ctx.font = '7px monospace';
    ctx.fillText(activeBubble.text.substring(0, 34), bx + 5, by + 22);
  }

  ctx.restore();
}

function loop() {
  updateSimulation();
  render();
  requestAnimationFrame(loop);
}

// Touch Interaction
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
      const text = (viewMode === 'thought') ? touchedAgent.thought : touchedAgent.speech;
      activeBubble = { agent: touchedAgent, text: text, mode: viewMode };
      bubbleTimer = 190;
      playSFX(viewMode === 'thought' ? 'mind' : 'blip');
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

print("Upgraded Game Engine with Inner Mind Reader & Personality Crushes Engine!")
