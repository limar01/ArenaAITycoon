#!/usr/bin/env python3
"""
deploy_fs_patch2.py - Fix pointer/pan math for FULLSCREEN COVER mode (runs ON PHONE).
1) handleCanvasTap: screen -> world conversion now uses dynamic canvas size + fitScale.
2) touchmove/mousemove pan deltas: same fix.
Backup: index.html.bak_pre_fs2
"""
import os, sys

BASE = os.path.expanduser('~/projects/hermes_game_studio/builds/arena_ai_simulator')
PATH = os.path.join(BASE, 'index.html')
html = open(PATH, encoding='utf-8').read()
orig = html

# ---------- 1) TAP conversion ----------
OLD_TAP = """  const rect = canvas.getBoundingClientRect();
  const rawX = (clientX - rect.left) * (1600 / rect.width);
  const rawY = (clientY - rect.top) * (900 / rect.height);

  let clickX = rawX;
  let clickY = rawY;

  if (zoomScale > 1.0) {
    const maxOffsetX = 800 - (canvas.width / (2 * zoomScale * (window.__fitScale || 1)));
    const maxOffsetY = 450 - (canvas.height / (2 * zoomScale * (window.__fitScale || 1)));
    let cx = Math.max(800 - maxOffsetX, Math.min(800 + maxOffsetX, camX));
    let cy = Math.max(450 - maxOffsetY, Math.min(450 + maxOffsetY, camY));
    clickX = (rawX - 800) / zoomScale + cx;
    clickY = (rawY - 450) / zoomScale + cy;
  }"""

NEW_TAP = """  const rect = canvas.getBoundingClientRect();
  const px = (clientX - rect.left) * (canvas.width / rect.width);
  const py = (clientY - rect.top) * (canvas.height / rect.height);
  const zoomFull = zoomScale * (window.__fitScale || 1);
  const coX = 800 - (canvas.width / (2 * zoomFull));
  const coY = 450 - (canvas.height / (2 * zoomFull));
  const ccx = Math.max(800 - coX, Math.min(800 + coX, camX));
  const ccy = Math.max(450 - coY, Math.min(450 + coY, camY));
  const clickX = (px - canvas.width / 2) / zoomFull + ccx;
  const clickY = (py - canvas.height / 2) / zoomFull + ccy;"""

n_tap = html.count(OLD_TAP)
print("TAP block hits:", n_tap)
if n_tap >= 1:
    html = html.replace(OLD_TAP, NEW_TAP, n_tap)

# ---------- 2) PAN delta conversion ----------
OLD_PAN_X = "* (1600 / canvas.clientWidth) / zoomScale"
OLD_PAN_Y = "* (900 / canvas.clientHeight) / zoomScale"
NEW_PAN_X = "* (canvas.width / canvas.clientWidth) / (zoomScale * (window.__fitScale || 1))"
NEW_PAN_Y = "* (canvas.height / canvas.clientHeight) / (zoomScale * (window.__fitScale || 1))"
nx = html.count(OLD_PAN_X); ny = html.count(OLD_PAN_Y)
print("PAN X hits:", nx, " PAN Y hits:", ny)
if nx >= 1: html = html.replace(OLD_PAN_X, NEW_PAN_X, nx)
if ny >= 1: html = html.replace(OLD_PAN_Y, NEW_PAN_Y, ny)

if n_tap == 0 or nx == 0 or ny == 0:
    print("WARNING: some patterns not found - verify manually")
else:
    bak = os.path.join(BASE, 'index.html.bak_pre_fs2')
    if not os.path.exists(bak):
        open(bak, 'w', encoding='utf-8').write(orig)
        print("BACKUP -> index.html.bak_pre_fs2", len(orig))
    open(PATH, 'w', encoding='utf-8').write(html)
    print("PATCH2 OK -> index.html", len(html), "bytes")
