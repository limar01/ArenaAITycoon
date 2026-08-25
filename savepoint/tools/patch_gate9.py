#!/usr/bin/env python3
"""
patch_gate9.py - WALL COLLISION + A* PATHFINDING (Boss QA: tumatagos sa dingding).
Reads _g9/index.html (Gate 8 live), writes _g9/gate9.html.
"""
import os, re, sys

SRC = '/home/user/_g9/index.html'
OUT = '/home/user/_g9/gate9.html'

html = open(SRC, encoding='utf-8').read()

# ---------- 1) Load collision grid ----------
grid_lines = [l.strip() for l in open('/home/user/_g9/collision_grid20.txt').read().split('\n') if l.strip()]
COLS = len(grid_lines[0]); ROWS = len(grid_lines)
assert all(len(l) == COLS for l in grid_lines), "grid rows inconsistent"
print(f"grid: {COLS}x{ROWS}")

# ---------- 2) Insert WALL_GRID + findPath after waypoints const ----------
ANCHOR = "// 10 Proportional Studio Agents with Directional Walking State"
PATH_CODE = """// ===== WALL COLLISION + A* PATHFINDING (Gate 9) =====
const WALL_GRID = [
"""
for l in grid_lines:
    PATH_CODE += '  "' + l + '",\n'
PATH_CODE += """];
const GRID_CW = 20, GRID_CH = 20, GRID_COLS = %d, GRID_ROWS = %d;

function gridBlocked(cx, cy) {
  if (cx < 0 || cx >= GRID_COLS || cy < 0 || cy >= GRID_ROWS) return true;
  return WALL_GRID[cy][cx] === '#';
}

function findPath(sx, sy, tx, ty) {
  const sc = [Math.max(0, Math.min(GRID_COLS - 1, Math.floor(sx / GRID_CW))), Math.max(0, Math.min(GRID_ROWS - 1, Math.floor(sy / GRID_CH)))];
  const gc = [Math.max(0, Math.min(GRID_COLS - 1, Math.floor(tx / GRID_CW))), Math.max(0, Math.min(GRID_ROWS - 1, Math.floor(ty / GRID_CH)))];
  if (gridBlocked(gc[0], gc[1])) return null;
  const key = (c) => c[0] + ',' + c[1];
  const openQ = [[0, sc]];
  const came = {};
  const gScore = {};
  gScore[key(sc)] = 0;
  const h = (c) => Math.abs(c[0] - gc[0]) + Math.abs(c[1] - gc[1]);
  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  const seen = new Set([key(sc)]);
  let found = null;
  while (openQ.length) {
    let best = 0;
    for (let i = 1; i < openQ.length; i++) if (openQ[i][0] < openQ[best][0]) best = i;
    const [f, cur] = openQ.splice(best, 1)[0];
    if (cur[0] === gc[0] && cur[1] === gc[1]) { found = cur; break; }
    for (const [dc, dr] of dirs) {
      const nc = [cur[0] + dc, cur[1] + dr];
      const k = key(nc);
      if (seen.has(k) || gridBlocked(nc[0], nc[1])) continue;
      seen.add(k);
      const ng = (gScore[key(cur)] || 0) + 1;
      gScore[k] = ng;
      came[k] = cur;
      openQ.push([ng + h(nc), nc]);
    }
  }
  if (!found) return null;
  const path = [found];
  let cur = found;
  while (came[key(cur)] !== undefined) { cur = came[key(cur)]; path.push(cur); }
  path.reverse();
  return path.slice(1).map(c => [(c[0] + 0.5) * GRID_CW, (c[1] + 0.5) * GRID_CH]);
}
// ===== END WALL COLLISION =====

""" % (COLS, ROWS)

if ANCHOR not in html:
    print("!! ANCHOR not found"); sys.exit(1)
html = html.replace(ANCHOR, PATH_CODE + ANCHOR, 1)
print("[1] WALL_GRID + findPath inserted")

# ---------- 3) Rewrite movement block ----------
OLD_MOV = """    const dx = target.x - a.x;
    const dy = target.y - a.y;
    const dist = Math.hypot(dx, dy);

    if (dist < 4) {
      a.wp = a.targetWp;
      a.x = target.x;
      a.y = target.y;
      a.isMoving = false;
      a.walkFrame = 0;

      if (Math.random() < 0.25) {
        a.waitTimer = 120 + Math.floor(Math.random() * 180);
      }

      const currentWpObj = waypoints[a.wp];
      const nextNeighbors = currentWpObj.neighbors;
      a.targetWp = nextNeighbors[Math.floor(Math.random() * nextNeighbors.length)];
    } else {
      // Direction Vector Tracking
      if (Math.abs(dx) > Math.abs(dy)) {
        a.facing = dx > 0 ? 'right' : 'left';
      } else {
        a.facing = dy > 0 ? 'down' : 'up';
      }
      a.isMoving = true;
      if (stepFrame % 9 === 0) a.walkFrame = (a.walkFrame + 1) % 3;

      a.x += (dx / dist) * a.speed;
      a.y += (dy / dist) * a.speed;
    }"""

NEW_MOV = """    const dx = target.x - a.x;
    const dy = target.y - a.y;
    const dist = Math.hypot(dx, dy);

    if (dist < 4) {
      a.wp = a.targetWp;
      a.x = target.x;
      a.y = target.y;
      a.isMoving = false;
      a.walkFrame = 0;
      a.path = null;

      if (Math.random() < 0.25) {
        a.waitTimer = 120 + Math.floor(Math.random() * 180);
      }

      const currentWpObj = waypoints[a.wp];
      const nextNeighbors = currentWpObj.neighbors;
      a.targetWp = nextNeighbors[Math.floor(Math.random() * nextNeighbors.length)];
    } else {
      // Wall-aware pathing: follow A* grid path, never cross walls
      if (!a.path) a.path = findPath(a.x, a.y, target.x, target.y);
      let mx = dx, my = dy;
      if (a.path && a.path.length) {
        const node = a.path[0];
        mx = node[0] - a.x; my = node[1] - a.y;
        if (Math.hypot(mx, my) < 5) { a.path.shift(); mx = dx; my = dy; }
      }
      const mdist = Math.hypot(mx, my) || 1;
      // Direction Vector Tracking
      if (Math.abs(mx) > Math.abs(my)) {
        a.facing = mx > 0 ? 'right' : 'left';
      } else {
        a.facing = my > 0 ? 'down' : 'up';
      }
      a.isMoving = true;
      if (stepFrame % 9 === 0) a.walkFrame = (a.walkFrame + 1) % 3;

      a.x += (mx / mdist) * a.speed;
      a.y += (my / mdist) * a.speed;
    }"""

if OLD_MOV not in html:
    print("!! movement block not found"); sys.exit(1)
html = html.replace(OLD_MOV, NEW_MOV, 1)
print("[2] Movement -> wall-aware pathing")

# ---------- 4) agents need path field ----------
html = html.replace("{ id: 'zillion', name: 'Zillion', role: 'Tech Director', wp: 'exec_hq', targetWp: 'central_cross_1', x: 350, y: 420, speed: 1.1, waitTimer: 0,",
                    "{ id: 'zillion', name: 'Zillion', role: 'Tech Director', wp: 'exec_hq', targetWp: 'central_cross_1', x: 350, y: 420, speed: 1.1, waitTimer: 0, path: null,", 1)
print("[3] agents.path field on zillion (others default undefined -> falsy works)")

open(OUT, 'w', encoding='utf-8').write(html)
print(f"\nGATE9: {len(html)} bytes (+{len(html.replace(PATH_CODE,''))} ... written)")
