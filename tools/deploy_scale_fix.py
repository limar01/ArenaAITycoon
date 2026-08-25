#!/usr/bin/env python3
"""
deploy_scale_fix.py - SPRITE SCALE + ZOOM + SPEECH BUBBLE fix.
Usage (phone):  python3 deploy_scale_fix.py
Usage (local):  python3 deploy_scale_fix.py <infile> <outfile>
Boss QA: sprites masyadong malaki vs background NPCs; sobrang zoomed sa portrait;
speech bubble malaki sobra.
"""
import os, sys

if len(sys.argv) >= 3:
    PATH = sys.argv[2]; MODE = "local"; SRC = sys.argv[1]
    html = open(SRC, encoding='utf-8').read()
    orig = html
else:
    BASE = os.path.expanduser('~/projects/hermes_game_studio/builds/arena_ai_simulator')
    PATH = os.path.join(BASE, 'index.html'); MODE = "phone"
    html = open(PATH, encoding='utf-8').read()
    orig = html

REPORT = []
def rep(old, new, label):
    n = html.count(old)
    REPORT.append(f"{label}: {n}x")
    if n >= 1:
        return html.replace(old, new, n)
    print(f"!! MISSING {label}")
    return html

# 1) SPRITE HEIGHT -> NPC scale match (46 -> 34)
html = rep("const targetH = 46;", "const targetH = 34;", "targetH 46->34")

# 2) ZOOM DEFAULTS -> wider view
html = rep("let zoomScale = 1.4;", "let zoomScale = 1.0;", "zoom default->1.0")
html = rep("let initialZoom = 1.4;", "let initialZoom = 1.0;", "initialZoom->1.0")
html = rep("zoomScale = 1.4;", "zoomScale = 1.0;", "resetZoom->1.0")
html = rep('zoomDisp.innerText = "1.4x";', 'zoomDisp.innerText = "1.0x";', "zoomDisp->1.0x")
html = rep('>1.4x</span>', '>1.0x</span>', "zoomDisp HTML->1.0x")

# 3) PORTRAIT AUTO-FIT (in FS applyFit)
OLD_FIT = "window.__fitScale = Math.max(canvas.width / WORLD_W, canvas.height / WORLD_H);"
NEW_FIT = """window.__fitScale = Math.max(canvas.width / WORLD_W, canvas.height / WORLD_H);
    if (window.innerHeight > window.innerWidth && typeof zoomScale === 'number') {
      zoomScale = 1.0;
      var zd = document.getElementById('zoom-disp');
      if (zd) zd.innerText = '1.0x';
    }"""
html = rep(OLD_FIT, NEW_FIT, "portrait auto zoom")

# 4) SPEECH BUBBLE -> compact
OLD_BUBBLE = """      const bx = Math.max(20, Math.min(1380, ag.x - 100));
      const by = Math.max(20, ag.y - 75);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.96)';
      ctx.fillRect(bx, by, 210, 34);
      ctx.strokeStyle = '#182848';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(bx, by, 210, 34);

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.moveTo(ag.x - 4, by + 34);
      ctx.lineTo(ag.x + 4, by + 34);
      ctx.lineTo(ag.x, by + 42);
      ctx.fill();

      ctx.fillStyle = '#000000';
      ctx.font = 'bold 10px monospace';
      ctx.fillText(ag.name + ":", bx + 6, by + 13);
      ctx.font = '9px monospace';
      ctx.fillText(activeBubble.text.substring(0, 34), bx + 6, by + 27);"""
NEW_BUBBLE = """      const bx = Math.max(14, Math.min(1402, ag.x - 78));
      const by = Math.max(14, ag.y - 58);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
      ctx.fillRect(bx, by, 162, 24);
      ctx.strokeStyle = '#182848';
      ctx.lineWidth = 1.2;
      ctx.strokeRect(bx, by, 162, 24);

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.moveTo(ag.x - 3, by + 24);
      ctx.lineTo(ag.x + 3, by + 24);
      ctx.lineTo(ag.x, by + 30);
      ctx.fill();

      ctx.fillStyle = '#000000';
      ctx.font = 'bold 8px monospace';
      ctx.fillText(ag.name + ":", bx + 5, by + 10);
      ctx.font = '8px monospace';
      ctx.fillText(activeBubble.text.substring(0, 26), bx + 5, by + 20);"""
html = rep(OLD_BUBBLE, NEW_BUBBLE, "speech bubble compact")

print("\n".join(REPORT))
print("MODE:", MODE, "->", PATH)

if MODE == "phone":
    bak = os.path.join(os.path.expanduser('~/projects/hermes_game_studio/builds/arena_ai_simulator'), 'index.html.bak_pre_scale')
    if not os.path.exists(bak):
        open(bak, 'w', encoding='utf-8').write(orig)
        print("BACKUP -> index.html.bak_pre_scale", len(orig))
    open(PATH, 'w', encoding='utf-8').write(html)
    print("PATCHED -> index.html", len(html), "bytes (+%d)" % (len(html) - len(orig)))
else:
    open(SRC + '.patched', 'w', encoding='utf-8').write(html)
    print("LOCAL OUT ->", SRC + '.patched', len(html), "bytes (+%d)" % (len(html) - len(orig)))
