import json
import base64
import os
from PIL import Image
import numpy as np
import io

SPRITES_DIR = os.path.expanduser('~/sprites')
BASE = os.path.expanduser('~/projects/hermes_game_studio/builds/castlevania_stage1')

img_chars = Image.open(os.path.join(SPRITES_DIR, 'character_sprites_preview.png')).convert('RGB')
arr = np.array(img_chars)
bg = np.median(arr[:30, :30], axis=(0,1))
W, H = img_chars.size
char_grid = [
    ['zillion', 'marcus', 'aria', 'cody', 'pixel'],
    ['echo', 'vortex', 'jax', 'vanguard', 'chronos']
]

assets = {}

for r in range(2):
    for c in range(5):
        name = char_grid[r][c]
        x1 = int(c * W / 5)
        x2 = int((c + 1) * W / 5)
        y1 = int(r * H / 2)
        y2 = int((r + 1) * H / 2) - 55
        
        cell = arr[y1:y2, x1:x2].copy()
        dist = np.linalg.norm(cell - bg, axis=2)
        mask = dist > 20
        mask[:5, :] = False; mask[-5:, :] = False; mask[:, :5] = False; mask[:, -5:] = False
        
        row_counts = mask.sum(axis=1)
        col_counts = mask.sum(axis=0)
        
        min_r = np.where(row_counts > 4)[0][0]
        max_r = np.where(row_counts > 4)[0][-1]
        min_c = np.where(col_counts > 4)[0][0]
        max_c = np.where(col_counts > 4)[0][-1]
        
        rgba = np.zeros((cell.shape[0], cell.shape[1], 4), dtype=np.uint8)
        rgba[:, :, :3] = cell
        rgba[:, :, 3] = np.where(mask, 255, 0)
        cropped = rgba[min_r:max_r+1, min_c:max_c+1]
        
        head_h = int(cropped.shape[0] * 0.45)
        head_crop = cropped[:head_h, :]
        
        buf = io.BytesIO()
        Image.fromarray(cropped).save(buf, format='PNG')
        assets[name] = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')
        
        buf_h = io.BytesIO()
        Image.fromarray(head_crop).save(buf_h, format='PNG')
        assets[name + '_head'] = 'data:image/png;base64,' + base64.b64encode(buf_h.getvalue()).decode('ascii')

with open(os.path.join(SPRITES_DIR, 'office_topdown_preview.png'), 'rb') as f:
    assets['office_bg'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>DEV STUDIO SIM - HD Edition</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
  body {
    background: #06060c;
    color: #fff;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow-x: hidden;
    padding: 6px;
  }
  
  #game-wrapper {
    width: 100%;
    max-width: 960px;
    background: #11111d;
    border: 3px solid #3d3d66;
    border-radius: 10px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.8), 0 0 20px rgba(184, 120, 248, 0.2);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  /* Retro Top Header */
  #retro-header {
    background: #181828;
    border-bottom: 2px solid #3d3d66;
    padding: 6px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    font-weight: bold;
    color: #e0e0ff;
    flex-wrap: wrap;
    gap: 8px;
  }
  .stat-badge { color: #ffcc00; }
  .heart-hp { color: #ff3344; letter-spacing: 2px; }

  /* Controls Bar */
  #control-bar {
    background: #141422;
    border-bottom: 2px solid #2a2a44;
    padding: 6px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    font-weight: bold;
    flex-wrap: wrap;
    gap: 6px;
  }
  .btn-group { display: flex; align-items: center; gap: 4px; }
  .ctrl-btn {
    background: #25253d;
    border: 1px solid #5a5a88;
    color: #fff;
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 10px;
    font-weight: bold;
    transition: all 0.15s;
  }
  .ctrl-btn:hover { background: #3d3d66; border-color: #00ffff; }
  .ctrl-btn:active { transform: scale(0.94); }
  
  .status-badge {
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 10px;
    cursor: pointer;
    font-weight: bold;
  }
  .status-party { background: #e45c10; color: #fff; animation: party 0.6s infinite; }
  .status-paused { background: #aa2200; color: #fff; animation: pulse 1s infinite; }
  @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
  @keyframes party { 0% { background: #e45c10; } 50% { background: #b878f8; } 100% { background: #e45c10; } }

  /* Canvas Container */
  .canvas-container {
    position: relative;
    width: 100%;
    background: #080810;
    display: flex;
    justify-content: center;
    padding: 4px;
  }
  canvas {
    width: 100%;
    height: auto;
    aspect-ratio: 1408 / 768;
    display: block;
    cursor: pointer;
    image-rendering: pixelated;
    border: 2px solid #2a2a44;
    border-radius: 4px;
  }

  /* Comic Dialogue Box */
  #dialogue-container {
    width: calc(100% - 16px);
    margin: 8px;
    background: #0e1a38;
    border: 3px solid #2a4c8a;
    box-shadow: inset 0 0 12px rgba(0,0,0,0.6), 0 4px 12px rgba(0,0,0,0.5);
    border-radius: 6px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 14px;
    position: relative;
  }
  #dialogue-portrait-box {
    width: 64px;
    height: 64px;
    border: 3px solid #842828;
    background: #1a1a2e;
    border-radius: 4px;
    overflow: hidden;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 8px rgba(0,0,0,0.6);
  }
  #dialogue-portrait {
    width: 100%;
    height: 100%;
    object-fit: cover;
    image-rendering: pixelated;
  }
  #dialogue-text-box {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  #dialogue-speaker {
    font-family: 'Courier New', monospace;
    font-size: 14px;
    font-weight: 900;
    color: #ffcc00;
  }
  #dialogue-message {
    font-family: 'Courier New', monospace;
    font-size: 13px;
    color: #ffffff;
    line-height: 1.35;
    min-height: 28px;
  }
  #dialogue-indicator {
    position: absolute;
    bottom: 8px;
    right: 12px;
    color: #ffffff;
    font-size: 10px;
    animation: pulse 0.8s infinite;
  }

  /* Zone Info Footer */
  #zone-legend {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    padding: 6px 12px;
    background: #10101c;
    border-top: 1px solid #22223a;
    font-size: 10px;
    color: #aaa;
    gap: 8px;
  }
  .zone-tag {
    cursor: pointer;
    padding: 2px 6px;
    border-radius: 3px;
    background: #181828;
    border: 1px solid #333355;
    color: #00ffff;
  }
  .zone-tag:hover { background: #252544; }
</style>
</head>
<body>

<div id="game-wrapper">
  <!-- Top HUD Bar -->
  <div id="retro-header">
    <div>LEVEL 04</div>
    <div>STUDIO: <span class="stat-badge">[HERMES GAME STUDIO]</span></div>
    <div>HP: <span class="heart-hp">❤️❤️❤️</span></div>
    <div>CASH: <span class="stat-badge">$24,800</span></div>
    <div>DAY: <span class="stat-badge">42</span></div>
  </div>

  <!-- Interactive Controls -->
  <div id="control-bar">
    <div>🏛️ <b>ARENA AI SIMULATOR (HD SPRITES)</b></div>
    <span id="party-btn" class="status-badge status-party" onclick="toggleParty()">BEER FRIDAY 🍺</span>
    <div class="btn-group">
      <span>ZOOM:</span>
      <span id="zoom-disp" style="color:#00ffff;">1.0x</span>
      <button class="ctrl-btn" onclick="adjustZoom(-0.25)">-</button>
      <button class="ctrl-btn" onclick="adjustZoom(0.25)">+</button>
      <button class="ctrl-btn" onclick="resetZoom()">RESET 🔄</button>
    </div>
    <div>🎵 <span id="bgm-btn" style="color:#00ffff; cursor:pointer;" onclick="toggleBGM()">START BGM 🔊</span></div>
  </div>

  <!-- Main Game Canvas -->
  <div class="canvas-container">
    <canvas id="gameCanvas" width="1408" height="768"></canvas>
  </div>

  <!-- Comic Dialogue Box -->
  <div id="dialogue-container">
    <div id="dialogue-portrait-box">
      <img id="dialogue-portrait" src="" alt="Avatar" />
    </div>
    <div id="dialogue-text-box">
      <div id="dialogue-speaker">Zillion (Tech Director):</div>
      <div id="dialogue-message">Boss approved Gate 2! Let's get to work!</div>
    </div>
    <div id="dialogue-indicator">▼</div>
  </div>

  <!-- Interactive Zone Legend -->
  <div id="zone-legend">
    <span class="zone-tag" onclick="focusZone('gym')">🏋️ GYM</span>
    <span class="zone-tag" onclick="focusZone('lounge')">🎱 BILLIARDS LOUNGE</span>
    <span class="zone-tag" onclick="focusZone('war_room')">📊 WAR ROOM</span>
    <span class="zone-tag" onclick="focusZone('pantry')">☕ PANTRY</span>
    <span class="zone-tag" onclick="focusZone('dev_desks')">💻 DEV WORKSTATIONS</span>
    <span class="zone-tag" onclick="focusZone('exec')">🏛️ EXEC SUITE</span>
  </div>
</div>

<script>
// --- ASSETS INJECTION ---
const ASSETS = __ASSETS_JSON__;

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const zoomDisp = document.getElementById('zoom-disp');
const bgmBtn = document.getElementById('bgm-btn');
const partyBtn = document.getElementById('party-btn');
const diagSpeaker = document.getElementById('dialogue-speaker');
const diagMessage = document.getElementById('dialogue-message');
const diagPortrait = document.getElementById('dialogue-portrait');

// Load Background Image
const bgImg = new Image();
bgImg.src = ASSETS.office_bg;

// Load Character Sprites
const sprites = {};
const headAvatars = {};
const agentKeys = ['zillion', 'marcus', 'aria', 'cody', 'pixel', 'echo', 'vortex', 'jax', 'vanguard', 'chronos'];

agentKeys.forEach(k => {
  const img = new Image();
  img.src = ASSETS[k];
  sprites[k] = img;

  const hImg = new Image();
  hImg.src = ASSETS[k + '_head'];
  headAvatars[k] = hImg;
});

// Audio System
let actx = null;
let bgmPlaying = false;
let bgmInterval = null;
let isBeerFriday = true;

function initAudio() {
  try {
    if (!actx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) actx = new AudioCtx();
    }
    if (actx && actx.state === 'suspended') actx.resume();
  } catch(e){}
}

function startBGM() {
  if (bgmPlaying || !actx) return;
  bgmPlaying = true;
  bgmBtn.innerText = "ON 🔊";
  const notes = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 440.00, 493.88];
  let noteIdx = 0;
  if (bgmInterval) clearInterval(bgmInterval);
  bgmInterval = setInterval(() => {
    try {
      if (!bgmPlaying || !actx) return;
      const now = actx.currentTime;
      const osc = actx.createOscillator();
      osc.type = isBeerFriday ? 'square' : 'triangle';
      osc.frequency.setValueAtTime(notes[noteIdx], now);
      const noteGain = actx.createGain();
      noteGain.gain.setValueAtTime(0.025, now);
      noteGain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
      osc.connect(noteGain);
      noteGain.connect(actx.destination);
      osc.start(now);
      osc.stop(now + 0.18);
      noteIdx = (noteIdx + 1) % notes.length;
    } catch(e){}
  }, 200);
}

function toggleBGM() {
  initAudio();
  bgmPlaying = !bgmPlaying;
  bgmBtn.innerText = bgmPlaying ? "ON 🔊" : "OFF 🔇";
  if (bgmPlaying) startBGM();
}

function playSFX(type) {
  try {
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
      osc.frequency.setValueAtTime(800, now);
      osc.frequency.exponentialRampToValueAtTime(150, now + 0.08);
      gain.gain.setValueAtTime(0.3, now);
      gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
      osc.start(now);
      osc.stop(now + 0.08);
    } else if (type === 'cheer') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(440, now);
      osc.frequency.linearRampToValueAtTime(880, now + 0.15);
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
      osc.start(now);
      osc.stop(now + 0.2);
    }
  } catch(e){}
}

// 10 Detailed Studio Agents with Initial World Coordinates (1408x768 scale)
const agents = [
  { id: 'zillion', name: 'Zillion', role: 'Tech Director', x: 520, y: 320, vx: 0.3, vy: 0.2, phrase: "Boss approved Gate 2! Let's get to work!", zone: 'war_room' },
  { id: 'marcus', name: 'Marcus', role: 'Producer', x: 740, y: 640, vx: -0.2, vy: 0.1, phrase: "Beer Friday Party is LIVE! Sprint velocity is at 100%!", zone: 'war_room' },
  { id: 'aria', name: 'Aria', role: 'Systems Designer', x: 620, y: 320, vx: 0.1, vy: -0.2, phrase: "Tiled level maps and GDD balance trees are fully synced!", zone: 'war_room' },
  { id: 'cody', name: 'Cody', role: 'Lead Programmer', x: 720, y: 220, vx: 0.3, vy: 0.1, phrase: "qwen2.5-coder code synthesis ready. 60 FPS verified!", zone: 'dev_desks' },
  { id: 'pixel', name: 'Pixel', role: 'Graphic Artist', x: 960, y: 220, vx: -0.2, vy: 0.2, phrase: "HD 16-bit PNG character sprite atlases rendered in full crispness!", zone: 'dev_desks' },
  { id: 'echo', name: 'Echo', role: 'Audio Director', x: 1200, y: 220, vx: 0.2, vy: -0.1, phrase: "44.1kHz stereo Web Audio MIDI OST synthesizer playing!", zone: 'dev_desks' },
  { id: 'vortex', name: 'Vortex', role: 'Shader Dev', x: 960, y: 440, vx: -0.1, vy: 0.3, phrase: "GLSL fragment shaders and GPU particles loaded!", zone: 'dev_desks' },
  { id: 'jax', name: 'Jax', role: 'QA Auditor', x: 1200, y: 440, vx: 0.2, vy: 0.2, phrase: "Jax rubber duck 🦆 & DeepSeek-R1 QA test suite passed 100%!", zone: 'dev_desks' },
  { id: 'vanguard', name: 'Judge Vanguard', role: 'AAA Quality Judge', x: 880, y: 640, vx: -0.2, vy: -0.1, phrase: "AAA Commercial Benchmark: 10/10 Test Cases Cleared!", zone: 'war_room' },
  { id: 'chronos', name: 'Keeper Chronos', role: 'Memory Anchor', x: 280, y: 640, vx: 0.1, vy: 0.2, phrase: "Vector context memory anchored in persistent phone storage!", zone: 'lounge' }
];

// Billiards Simulation in Lounge
const poolBalls = [
  { x: 380, y: 620, vx: 1.5, vy: 1.0, color: '#ffffff' },
  { x: 340, y: 615, vx: -1.0, vy: 0.8, color: '#ee2211' },
  { x: 340, y: 625, vx: 0.7, vy: -1.2, color: '#ffff00' },
  { x: 310, y: 620, vx: -0.9, vy: -0.6, color: '#38b0de' }
];

// Camera / Zoom System
let zoomScale = 1.0;
let camX = 704;
let camY = 384;

function resetZoom() {
  initAudio();
  zoomScale = 1.0;
  camX = 704;
  camY = 384;
  zoomDisp.innerText = "1.0x";
}

function adjustZoom(delta) {
  initAudio();
  zoomScale = Math.max(1.0, Math.min(2.5, +(zoomScale + delta).toFixed(2)));
  zoomDisp.innerText = zoomScale.toFixed(1) + "x";
}

function focusZone(zone) {
  initAudio();
  if (zone === 'gym') { camX = 150; camY = 620; setDialogue(agents[6]); }
  else if (zone === 'lounge') { camX = 380; camY = 620; setDialogue(agents[9]); shootPool(); }
  else if (zone === 'war_room') { camX = 760; camY = 640; setDialogue(agents[0]); }
  else if (zone === 'pantry') { camX = 1200; camY = 640; setDialogue(agents[1]); }
  else if (zone === 'dev_desks') { camX = 960; camY = 320; setDialogue(agents[3]); }
  else if (zone === 'exec') { camX = 150; camY = 220; setDialogue(agents[0]); }
  zoomScale = 1.5;
  zoomDisp.innerText = "1.5x";
}

function setDialogue(ag) {
  if (!ag) return;
  diagSpeaker.innerText = ag.name + " (" + ag.role + "):";
  diagMessage.innerText = ag.phrase;
  if (headAvatars[ag.id] && headAvatars[ag.id].complete) {
    diagPortrait.src = headAvatars[ag.id].src;
  }
}

// Initial dialogue setup
setDialogue(agents[0]);

function toggleParty() {
  initAudio();
  isBeerFriday = !isBeerFriday;
  partyBtn.innerText = isBeerFriday ? "BEER FRIDAY 🍺" : "STUDIO ACTIVE 💻";
  partyBtn.className = isBeerFriday ? "status-badge status-party" : "status-badge";
  playSFX('cheer');
  setDialogue(agents[1]);
}

function shootPool() {
  playSFX('pool_hit');
  poolBalls[0].vx = (Math.random() - 0.5) * 8;
  poolBalls[0].vy = (Math.random() - 0.5) * 8;
}

let stepFrame = 0;
let activeBubble = null;
let bubbleTimer = 0;

function updateSimulation() {
  stepFrame++;
  if (bubbleTimer > 0) bubbleTimer--;

  // Wandering Agent Movement within Zone Bounds
  for (let a of agents) {
    if (Math.random() < 0.02) {
      a.vx = (Math.random() - 0.5) * 1.5;
      a.vy = (Math.random() - 0.5) * 1.5;
    }
    a.x += a.vx;
    a.y += a.vy;

    // World boundary clamping
    a.x = Math.max(80, Math.min(1330, a.x));
    a.y = Math.max(100, Math.min(710, a.y));

    // Collision detection & chatter trigger
    for (let other of agents) {
      if (other.id !== a.id && Math.hypot(a.x - other.x, a.y - other.y) < 40) {
        if (bubbleTimer <= 0 && Math.random() < 0.02) {
          activeBubble = { agent: a, text: a.name + ": " + a.phrase };
          bubbleTimer = 180;
          setDialogue(a);
          playSFX('blip');
        }
      }
    }
  }

  // Billiards Ball Physics
  for (let b of poolBalls) {
    b.x += b.vx; b.y += b.vy;
    b.vx *= 0.985; b.vy *= 0.985;
    if (b.x < 270 || b.x > 490) { b.vx *= -0.92; playSFX('pool_hit'); }
    if (b.y < 570 || b.y > 680) { b.vy *= -0.92; playSFX('pool_hit'); }
    if (Math.abs(b.vx) < 0.05 && Math.abs(b.vy) < 0.05 && Math.random() < 0.01) {
      b.vx = (Math.random() - 0.5) * 4;
      b.vy = (Math.random() - 0.5) * 4;
    }
  }
}

function render() {
  try {
    ctx.save();
    ctx.clearRect(0, 0, 1408, 768);

    // Camera Transformation & Clamping
    if (zoomScale > 1.0) {
      const maxOffsetX = 704 * (1 - 1 / zoomScale);
      const maxOffsetY = 384 * (1 - 1 / zoomScale);
      let cx = Math.max(704 - maxOffsetX, Math.min(704 + maxOffsetX, camX));
      let cy = Math.max(384 - maxOffsetY, Math.min(384 + maxOffsetY, camY));

      ctx.translate(704, 384);
      ctx.scale(zoomScale, zoomScale);
      ctx.translate(-cx, -cy);
    }

    // 1. Draw HD Studio Campus Map
    if (bgImg.complete && bgImg.naturalWidth > 0) {
      ctx.drawImage(bgImg, 0, 0, 1408, 768);
    } else {
      ctx.fillStyle = '#181828';
      ctx.fillRect(0, 0, 1408, 768);
    }

    // 2. Draw Dynamic Pool Balls on Lounge Table
    for (let b of poolBalls) {
      ctx.fillStyle = b.color;
      ctx.beginPath();
      ctx.arc(b.x, b.y, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    // 3. Draw All 10 High-Definition Character Sprites
    const bob = Math.sin(stepFrame * 0.15) * 2;
    for (let a of agents) {
      const spr = sprites[a.id];
      if (spr && spr.complete && spr.naturalWidth > 0) {
        const sw = 48;
        const sh = (spr.height / spr.width) * sw;

        // Shadow ellipse
        ctx.fillStyle = 'rgba(0,0,0,0.35)';
        ctx.beginPath();
        ctx.ellipse(a.x, a.y + 4, 18, 7, 0, 0, Math.PI * 2);
        ctx.fill();

        // Draw HD Character Sprite
        ctx.drawImage(spr, a.x - sw / 2, a.y - sh + bob, sw, sh);

        // Name tag
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 11px monospace';
        ctx.shadowColor = '#000000';
        ctx.shadowBlur = 4;
        ctx.fillText(a.name, a.x - (a.name.length * 3.3), a.y + 16 + bob);
        ctx.shadowBlur = 0;
      }
    }

    // 4. Render Active Thought/Speech Bubble
    if (bubbleTimer > 0 && activeBubble) {
      const ag = activeBubble.agent;
      const bx = Math.max(40, Math.min(1150, ag.x - 100));
      const by = Math.max(30, ag.y - 85);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.96)';
      ctx.fillRect(bx, by, 220, 36);
      ctx.strokeStyle = '#182848';
      ctx.lineWidth = 2;
      ctx.strokeRect(bx, by, 220, 36);

      // Tail
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.moveTo(ag.x - 5, by + 36);
      ctx.lineTo(ag.x + 5, by + 36);
      ctx.lineTo(ag.x, by + 44);
      ctx.fill();

      ctx.fillStyle = '#000000';
      ctx.font = 'bold 11px monospace';
      ctx.fillText(ag.name + ":", bx + 8, by + 14);
      ctx.font = '10px monospace';
      ctx.fillText(activeBubble.text.substring(0, 34), bx + 8, by + 28);
    }

    ctx.restore();
  } catch(e){}
}

function handleInteraction(clientX, clientY) {
  initAudio();
  const rect = canvas.getBoundingClientRect();
  const rawX = (clientX - rect.left) * (1408 / rect.width);
  const rawY = (clientY - rect.top) * (768 / rect.height);

  let clickX = rawX;
  let clickY = rawY;

  if (zoomScale > 1.0) {
    const maxOffsetX = 704 * (1 - 1 / zoomScale);
    const maxOffsetY = 384 * (1 - 1 / zoomScale);
    let cx = Math.max(704 - maxOffsetX, Math.min(704 + maxOffsetX, camX));
    let cy = Math.max(384 - maxOffsetY, Math.min(384 + maxOffsetY, camY));
    clickX = (rawX - 704) / zoomScale + cx;
    clickY = (rawY - 384) / zoomScale + cy;
  }

  // Check agent clicks
  let touchedAgent = null;
  for (let a of agents) {
    if (Math.hypot(clickX - a.x, clickY - a.y) < 40) {
      touchedAgent = a;
      break;
    }
  }

  if (touchedAgent) {
    setDialogue(touchedAgent);
    activeBubble = { agent: touchedAgent, text: touchedAgent.name + ": " + touchedAgent.phrase };
    bubbleTimer = 220;
    playSFX('blip');
    return;
  }

  // Check Pool Table Click
  if (clickX >= 260 && clickX <= 500 && clickY >= 560 && clickY <= 700) {
    shootPool();
    setDialogue(agents[9]);
    return;
  }
}

canvas.addEventListener('touchstart', e => {
  if (e.touches.length > 0) handleInteraction(e.touches[0].clientX, e.touches[0].clientY);
});
canvas.addEventListener('mousedown', e => {
  handleInteraction(e.clientX, e.clientY);
});

function loop() {
  updateSimulation();
  render();
  requestAnimationFrame(loop);
}

requestAnimationFrame(loop);
</script>
</body>
</html>
"""

final_html = html_template.replace("__ASSETS_JSON__", json.dumps(assets))

with open('/home/user/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print('Compiled /home/user/index.html, total size:', len(final_html))
