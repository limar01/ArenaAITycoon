#!/usr/bin/env python3
"""
patch_gate7.py - ANIMATION POLISH (direction fix + walk speed + idle breathing).
Reads live.html, writes gate7.html.
1) Side-direction fix: characters without a distinct RIGHT row get right=left-flipped.
   NATIVE_RIGHT (has real right row): cody, vortex, vanguard. Everyone else flips row2.
2) Walk cycle throttle: frame advance every 9 steps (was every frame = too fast).
3) Idle breathing: subtle 0.5px bob (no jumps).
"""
import os, sys, re

SRC = '/home/user/_gate7/live.html'
OUT = '/home/user/_gate7/gate7.html'

html = open(SRC, encoding='utf-8').read()
orig_len = len(html)

# ---------- 1) Walk cycle throttle in updateSimulation ----------
OLD_WALK = "      a.isMoving = true;\n      a.walkFrame = (a.walkFrame + 1) % 3;"
NEW_WALK = """      a.isMoving = true;
      if (stepFrame % 9 === 0) a.walkFrame = (a.walkFrame + 1) % 3;"""
if OLD_WALK not in html:
    print("!! walk throttle pattern MISSING"); sys.exit(1)
html = html.replace(OLD_WALK, NEW_WALK, 1)
print("[1] Walk frame throttle (every 9 frames)")

# ---------- 2) Renderer: directional rows + flip + breathing ----------
OLD_REN = """        const ROW = { down: 0, up: 1, left: 2, right: 3 };
        const row = (ROW[a.facing] !== undefined) ? ROW[a.facing] : 0;
        const fw = dir.naturalWidth / 3;
        const fh = dir.naturalHeight / 4;
        const moving = !!a.isMoving;
        // frame 0 = stand/idle; frames 1-2 = walk steps
        const frame = moving ? (1 + (a.walkFrame % 2)) : 0;
        const sx = frame * fw;
        const sy = row * fh;
        const targetH = 34;
        const scaleF = targetH / fh;
        const dw = fw * scaleF;
        const dh = fh * scaleF;
        const bob = moving ? Math.sin((a.walkFrame % 3) * Math.PI) * 1.4 : 0;

        ctx.save();
        ctx.translate(a.x, a.y);

        // Shadow ellipse
        ctx.fillStyle = 'rgba(0,0,0,0.35)';
        ctx.beginPath();
        ctx.ellipse(0, 3, 10, 4, 0, 0, Math.PI * 2);
        ctx.fill();

        // True directional frame from spritesheet
        ctx.drawImage(dir, sx, sy, fw, fh, -dw / 2, -dh + bob, dw, dh);
        ctx.restore();"""

NEW_REN = """        const ROW = { down: 0, up: 1, left: 2, right: 3 };
        // characters with a genuine RIGHT row (verified via orientation analysis);
        // everyone else: RIGHT = LEFT row horizontally flipped (always correct direction)
        const NATIVE_RIGHT = { cody: 1, vortex: 1, vanguard: 1 };
        let row = (ROW[a.facing] !== undefined) ? ROW[a.facing] : 0;
        let flip = false;
        if (a.facing === 'right') {
          if (NATIVE_RIGHT[a.id]) { row = 3; }
          else { row = 2; flip = true; }
        } else if (a.facing === 'left') {
          row = 2; flip = false;
        }
        const fw = dir.naturalWidth / 3;
        const fh = dir.naturalHeight / 4;
        const moving = !!a.isMoving;
        // frame 0 = stand/idle; frames 1-2 = walk steps
        const frame = moving ? (1 + (a.walkFrame % 2)) : 0;
        const sx = frame * fw;
        const sy = row * fh;
        const targetH = 34;
        const scaleF = targetH / fh;
        const dw = fw * scaleF;
        const dh = fh * scaleF;
        // breathing when idle (<=0.5px, no jumps); gentle walk bob when moving
        const bob = moving ? Math.sin((a.walkFrame % 3) * Math.PI) * 1.2
                           : Math.sin(stepFrame * 0.035 + a.x * 0.05) * 0.5;

        ctx.save();
        ctx.translate(a.x, a.y);

        // Shadow ellipse
        ctx.fillStyle = 'rgba(0,0,0,0.35)';
        ctx.beginPath();
        ctx.ellipse(0, 3, 10, 4, 0, 0, Math.PI * 2);
        ctx.fill();

        // True directional frame from spritesheet (with flip when needed)
        if (flip) {
          ctx.translate(0, 0);
          ctx.scale(-1, 1);
        }
        ctx.drawImage(dir, sx, sy, fw, fh, -dw / 2, -dh + bob, dw, dh);
        ctx.restore();"""
if OLD_REN not in html:
    print("!! render direction pattern MISSING"); sys.exit(1)
html = html.replace(OLD_REN, NEW_REN, 1)
print("[2] Direction fix (NATIVE_RIGHT flip) + idle breathing")

open(OUT, 'w', encoding='utf-8').write(html)
print(f"\nGATE7 PATCHED: {orig_len} -> {len(html)} (+{len(html)-orig_len})")
