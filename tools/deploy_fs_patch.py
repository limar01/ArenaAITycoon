#!/usr/bin/env python3
"""
deploy_fs_patch.py - MOBILE FULLSCREEN patch for Arena AI Tycoon (runs ON PHONE).
- Canvas covers the whole phone screen (cover-fit, no letterbox bars).
- Render math becomes dynamic (canvas.width/height + fit scale).
- Keeps header/control/dialogue compact; game area flex-fills remaining space.
Creates backup index.html.bak_pre_fs before patching.
"""
import os, re, sys

BASE = os.path.expanduser('~/projects/hermes_game_studio/builds/arena_ai_simulator')
PATH = os.path.join(BASE, 'index.html')

html = open(PATH, encoding='utf-8').read()
orig = html

# ---------- 1) Render math replacements (world stays 1600x900, viewport becomes dynamic) ----------
REPLACEMENTS = [
    ("ctx.clearRect(0, 0, 1600, 900);",
     "ctx.clearRect(0, 0, canvas.width, canvas.height);"),
    ("const maxOffsetX = 800 * (1 - 1 / zoomScale);",
     "const maxOffsetX = 800 - (canvas.width / (2 * zoomScale * (window.__fitScale || 1)));"),
    ("const maxOffsetY = 450 * (1 - 1 / zoomScale);",
     "const maxOffsetY = 450 - (canvas.height / (2 * zoomScale * (window.__fitScale || 1)));"),
    ("ctx.translate(800, 450);",
     "ctx.translate(canvas.width / 2, canvas.height / 2);"),
    ("ctx.scale(zoomScale, zoomScale);",
     "ctx.scale(zoomScale * (window.__fitScale || 1), zoomScale * (window.__fitScale || 1));"),
]
report = []
for old, new in REPLACEMENTS:
    n = html.count(old)
    report.append(f"{old[:45]!r}: {n} hits")
    if n >= 1:
        html = html.replace(old, new, n)
    else:
        print("MISSING PATTERN:", old[:60]); 

# ---------- 2) Append FULLSCREEN layer (CSS overrides + JS) ----------
LAYER = r'''
<!-- ============ MOBILE FULLSCREEN COVER (Boss order) ============ -->
<style id="fs-css">
  html, body { height: 100% !important; margin: 0 !important; padding: 0 !important; overflow: hidden !important; }
  body { justify-content: flex-start !important; min-height: 0 !important; }
  #game-wrapper {
    width: 100% !important; max-width: none !important;
    height: 100dvh !important; height: 100vh !important;
    border: none !important; border-radius: 0 !important; box-shadow: none !important;
  }
  #retro-header, #control-bar { flex-wrap: nowrap !important; padding: 4px 8px !important; font-size: 10px !important; }
  .canvas-container { flex: 1 1 auto !important; min-height: 0 !important; width: 100% !important; }
  canvas#gameCanvas {
    width: 100% !important; height: 100% !important;
    aspect-ratio: auto !important; display: block !important;
  }
  #dialogue-container { margin: 4px !important; padding: 6px 10px !important; }
  @media (max-height: 560px) { #retro-header, #control-bar { display: none !important; } }
</style>
<script>
(function () {
  var canvas = document.getElementById('gameCanvas');
  function applyFit() {
    if (!canvas) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = canvas.clientWidth || window.innerWidth;
    var h = canvas.clientHeight || window.innerHeight;
    canvas.width = Math.max(2, Math.round(w * dpr));
    canvas.height = Math.max(2, Math.round(h * dpr));
    var WORLD_W = 1600, WORLD_H = 900;
    window.__fitScale = Math.max(canvas.width / WORLD_W, canvas.height / WORLD_H);
    document.documentElement.style.setProperty('--fs', window.__fitScale);
  }
  applyFit();
  window.addEventListener('resize', applyFit);
  window.addEventListener('orientationchange', function () { setTimeout(applyFit, 120); });
  document.addEventListener('DOMContentLoaded', applyFit);
  setTimeout(applyFit, 300);
  setTimeout(applyFit, 1200);
})();
</script>
</body>'''

# remove any previous FS layer (idempotent)
html = re.sub(r'<!-- ============ MOBILE FULLSCREEN COVER.*?</body>', '</body>', html, flags=re.S)
html = html.replace('</body>', LAYER, 1)

# ---------- 3) backup + write ----------
bak = os.path.join(BASE, 'index.html.bak_pre_fs')
if not os.path.exists(bak):
    open(bak, 'w', encoding='utf-8').write(orig)
    print("BACKUP -> index.html.bak_pre_fs", len(orig))
open(PATH, 'w', encoding='utf-8').write(html)
print("PATCHED -> index.html", len(html), "bytes")
print("\n".join(report))
print("FS layer count:", html.count('MOBILE FULLSCREEN COVER'))
print("__fitScale refs:", html.count('__fitScale'))
