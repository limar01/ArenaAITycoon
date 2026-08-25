#!/usr/bin/env python3
import os
import base64

BASE = os.path.expanduser("~/projects/hermes_game_studio/builds/castlevania_stage1")
SPRITES_DIR = os.path.expanduser("~/sprites")
ASSETS_DIR = os.path.join(BASE, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Copy sprites to assets dir
os.system(f"cp -f {SPRITES_DIR}/*.png {ASSETS_DIR}/ 2>/dev/null")

char_path = os.path.join(SPRITES_DIR, "character_sprites_preview.png")
office_path = os.path.join(SPRITES_DIR, "office_topdown_preview.png")

char_b64 = ""
office_b64 = ""

if os.path.exists(char_path):
    with open(char_path, "rb") as f:
        char_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

if os.path.exists(office_path):
    with open(office_path, "rb") as f:
        office_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Arena AI Simulator: Studio Life - HD Sprites Edition</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
  body {
    background: #080810;
    color: #fff;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow-x: hidden;
    padding: 8px;
  }
  #game-container {
    width: 100%;
    max-width: 480px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #121220;
    border-radius: 12px;
    border: 2px solid #3d3d66;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
    overflow: hidden;
  }
  #hud-bar {
    width: 100%;
    background: #1a1a2e;
    border-bottom: 2px solid #3d3d66;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    font-size: 11px;
    font-weight: bold;
    color: #ffcc00;
    gap: 6px;
  }
  .status-badge {
    background: #008833;
    color: #fff;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 10px;
    cursor: pointer;
    border: 1px solid rgba(255,255,255,0.2);
  }
  .status-paused { background: #aa2200; animation: pulse 1s infinite; }
  .status-party { background: #e45c10; color: #fff; animation: party 0.5s infinite; }
  .btn-group { display: flex; align-items: center; gap: 4px; }
  .zoom-btn {
    background: #2a2a44;
    border: 1px solid #666699;
    color: #fff;
    padding: 3px 7px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 10px;
    font-weight: bold;
  }
  .zoom-btn:hover { background: #3d3d66; }
  @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
  @keyframes party { 0% { background: #e45c10; } 50% { background: #b878f8; } 100% { background: #e45c10; } }
  .canvas-wrapper {
    position: relative;
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 8px;
    background: #0a0a14;
  }
  canvas {
    width: 100%;
    max-width: 440px;
    aspect-ratio: 4/3;
    display: block;
    border: 3px solid #b878f8;
    border-radius: 6px;
    box-shadow: 0 0 20px rgba(184, 120, 248, 0.4);
    background: #222238;
    cursor: pointer;
    image-rendering: pixelated;
  }
  #agent-info-card {
    width: calc(100% - 16px);
    margin: 6px 8px;
    background: #18182c;
    border: 1px solid #444477;
    border-radius: 8px;
    padding: 6px 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
  }
  .agent-avatar {
    width: 26px;
    height: 26px;
    border-radius: 6px;
    background: #222233;
    border: 2px solid #ffcc00;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    margin-right: 8px;
  }
  #instruction-tip {
    padding: 6px 10px;
    font-size: 10px;
    color: #00ffff;
    text-align: center;
    font-weight: bold;
    background: #141424;
    width: 100%;
    border-top: 1px solid #22223a;
  }
</style>
</head>
<body>

<div id="game-container">
  <div id="hud-bar">
    <div>🏛️ <b>ARENA AI STUDIO (HD SPRITES)</b></div>
    <span id="pauseBadge" class="status-badge status-party" onclick="togglePause()">BEER FRIDAY 🍺</span>
    <div class="btn-group">
      <span>ZOOM:</span>
      <span id="zoom-level" style="color:#00ffff;">1.0x</span>
      <button class="zoom-btn" onclick="adjustZoom(-0.25)">-</button>
      <button class="zoom-btn" onclick="adjustZoom(0.25)">+</button>
      <button class="zoom-btn" onclick="resetCamera()">RESET 🔄</button>
    </div>
    <div>🎵 <span id="bgm-status" style="color:#00ffff; cursor:pointer;" onclick="toggleBGM()">START BGM 🔊</span></div>
  </div>

  <div class="canvas-wrapper">
    <canvas id="canvas" width="400" height="300"></canvas>
  </div>

  <div id="agent-info-card">
    <div style="display:flex; align-items:center;">
      <div class="agent-avatar" id="info-avatar">👓</div>
      <div>
        <div id="info-name" style="font-weight:bold; color:#ffcc00;">Zillion (Tech Director)</div>
        <div id="info-phrase" style="color:#aaccff; font-size:10px;">"HD PNG Sprites Linked & Camera Clamped!"</div>
      </div>
    </div>
    <button class="zoom-btn" onclick="focusAgent('zillion')">TRACK 🎯</button>
  </div>

  <div id="instruction-tip">
    💡 REAL HD SPRITES LOADED | TAP SPRITES / POOL TABLE TO INTERACT
  </div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const zoomLevelDisplay = document.getElementById('zoom-level');
const bgmStatus = document.getElementById('bgm-status');
const pauseBadge = document.getElementById('pauseBadge');
const infoName = document.getElementById('info-name');
const infoPhrase = document.getElementById('info-phrase');
const infoAvatar = document.getElementById('info-avatar');

// Sprite Images
const charImg = new Image();
let charLoaded = false;
charImg.onload = () => { charLoaded = true; };
charImg.src = """ + (f'"{char_b64}"' if char_b64 else '"assets/character_sprites_preview.png"') + """;

const officeImg = new Image();
let officeLoaded = false;
officeImg.onload = () => { officeLoaded = true; };
officeImg.src = """ + (f'"{office_b64}"' if office_b64 else '"assets/office_topdown_preview.png"') + """;

// Audio
let actx = null;
let bgmPlaying = false;
let bgmInterval = null;

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
  bgmStatus.innerText = "ON 🔊";
  const notes = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 440.00, 493.88];
  let noteIdx = 0;
  if (bgmInterval) clearInterval(bgmInterval);
  bgmInterval = setInterval(() => {
    try {
      if (!bgmPlaying || !actx || simPaused) return;
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
  bgmStatus.innerText = bgmPlaying ? "ON 🔊" : "OFF 🔇";
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

// State
let simPaused = false;
let isBeerFriday = true;
let activeBubble = null;
let bubbleTimer = 0;
let stepFrame = 0;

let zoomScale = 1.0;
let camX = 200;
let camY = 150;

function resetCamera() {
  initAudio();
  zoomScale = 1.0;
  camX = 200;
  camY = 150;
  zoomLevelDisplay.innerText = "1.0x";
}

function adjustZoom(delta) {
  initAudio();
  zoomScale = Math.max(1.0, Math.min(2.5, +(zoomScale + delta).toFixed(2)));
  zoomLevelDisplay.innerText = zoomScale.toFixed(1) + "x";
}

const agents = [
  { id: 'zillion', name: 'Zillion', role: 'Tech Director', emoji: '👓', x: 220, y: 100, coat: '#222233', glasses: true, phrase: 'HD Sprites Applied & Camera Clamped!' },
  { id: 'marcus', name: 'Marcus', role: 'Producer', emoji: '📋', x: 100, y: 100, coat: '#ffffff', vest: '#843800', phrase: 'Beer Friday Party is LIVE! Cheers Boss!' },
  { id: 'aria', name: 'Aria', role: 'Designer', emoji: '🎧', x: 370, y: 120, hair: '#b878f8', coat: '#6820b0', headphones: true, phrase: 'Bright studio campus map in full HD!' },
  { id: 'cody', name: 'Cody', role: 'Programmer', emoji: '🧢', x: 280, y: 120, coat: '#00cc66', cap: true, phrase: 'qwen2.5-coder multi-model engine active!' },
  { id: 'pixel', name: 'Pixel', role: 'Artist', emoji: '🎨', x: 340, y: 120, coat: '#e45c10', beret: true, phrase: 'Crisp 16-bit HD pixel character sprites active!' },
  { id: 'echo', name: 'Echo', role: 'Audio', emoji: '🎵', x: 300, y: 220, coat: '#442211', headset: true, phrase: 'Playing 16-Bit 44.1kHz MIDI OST in stereo!' },
  { id: 'vortex', name: 'Vortex', role: 'Shader Dev', emoji: '⚡', x: 220, y: 220, hair: '#00ffff', coat: '#113344', phrase: 'Walking to Gym Treadmill for workout!' },
  { id: 'jax', name: 'Jax', role: 'QA Auditor', emoji: '🦆', x: 160, y: 220, coat: '#005888', duck: true, phrase: 'Jax rubber duck & deepseek-r1 QA passed 100%!' },
  { id: 'vanguard', name: 'Vanguard', role: 'AAA Judge', emoji: '⚖️', x: 100, y: 220, coat: '#22222b', suit: true, phrase: 'AAA Benchmark: HD PNG Canvas PASSED 100%!' },
  { id: 'chronos', name: 'Chronos', role: 'Memory Anchor', emoji: '⏳', x: 360, y: 220, coat: '#554422', phrase: 'Savepoint v3.0 anchored in phone storage!' }
];

const poolBalls = [
  { x: 240, y: 220, vx: 1.5, vy: 1.0, color: '#ffffff' },
  { x: 220, y: 215, vx: -1.0, vy: 0.8, color: '#ee2211' },
  { x: 220, y: 225, vx: 0.7, vy: -1.2, color: '#ffff00' },
  { x: 205, y: 220, vx: -0.9, vy: -0.6, color: '#38b0de' }
];

function updateInfoCard(a) {
  if (!a) return;
  infoAvatar.innerText = a.emoji || '👤';
  infoName.innerText = `${a.name} (${a.role})`;
  infoPhrase.innerText = `"${a.phrase}"`;
}

function focusAgent(id) {
  const ag = agents.find(a => a.id === id);
  if (ag) {
    camX = ag.x;
    camY = ag.y;
    activeBubble = { agent: ag, text: `${ag.name}: ${ag.phrase}` };
    bubbleTimer = 200;
    updateInfoCard(ag);
    playSFX('blip');
  }
}

function updateSimulation() {
  try {
    if (simPaused) return;
    stepFrame++;
    if (bubbleTimer > 0) bubbleTimer--;

    for (let a of agents) {
      if (Math.random() < 0.03) {
        a.x += (Math.random() - 0.5) * 8;
        a.y += (Math.random() - 0.5) * 6;
        a.x = Math.max(35, Math.min(365, a.x));
        a.y = Math.max(35, Math.min(265, a.y));
      }
      for (let other of agents) {
        if (other.id !== a.id && Math.hypot(a.x - other.x, a.y - other.y) < 26) {
          if (bubbleTimer <= 0 && Math.random() < 0.02) {
            activeBubble = { agent: a, text: `${a.name}: ${a.phrase}` };
            bubbleTimer = 160;
            updateInfoCard(a);
            playSFX('blip');
          }
        }
      }
    }

    for (let b of poolBalls) {
      b.x += b.vx; b.y += b.vy;
      b.vx *= 0.985; b.vy *= 0.985;
      if (b.x < 210 || b.x > 260) { b.vx *= -0.92; playSFX('pool_hit'); }
      if (b.y < 200 || b.y > 235) { b.vy *= -0.92; playSFX('pool_hit'); }
      if (Math.abs(b.vx) < 0.05 && Math.abs(b.vy) < 0.05 && Math.random() < 0.015) {
        b.vx = (Math.random() - 0.5) * 3.5;
        b.vy = (Math.random() - 0.5) * 3.5;
      }
    }
  } catch(e){}
}

function drawDetailedSprite(a, idx) {
  const bob = Math.sin(stepFrame * 0.2 + (a.x * 0.05)) * 1.5;

  if (charLoaded && charImg.complete && charImg.naturalWidth > 0) {
    try {
      const col = idx % 5;
      const row = Math.floor(idx / 5);
      const sw = charImg.width / 5;
      const sh = charImg.height / 2;
      ctx.drawImage(charImg, col * sw, row * sh, sw, sh, a.x - 12, a.y - 16 + bob, 24, 24);
    } catch(e) {
      drawVectorSprite(a, bob);
    }
  } else {
    drawVectorSprite(a, bob);
  }

  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 8px monospace';
  ctx.shadowColor = '#000000'; ctx.shadowBlur = 4;
  ctx.fillText(a.name, a.x - (a.name.length * 2.4), a.y + 18 + bob);
  ctx.shadowBlur = 0;
}

function drawVectorSprite(a, bob) {
  ctx.fillStyle = a.coat || '#38b0de';
  ctx.fillRect(a.x - 6, a.y - 5 + bob, 12, 11);
  if (a.vest) { ctx.fillStyle = a.vest; ctx.fillRect(a.x - 4, a.y - 5 + bob, 8, 11); }
  if (a.suit) { ctx.fillStyle = '#ffffff'; ctx.fillRect(a.x - 1, a.y - 5 + bob, 2, 10); }
  ctx.fillStyle = '#111118';
  ctx.fillRect(a.x - 4, a.y + 6 + bob, 3, 5);
  ctx.fillRect(a.x + 1, a.y + 6 + bob, 3, 5);
  ctx.fillStyle = '#fce0a8'; ctx.fillRect(a.x - 5, a.y - 13 + bob, 10, 8);
  ctx.fillStyle = a.hair || '#222'; ctx.fillRect(a.x - 6, a.y - 15 + bob, 12, 4);
  if (a.glasses) { ctx.fillStyle = '#ffffff'; ctx.fillRect(a.x - 4, a.y - 10 + bob, 3, 3); ctx.fillRect(a.x + 1, a.y - 10 + bob, 3, 3); }
  if (a.cap) { ctx.fillStyle = '#ee2211'; ctx.fillRect(a.x - 6, a.y - 16 + bob, 12, 4); }
  if (a.beret) { ctx.fillStyle = '#e45c10'; ctx.fillRect(a.x - 7, a.y - 17 + bob, 14, 4); }
  if (a.headphones || a.headset) { ctx.fillStyle = '#00ffff'; ctx.fillRect(a.x - 8, a.y - 12 + bob, 3, 6); ctx.fillRect(a.x + 5, a.y - 12 + bob, 3, 6); }
  if (a.duck) { ctx.fillStyle = '#ffff00'; ctx.fillRect(a.x + 5, a.y - 4 + bob, 5, 5); }
}

function render() {
  try {
    ctx.save();
    ctx.clearRect(0, 0, 400, 300);

    if (zoomScale > 1.0) {
      const maxOffset = 200 * (1 - 1/zoomScale);
      let cx = Math.max(200 - maxOffset, Math.min(200 + maxOffset, camX));
      let cy = Math.max(150 - maxOffset * 0.75, Math.min(150 + maxOffset * 0.75, camY));
      ctx.translate(200, 150);
      ctx.scale(zoomScale, zoomScale);
      ctx.translate(-cx, -cy);
    }

    ctx.fillStyle = '#181828';
    ctx.fillRect(0, 0, 400, 300);
    ctx.fillStyle = isBeerFriday ? '#2b1738' : '#202038';
    ctx.fillRect(10, 10, 380, 280);

    if (officeLoaded && officeImg.complete && officeImg.naturalWidth > 0) {
      try {
        ctx.drawImage(officeImg, 10, 10, 380, 280);
      } catch(e){}
    } else {
      ctx.fillStyle = '#441a10'; ctx.fillRect(20, 20, 120, 80);
      ctx.fillStyle = '#151d30'; ctx.fillRect(150, 20, 230, 140);
      ctx.fillStyle = '#2d1616'; ctx.fillRect(20, 170, 120, 110);
      ctx.fillStyle = isBeerFriday ? '#321632' : '#142d1b'; ctx.fillRect(150, 170, 150, 110);
      ctx.fillStyle = '#302315'; ctx.fillRect(310, 170, 70, 110);
    }

    // Pool Table & Balls
    ctx.fillStyle = '#6e2e00'; ctx.fillRect(198, 193, 68, 48);
    ctx.fillStyle = '#007a2d'; ctx.fillRect(202, 197, 60, 40);
    for (let b of poolBalls) {
      ctx.fillStyle = b.color;
      ctx.beginPath(); ctx.arc(b.x, b.y, 3, 0, Math.PI * 2); ctx.fill();
    }

    // Sprites
    agents.forEach((a, idx) => drawDetailedSprite(a, idx));

    // Speech Bubbles
    if (bubbleTimer > 0 && activeBubble) {
      const ag = activeBubble.agent;
      const bx = Math.max(15, Math.min(240, ag.x - 55));
      const by = Math.max(20, ag.y - 42);
      ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
      ctx.fillRect(bx, by, 150, 28);
      ctx.strokeStyle = '#000000'; ctx.lineWidth = 1.5; ctx.strokeRect(bx, by, 150, 28);
      ctx.fillStyle = '#000000'; ctx.font = 'bold 8px monospace';
      ctx.fillText(`${ag.name}:`, bx + 5, by + 10);
      ctx.font = '7px monospace';
      ctx.fillText(activeBubble.text.substring(0, 32), bx + 5, by + 22);
    }

    ctx.restore();
  } catch(e){}
}

function handleInteraction(clientX, clientY) {
  initAudio();
  const rect = canvas.getBoundingClientRect();
  const rawX = (clientX - rect.left) * (400 / rect.width);
  const rawY = (clientY - rect.top) * (300 / rect.height);
  let clickX = rawX;
  let clickY = rawY;
  if (zoomScale > 1.0) {
    const maxOffset = 200 * (1 - 1/zoomScale);
    let cx = Math.max(200 - maxOffset, Math.min(200 + maxOffset, camX));
    let cy = Math.max(150 - maxOffset * 0.75, Math.min(150 + maxOffset * 0.75, camY));
    clickX = (rawX - 200) / zoomScale + cx;
    clickY = (rawY - 150) / zoomScale + cy;
  }

  let touchedAgent = null;
  for (let a of agents) {
    if (Math.hypot(clickX - a.x, clickY - a.y) < 22) {
      touchedAgent = a;
      break;
    }
  }

  if (touchedAgent) {
    activeBubble = { agent: touchedAgent, text: `${touchedAgent.name}: ${touchedAgent.phrase}` };
    bubbleTimer = 180;
    updateInfoCard(touchedAgent);
    playSFX('blip');
    return;
  }

  if (clickX >= 198 && clickX <= 266 && clickY >= 193 && clickY <= 241) {
    playSFX('pool_hit');
    poolBalls[0].vx = (Math.random() - 0.5) * 5;
    poolBalls[0].vy = (Math.random() - 0.5) * 5;
    activeBubble = { agent: { name: 'BOSS', x: 232, y: 217 }, text: 'BOSS shot a break on the Pool Table! 🎱' };
    bubbleTimer = 180;
    return;
  }
}

canvas.addEventListener('touchstart', e => {
  if (e.touches.length > 0) handleInteraction(e.touches[0].clientX, e.touches[0].clientY);
});
canvas.addEventListener('mousedown', e => {
  handleInteraction(e.clientX, e.clientY);
});

function togglePause() {
  initAudio();
  simPaused = !simPaused;
  if (simPaused) {
    pauseBadge.innerText = 'SIM PAUSED ⏸️';
    pauseBadge.className = 'status-badge status-paused';
  } else {
    pauseBadge.innerText = isBeerFriday ? 'BEER FRIDAY 🍺' : 'STUDIO ACTIVE 💻';
    pauseBadge.className = isBeerFriday ? 'status-badge status-party' : 'status-badge';
    playSFX('cheer');
  }
}

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

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: HD Sprites & Clamped Engine deployed to index.html!")
