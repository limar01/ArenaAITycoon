#!/usr/bin/env python3
"""
patch_gate10.py - GLITCH/TRANSPARENT FIX + FOOT-STEP WALK + STATIC NPCs (Boss QA).
1) Loader: 'solidify' each dir sheet -> hard alpha cut (alpha<48 -> 0, else 255) - kills ghost/transparent glitch.
2) Render: grounded anchor (feet touch floor, +3px), walk = frame alt + step tilt + tiny bounce; idle = 0.4px breathing only.
3) Static NPCs: 8 office NPCs (positions validated vs WALL_GRID), idle sway, periodic mini-dialogue bubbles, occasional small step (24px) left/right with proper directional frames.
Reads _g10/index.html, writes _g10/gate10.html.
"""
import os, sys, re

SRC = '/home/user/_g10/index.html'
OUT = '/home/user/_g10/gate10.html'
html = open(SRC, encoding='utf-8').read()

# ---------- 1) LOADER: solidify dir sheets ----------
OLD_LOAD = """  const dImg = new Image();
  dImg.src = ASSETS[k + '_dir'];
  dirSprites[k] = dImg;"""
NEW_LOAD = """  const dImg = new Image();
  dImg.onload = function () {
    // solidify: hard alpha cut (kills ghost/transparent pixels from flood-fill edges)
    try {
      const c = document.createElement('canvas');
      c.width = this.naturalWidth; c.height = this.naturalHeight;
      const cx = c.getContext('2d');
      cx.drawImage(this, 0, 0);
      const id = cx.getImageData(0, 0, c.width, c.height);
      const px = id.data;
      for (let i = 3; i < px.length; i += 4) px[i] = px[i] < 48 ? 0 : 255;
      cx.putImageData(id, 0, 0);
      dirSprites[k] = c;
    } catch (e) { dirSprites[k] = this; }
  };
  dImg.src = ASSETS[k + '_dir'];
  dirSprites[k] = dImg;"""
if OLD_LOAD not in html:
    print("!! loader pattern missing"); sys.exit(1)
html = html.replace(OLD_LOAD, NEW_LOAD, 1)
print("[1] solidify (hard alpha) loader")

# ---------- 2) RENDER: feet + step tilt ----------
# also normalize width for canvas sheets
OLD_SZ = "        const fw = dir.naturalWidth / 3;\n        const fh = dir.naturalHeight / 4;"
NEW_SZ = "        const dwAll = dir.naturalWidth || dir.width;\n        const dhAll = dir.naturalHeight || dir.height;\n        const fw = dwAll / 3;\n        const fh = dhAll / 4;"
if OLD_SZ not in html:
    print("!! size pattern missing"); sys.exit(1)
html = html.replace(OLD_SZ, NEW_SZ, 1)
print("[2a] size normalization for canvas sheets")

OLD_BOB = """        // breathing when idle (<=0.5px, no jumps); gentle walk bob when moving
        const bob = moving ? Math.sin((a.walkFrame % 3) * Math.PI) * 1.2
                           : Math.sin(stepFrame * 0.035 + a.x * 0.05) * 0.5;"""
NEW_BOB = """        // grounded: feet touch floor; breathing when idle, step bounce + tilt when walking
        const stepPh = (a.walkFrame % 2) === 0 ? -1 : 1;
        const bob = moving ? stepPh * 0.8 : Math.sin(stepFrame * 0.03 + a.x * 0.05) * 0.35;
        const tilt = moving ? stepPh * 0.045 : 0;"""
if OLD_BOB not in html:
    print("!! bob pattern missing"); sys.exit(1)
html = html.replace(OLD_BOB, NEW_BOB, 1)

OLD_DRAW = """        // True directional frame from spritesheet (with flip when needed)
        if (flip) {
          ctx.translate(0, 0);
          ctx.scale(-1, 1);
        }
        ctx.drawImage(dir, sx, sy, fw, fh, -dw / 2, -dh + bob, dw, dh);
        ctx.restore();"""
NEW_DRAW = """        // True directional frame from spritesheet (with flip when needed)
        if (flip) {
          ctx.scale(-1, 1);
        }
        if (tilt) ctx.rotate(tilt);
        ctx.drawImage(dir, sx, sy, fw, fh, -dw / 2, -dh + 3 + bob, dw, dh);
        ctx.restore();"""
if OLD_DRAW not in html:
    print("!! draw pattern missing"); sys.exit(1)
html = html.replace(OLD_DRAW, NEW_DRAW, 1)
print("[2b] grounded anchor + step tilt + bounce")

# shadow subtle (avoid double-shadow look)
OLD_SH = """        ctx.fillStyle = 'rgba(0,0,0,0.35)';
        ctx.beginPath();
        ctx.ellipse(0, 3, 10, 4, 0, 0, Math.PI * 2);
        ctx.fill();"""
# only replace the FIRST occurrence (agents) - boss avatar uses 4,12,5 pattern
first = html.find(OLD_SH)
if first < 0:
    print("!! shadow pattern missing"); sys.exit(1)
html = html[:first] + html[first:].replace(OLD_SH, """        ctx.fillStyle = 'rgba(0,0,0,0.22)';
        ctx.beginPath();
        ctx.ellipse(0, 4, 11, 3.6, 0, 0, Math.PI * 2);
        ctx.fill();""", 1)
print("[2c] subtle ground shadow")

# ---------- 3) STATIC NPCs ----------
NPC_BLOCK = """
// ===== STATIC OFFICE NPCs (Gate 10): idle sway + shuffles + mini dialogue =====
const staticNPCs = [
  { id: 'npc1', name: 'Intern Rei',   role: 'Trainee',     spr: 'cody',     x: 780,  y: 782, baseX: 780,  baseY: 782, facing: 'right', walkFrame: 0, isMoving: false, timer: 240 + Math.floor(Math.random()*300), phrase: 'Saan po ba ang meeting room? 🐣' },
  { id: 'npc2', name: 'HR Dana',      role: 'HR Manager',  spr: 'aria',     x: 430,  y: 420, baseX: 430,  baseY: 420, facing: 'down',  walkFrame: 0, isMoving: false, timer: 200 + Math.floor(Math.random()*300), phrase: 'Sino ang mag-lead ng 1:1s today? 📋' },
  { id: 'npc3', name: 'Barista Nia',  role: 'Pantry Barista', spr: 'pixel', x: 1130, y: 690, baseX: 1130, baseY: 690, facing: 'down',  walkFrame: 0, isMoving: false, timer: 180 + Math.floor(Math.random()*300), phrase: 'Bagong roast beans! Kumakanta sa espresso bar! ☕' },
  { id: 'npc4', name: 'Trainee Ben',  role: 'QA Intern',   spr: 'jax',      x: 620,  y: 600, baseX: 620,  baseY: 600, facing: 'left',  walkFrame: 0, isMoving: false, timer: 260 + Math.floor(Math.random()*300), phrase: 'Sana may bagong bug ako mahuli today! 🐛' },
  { id: 'npc5', name: 'Janitor Oli',  role: 'Facilities',  spr: 'marcus',   x: 1080, y: 600, baseX: 1080, baseY: 600, facing: 'left',  walkFrame: 0, isMoving: false, timer: 220 + Math.floor(Math.random()*300), phrase: 'Malinis na lahat ng server pods! 🧹' },
  { id: 'npc6', name: 'Security Sam', role: 'Front Desk',  spr: 'vanguard', x: 700,  y: 782, baseX: 700,  baseY: 782, facing: 'down',  walkFrame: 0, isMoving: false, timer: 300 + Math.floor(Math.random()*300), phrase: 'ID check po muna bago pumasok sa sound lab. 🛡️' },
  { id: 'npc7', name: 'Accountant Faye', role: 'Finance',  spr: 'echo',     x: 350,  y: 782, baseX: 350,  baseY: 782, facing: 'left',  walkFrame: 0, isMoving: false, timer: 250 + Math.floor(Math.random()*300), phrase: 'Budget ng studio: naka-beer mode na! 🍺' },
  { id: 'npc8', name: 'Agent Zed',    role: 'R&D',         spr: 'vortex',   x: 880,  y: 782, baseX: 880,  baseY: 782, facing: 'right', walkFrame: 0, isMoving: false, timer: 280 + Math.floor(Math.random()*300), phrase: 'Testing ng bagong shader! Cyan ang future. ⚡' }
];
function updateStaticNPCs() {
  for (const n of staticNPCs) {
    n.timer--;
    if (n.isMoving) {
      const dx = n.baseX + (n.shift || 0) - n.x;
      if (Math.abs(dx) < 2) { n.isMoving = false; n.x = n.baseX + (n.shift || 0); }
      else {
        n.facing = dx > 0 ? 'right' : 'left';
        n.walkFrame = (stepFrame % 10 === 0) ? (n.walkFrame + 1) % 3 : n.walkFrame;
        n.x += Math.sign(dx) * 0.85;
      }
    } else if (n.timer <= 0) {
      const roll = Math.random();
      if (roll < 0.5) {
        // mini dialogue bubble
        activeBubble = { agent: n, text: n.name + ': ' + n.phrase };
        bubbleTimer = 140;
        playSFX('blip');
        n.timer = 260 + Math.floor(Math.random() * 320);
      } else if (roll < 0.8 && !n.isMoving) {
        // small shuffle 24px to the side then back
        n.shift = (Math.random() < 0.5 ? -1 : 1) * 24;
        n.isMoving = true;
        n.timer = 220 + Math.floor(Math.random() * 240);
      } else {
        n.timer = 200 + Math.floor(Math.random() * 300);
      }
    }
  }
}
// ===== END STATIC NPCs =====
"""
# insert NPC block before "function updateSimulation()"
ANCHOR = "function updateSimulation() {"
if ANCHOR not in html:
    print("!! updateSimulation anchor missing"); sys.exit(1)
html = html.replace(ANCHOR, NPC_BLOCK + "\n" + ANCHOR, 1)
# call updateStaticNPCs at start of updateSimulation
html = html.replace("function updateSimulation() {\n  stepFrame++;", "function updateSimulation() {\n  stepFrame++;\n  updateStaticNPCs();", 1)
print("[3] static NPCs block + update hook")

# render static NPCs after agents loop: insert before "// 5. Draw Proportional Boss Avatar"
REN_ANCHOR = "    // 5. Draw Proportional Boss Avatar"
NPC_RENDER = """    // 4b. Draw Static Office NPCs
    for (const n of staticNPCs) {
      const ds = dirSprites[n.spr];
      if (ds && (ds.complete || ds.width > 0)) {
        const dwAll = ds.naturalWidth || ds.width;
        const dhAll = ds.naturalHeight || ds.height;
        const fw = dwAll / 3, fh = dhAll / 4;
        const ROW2 = { down: 0, up: 1, left: 2, right: 3 };
        let row = ROW2[n.facing] || 0;
        let flip = false;
        const frame = n.isMoving ? (1 + (n.walkFrame % 2)) : 0;
        const sx = frame * fw;
        const targetH = 34, scaleF = targetH / fh;
        const dw = fw * scaleF, dh = fh * scaleF;
        const bob = n.isMoving ? ((n.walkFrame % 2 === 0 ? -1 : 1) * 0.7) : Math.sin(stepFrame * 0.03 + n.x) * 0.3;
        ctx.save();
        ctx.translate(n.x, n.y);
        ctx.fillStyle = 'rgba(0,0,0,0.2)';
        ctx.beginPath(); ctx.ellipse(0, 4, 10, 3.4, 0, 0, Math.PI * 2); ctx.fill();
        const SIDE_N = { zillion:{left:2,right:'2f'}, marcus:{left:'2f',right:2}, aria:{left:2,right:'2f'}, cody:{left:2,right:3}, pixel:{left:'2f',right:2}, echo:{left:'2f',right:2}, vortex:{left:3,right:2}, jax:{left:2,right:'2f'}, vanguard:{left:3,right:2}, chronos:{left:'2f',right:2} };
        if (n.facing === 'right' || n.facing === 'left') {
          const m = (SIDE_N[n.spr] || { left: 2, right: '2f' })[n.facing];
          if (m === 2 || m === 3) { row = m; flip = false; } else { row = 2; flip = true; }
        }
        const sy2 = row * fh;
        if (flip) ctx.scale(-1, 1);
        ctx.drawImage(ds, sx, sy2, fw, fh, -dw / 2, -dh + 3 + bob, dw, dh);
        ctx.restore();
        ctx.fillStyle = 'rgba(255,255,255,0.85)';
        ctx.font = 'bold 8px monospace';
        ctx.shadowColor = '#000'; ctx.shadowBlur = 2;
        ctx.fillText(n.name, n.x - (n.name.length * 2.2), n.y + 10 + bob);
        ctx.shadowBlur = 0;
      }
    }

"""
if REN_ANCHOR not in html:
    print("!! render anchor missing"); sys.exit(1)
html = html.replace(REN_ANCHOR, NPC_RENDER + REN_ANCHOR, 1)
print("[4] NPC render inserted")

open(OUT, 'w', encoding='utf-8').write(html)
print(f"\nGATE10: {len(html)} bytes (+{len(html) - 11697784})")
