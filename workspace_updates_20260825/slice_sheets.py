#!/usr/bin/env python3
"""
slice_sheets.py - Slice directional sprite sheets into 4-direction frame sets.
Sheet layout (per verified reference):
  Row 1: front (SOUTH/down) left 3 cells + back (NORTH/up) right 3 cells
  Row 2: leg crops -> SKIPPED
  Row 3: side (WEST/left) left 3 cells + side (mirror for right) right 3 cells
Output: 4-direction spritesheet PNG per character (4 rows x 3 cols, transparent).
"""
import sys, os, json
from PIL import Image
import numpy as np

try:
    from scipy import ndimage
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False

def is_bg(px):
    r, g, b = px[0], px[1], px[2]
    # white (#fff) or checker gray (#ccc..#ddd), low color
    if r > 200 and g > 200 and b > 200:
        return True
    if abs(r - g) < 14 and abs(g - b) < 14 and 175 < r < 240:
        return True
    return False

def flood_transparent(arr):
    """Make connected background transparent (flood from edges)."""
    h, w, _ = arr.shape
    bgmask = np.zeros((h, w), dtype=bool)
    for y in range(h):
        for x in range(w):
            if is_bg(arr[y, x]):
                bgmask[y, x] = True
    # BFS from borders over bgmask
    visited = np.zeros((h, w), dtype=bool)
    from collections import deque
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if bgmask[y, x] and not visited[y, x]:
                visited[y, x] = True; dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if bgmask[y, x] and not visited[y, x]:
                visited[y, x] = True; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for ny, nx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
            if 0 <= ny < h and 0 <= nx < w and bgmask[ny, nx] and not visited[ny, nx]:
                visited[ny, nx] = True; dq.append((ny, nx))
    out = arr.copy()
    out[visited] = [0, 0, 0, 0]
    return out

def detect_cells(path):
    im = Image.open(path).convert('RGB')
    a = np.array(im)
    h, w, _ = a.shape
    gray = a.mean(axis=2)
    sat = a.max(axis=2).astype(int) - a.min(axis=2).astype(int)
    mask = (gray < 120) | (sat > 40)
    if HAVE_SCIPY:
        lab, n = ndimage.label(mask)
        cells = []
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            if len(ys) < 500:
                continue
            x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
            cw, ch = x1 - x0, y1 - y0
            # skip giant grid/border components (spans whole panel)
            if cw > 400 or ch > 460:
                continue
            # character cells: ~90x220; leg crops ~85x90
            if not (40 < cw < 320 and 40 < ch < 300):
                continue
            cells.append((x0, y0, x1, y1, len(ys)))
        return im, a, cells
    return im, a, []

def slice_sheet(path, out_dir, tag_probe=None):
    im, a, cells = detect_cells(path)
    if not cells:
        return None
    # sort into rows by y0 (gap threshold 100)
    cells.sort(key=lambda c: (c[1], c[0]))
    rows = []
    cur = [cells[0]]
    for c in cells[1:]:
        if c[1] - cur[0][1] < 100:
            cur.append(c)
        else:
            rows.append(cur); cur = [c]
    rows.append(cur)
    # drop leg-crop rows (avg height < 150)
    tall = []
    for row in rows:
        avg_h = sum(c[4] - c[2] for c in row) / len(row)
        if avg_h > 150:
            tall.append(row)
    rows = tall
    rows.sort(key=lambda r: r[0][1])
    info = []
    for ri, row in enumerate(rows):
        row.sort(key=lambda c: c[0])
        info.append([(c[0], c[1], c[2], c[3]) for c in row])
    return im, a, info

def compose_character(name, src_path, out_path):
    res = slice_sheet(src_path, None)
    if res is None:
        return None
    im, a, rows = res
    # Expect >= 3 rows; use row0 (front+back), row1 (skip legs), row2 (side)
    # row with most cells = row0/row2 typically 6; legs row may have 6 too (crops)
    # Identify: row2 present? use last row as side, first row as front/back
    front_back = rows[0]
    side_row = rows[-1] if len(rows) >= 3 else rows[0]
    # front = left 3, back = right 3 (of front_back by x)
    front_back.sort(key=lambda c: c[0])
    if len(front_back) >= 6:
        frontc = front_back[0:3]
        backc = front_back[3:6]
    else:
        frontc = front_back[:3]
        backc = front_back[:3][::-1]
    side_row.sort(key=lambda c: c[0])
    sidec = side_row[:3]
    if len(sidec) < 3:
        sidec = side_row
    def crop(bb, pad=4):
        x0, y0, x1, y1 = bb
        x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
        x1 = min(a.shape[1], x1 + pad); y1 = min(a.shape[0], y1 + pad)
        cell = a[y0:y1, x0:x1].copy()
        rgba = np.dstack([cell, np.full((cell.shape[0], cell.shape[1]), 255, dtype=cell.dtype)])
        return flood_transparent(rgba)
    frames = {'down': [], 'up': [], 'left': []}
    for bb in frontc: frames['down'].append(crop(bb))
    for bb in backc: frames['up'].append(crop(bb))
    for bb in sidec: frames['left'].append(crop(bb))
    # trim each frame to content bbox first
    trimmed = {}
    for d in ('down', 'up', 'left'):
        trimmed[d] = []
        for arr in frames[d]:
            img = Image.fromarray(arr)
            alpha = np.array(img)[:, :, 3]
            if alpha.any():
                ys, xs = np.where(alpha > 8)
                img = img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
            trimmed[d].append(img)
    all_frames = trimmed['down'] + trimmed['up'] + trimmed['left']
    cw = max(im.width for im in all_frames) + 4
    ch = max(im.height for im in all_frames) + 6
    sheet = Image.new('RGBA', (cw * 3, ch * 4), (0, 0, 0, 0))
    dirs = ['down', 'up', 'left', 'right']
    for di, d in enumerate(dirs):
        for fi in range(3):
            img = trimmed['left'][fi] if d == 'right' else trimmed[d][fi]
            cell = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
            ax = (cw - img.width) // 2
            ay = ch - img.height - 2
            cell.paste(img, (ax, ay), img)
            sheet.paste(cell, (fi * cw, di * ch))
    sheet.save(out_path, optimize=True)
    return {'name': name, 'out': out_path, 'size': [sheet.width, sheet.height], 'cell': [cw, ch],
            'down': [f.shape[:2] for f in frames['down']],
            'up': [f.shape[:2] for f in frames['up']],
            'left': [f.shape[:2] for f in frames['left']]}

if __name__ == '__main__':
    os.makedirs('/home/user/dir_frames', exist_ok=True)
    jobs = [
        ('zillion', '/home/user/images/sprite_opt1_director.png'),
        ('cody', '/home/user/images/sprite_opt2_programmer.png'),
        ('aria', '/home/user/images/sprite_opt3_designer.png'),
        ('pixel', '/home/user/images/sprite_opt4_artist.png'),
        ('jax', '/home/user/images/sprite_opt5_qa_auditor.png'),
    ]
    meta = {}
    for name, src in jobs:
        try:
            r = compose_character(name, src, f'/home/user/dir_frames/{name}_dir.png')
            if r:
                meta[name] = r
                print(f"[OK] {name}: sheet {r['size']} cell {r['cell']} down={r['down']} up={r['up']} left={r['left']}")
            else:
                print(f"[FAIL] {name}: no cells detected")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
    json.dump(meta, open('/home/user/dir_frames/meta.json', 'w'), indent=1)
    print("meta saved")
