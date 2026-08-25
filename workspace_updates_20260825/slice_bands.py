#!/usr/bin/env python3
"""
slice_bands.py - Robust per-sheet directional slicer using ROW BANDS + COLUMN PROJECTION.
Output: per-character 4-direction sheets (rows: down, left, right, up) x 3 frames, transparent, content-trimmed.
"""
import os, json, sys
from PIL import Image
import numpy as np
from collections import deque

def load_rgba(path):
    im = Image.open(path).convert('RGBA')
    return np.array(im)

def edge_bg_colors(a):
    """Sample background colors from band edges."""
    h, w, _ = a.shape
    sample = []
    for x in range(0, w, max(1, w // 40)):
        for y in (0, 1, h - 2, h - 1):
            px = a[y, x]
            sample.append((int(px[0]), int(px[1]), int(px[2])))
    for y in range(0, h, max(1, h // 40)):
        for x in (0, 1, w - 2, w - 1):
            px = a[y, x]
            sample.append((int(px[0]), int(px[1]), int(px[2])))
    return sample

def modal_bg(x0, y0, x1, y1):
    """Modal color from border pixels of a crop region, returns (r,g,b)."""
    im = Image.open(Path_IMG).convert('RGB') if False else None
    return None

def bg_mask(a, tol=22):
    h, w, _ = a.shape
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    # 1) white / light neutral (checkerboard shades)
    white = (r > 210) & (g > 210) & (b > 210)
    light_neutral = (np.abs(r - g) < 12) & (np.abs(g - b) < 12) & (r > 170) & (r < 255)
    # 2) dominant border color (mode via median)
    border_px = np.concatenate([a[0, :, :3], a[-1, :, :3], a[:, 0, :3], a[:, -1, :3]]).astype(int)
    med = np.median(border_px, axis=0)
    d = (r - med[0]) ** 2 + (g - med[1]) ** 2 + (b - med[2]) ** 2
    close = d < tol * tol
    return white | light_neutral | close

def flood_transparent(a):
    m = bg_mask(a)
    h, w = m.shape
    vis = np.zeros((h, w), dtype=bool)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if m[y, x] and not vis[y, x]:
                vis[y, x] = True; dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if m[y, x] and not vis[y, x]:
                vis[y, x] = True; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for ny, nx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
            if 0 <= ny < h and 0 <= nx < w and not vis[ny, nx] and m[ny, nx]:
                vis[ny, nx] = True; dq.append((ny, nx))
    out = a.copy()
    out[vis] = [0, 0, 0, 0]
    return out

def frame_columns(band, min_w=14, gap=6):
    """band: RGBA array with bg already transparent. Return list of (x0,x1) frame columns."""
    alpha = band[:, :, 3]
    colsum = (alpha > 16).sum(axis=0)
    cols = colsum > 0
    segs = []
    start = None
    gap_run = 0
    for x in range(len(cols)):
        if cols[x]:
            if start is None:
                start = x
            gap_run = 0
        else:
            if start is not None:
                gap_run += 1
                if gap_run >= gap:
                    segs.append((start, x - gap_run + 1))
                    start = None
    if start is not None:
        segs.append((start, len(cols) - 1))
    segs = [s for s in segs if (s[1] - s[0]) >= min_w]
    return segs

def trim_alpha(img):
    a = np.array(img)[:, :, 3]
    if not a.any():
        return img
    ys, xs = np.where(a > 8)
    return img.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))

def slice_band(src_arr, x0, x1, y0, y1):
    band = src_arr[y0:y1, x0:x1].copy()
    band = flood_transparent(band)
    segs = frame_columns(band)
    frames = []
    for (a, b) in segs:
        cell = band[:, a:b]
        img = Image.fromarray(cell)
        frames.append(trim_alpha(img))
    return frames

def build_sheet(frames_by_dir, out_path, max_h=170):
    """frames_by_dir: {'down':[3 imgs], 'left':[...], 'right':[...], 'up':[...]}"""
    dirs = ['down', 'left', 'right', 'up']
    cw = max(max((f.width for f in frames_by_dir[d]), default=10) for d in dirs) + 4
    ch = max(max((f.height for f in frames_by_dir[d]), default=10) for d in dirs) + 6
    ch = min(ch, max_h + 6)
    sheet = Image.new('RGBA', (cw * 3, ch * 4), (0, 0, 0, 0))
    for di, d in enumerate(dirs):
        fs = frames_by_dir.get(d) or []
        for fi in range(3):
            img = fs[fi] if fi < len(fs) else fs[0]
            if img is None:
                continue
            if img.height > max_h:
                r = max_h / img.height
                img = img.resize((max(1, int(img.width * r)), max_h), Image.LANCZOS)
            cell = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
            ax = (cw - img.width) // 2
            ay = ch - img.height - 2
            cell.paste(img, (ax, ay), img)
            sheet.paste(cell, (fi * cw, di * ch))
    sheet.save(out_path, optimize=True)
    return sheet, cw, ch

SPECS = {
    # name: (src, [ (dir, x0, x1, y0, y1) , ... ] rows top->bottom)
    'zillion': ('images/sprite_opt1_director.png', [
        ('down', 20, 645, 55, 310),
        ('up', 700, 1400, 55, 310),
        ('left', 20, 645, 500, 762),
        ('right', 700, 1400, 500, 762),
    ]),
    # exact cell boxes (found via component detection; grid panels excluded)
    'zillion_cells': ('images/sprite_opt1_director.png', {
        'down': [(79, 71, 171, 292), (285, 71, 385, 292), (478, 71, 584, 292)],
        'up': [(827, 71, 920, 292), (1026, 71, 1124, 292), (1228, 73, 1325, 292)],
        'left': [(85, 522, 174, 743), (276, 522, 385, 743), (485, 522, 593, 743)],
        'right': [(825, 522, 914, 743), (1022, 522, 1132, 743), (1229, 522, 1338, 743)],
    }),
    'cody': ('images/sprite_opt2_programmer.png', [
        ('down', 180, 1360, 85, 270),
        ('up', 180, 1360, 255, 430),
        ('right', 180, 1360, 425, 595),
        ('left', 180, 1360, 580, 760),
    ]),
    'aria': ('images/sprite_opt3_designer.png', [
        ('down', 60, 1390, 106, 216),
        ('up', 60, 1390, 218, 322),
        ('left', 60, 1390, 325, 428),
        ('right', 60, 1390, 430, 540),
    ]),
    'pixel': ('images/sprite_opt4_artist.png', [
        ('down', 250, 1200, 40, 235),
        ('left', 250, 1200, 230, 405),
        ('right', 250, 1200, 405, 585),
        ('up', 250, 1200, 585, 765),
    ]),
    'jax': ('images/sprite_opt5_qa_auditor.png', [
        ('down', 150, 1400, 75, 240),
        ('up', 150, 1400, 240, 415),
        ('right', 150, 1400, 450, 600),
        ('left', 150, 1400, 620, 768),
    ]),
}

def process(name, src, rows, outdir):
    a = load_rgba(src)
    frames_by_dir = {}
    for d, x0, x1, y0, y1 in rows:
        fs = slice_band(a, x0, x1, y0, y1)
        if len(fs) < 3:
            print(f"  [warn] {name}/{d}: only {len(fs)} frames")
        frames_by_dir[d] = fs[:3]
    sheet, cw, ch = build_sheet(frames_by_dir, f'{outdir}/{name}_dir.png')
    return {'cw': cw, 'ch': ch, 'frames': {d: len(fs) for d, fs in frames_by_dir.items()},
            'sizes': {d: [f.size for f in fs[:3]] for d, fs in frames_by_dir.items()}}

def process_cells(name, src, boxes, outdir):
    a = load_rgba(src)
    frames_by_dir = {}
    for d, cells in boxes.items():
        fs = []
        for (x0, y0, x1, y1) in cells:
            cell = a[y0:y1, x0:x1].copy()
            cell = flood_transparent(cell)
            img = Image.fromarray(cell)
            fs.append(trim_alpha(img))
        frames_by_dir[d] = fs
    sheet, cw, ch = build_sheet(frames_by_dir, f'{outdir}/{name}_dir.png')
    return {'cw': cw, 'ch': ch, 'frames': {d: len(fs) for d, fs in frames_by_dir.items()},
            'sizes': {d: [f.size for f in fs[:3]] for d, fs in frames_by_dir.items()}}

def process_grid(name, src, cols_x, w, rows_y, ncols=3, outdir=None):
    """cols_x: list of x0; rows_y: dict dir->(y0, h)."""
    a = load_rgba(src)
    frames_by_dir = {}
    for d, (y0, h) in rows_y.items():
        fs = []
        for i in range(min(ncols, len(cols_x))):
            x0 = cols_x[i]
            cell = a[y0:y0 + h, x0:x0 + w].copy()
            cell = flood_transparent(cell)
            img = Image.fromarray(cell)
            fs.append(trim_alpha(img))
        frames_by_dir[d] = fs
    sheet, cw, ch = build_sheet(frames_by_dir, f'{outdir or "/home/user/dir_frames"}/{name}_dir.png')
    return {'mode': 'grid', 'cw': cw, 'ch': ch, 'frames': {d: len(fs) for d, fs in frames_by_dir.items()},
            'sizes': {d: [f.size for f in fs[:3]] for d, fs in frames_by_dir.items()}}

# exact grid geometry (verified via component detection + grid overlays)
GRIDS = {
    # rows in sheet order; values are (y0, h) measured from character-mask probes
    'cody': ('images/sprite_opt2_programmer.png', [241, 425, 598], 74,
             {'down': (104, 145), 'up': (265, 145), 'right': (432, 145), 'left': (594, 145)}),
    'aria': ('images/sprite_opt3_designer.png', [80, 161, 241], 45,
             {'down': (116, 104), 'up': (220, 99), 'left': (329, 92), 'right': (429, 93)}),
    'pixel': ('images/sprite_opt4_artist.png', [313, 558, 798], 106,
              {'down': (56, 162), 'left': (232, 163), 'right': (413, 161), 'up': (588, 167)}),
    'jax': ('images/sprite_opt5_qa_auditor.png', [267, 569, 881], 95,
            {'down': (65, 175), 'up': (241, 164), 'right': (418, 175), 'left': (596, 166)}),
}

if __name__ == '__main__':
    outdir = '/home/user/dir_frames'
    os.makedirs(outdir, exist_ok=True)
    meta = {}
    # zillion via exact cells
    try:
        src, boxes = SPECS['zillion_cells']
        info = process_cells('zillion', src, boxes, outdir)
        meta['zillion'] = info
        print(f"[OK] zillion(exact): cell {info['cw']}x{info['ch']} frames={info['frames']}")
    except Exception as e:
        print(f"[FAIL] zillion(exact): {e}")
    for name, (src, cols_x, w, rows_y, h) in GRIDS.items():
        try:
            info = process_grid(name, src, cols_x, rows_y, w, h, ncols=3, outdir=outdir)
            meta[name] = info
            print(f"[OK] {name}(grid): cell {info['cw']}x{info['ch']} frames={info['frames']}")
        except Exception as e:
            print(f"[FAIL] {name}(grid): {e}")
    json.dump(meta, open(f'{outdir}/meta.json', 'w'), indent=1, ensure_ascii=False)
