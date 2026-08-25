// qa_visual.js - Automated visual QA rig for Arena AI Tycoon (Gate 9 build)
// Runs the real game in headless Chromium, drives the 10 agents, captures screenshots.
const puppeteer = require('puppeteer');
const fs = require('fs');

const GAME = '/home/user/_g9/gate9_fixed.html';
const OUT = '/home/user/_g9/qa/shots';
fs.mkdirSync(OUT, { recursive: true });

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--hide-scrollbars']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 620, deviceScaleFactor: 1 });
  await page.goto('file://' + GAME, { waitUntil: 'load', timeout: 60000 });

  // wait for all sprites to decode
  await page.waitForFunction(() => {
    if (typeof dirSprites === 'undefined') return false;
    const d = dirSprites || {};
    const keys = Object.keys(d);
    return keys.length >= 10 && keys.every(k => d[k] && d[k].complete && d[k].naturalWidth > 0);
  }, { timeout: 30000 });
  await sleep(800);

  // enter game, wide view
  await page.evaluate(() => {
    if (typeof startPlay === 'function') startPlay();
    zoomScale = 1.0; camX = 800; camY = 450;
    const zd = document.getElementById('zoom-disp'); if (zd) zd.innerText = '1.0x';
  });
  await sleep(600);

  const shot = (n) => page.screenshot({ path: `${OUT}/${n}.png` });

  // helper: reset all agents, assign scenario positions + target
  async function scenario(jobs, waitMs, name) {
    await page.evaluate((jobs) => {
      for (let i = 0; i < agents.length; i++) {
        const a = agents[i];
        a.waitTimer = 0; a.path = null; a.isMoving = false;
      }
      for (const j of jobs) {
        const a = agents[j.idx];
        a.x = j.x; a.y = j.y; a.wp = j.wp; a.targetWp = j.target;
      }
    }, jobs);
    await sleep(waitMs);
    await shot(name);
  }

  // A) WALK LEFT — 4 agents moving left across central plaza / corridor
  await scenario([
    { idx: 0, x: 950, y: 600, wp: 'central_plaza', target: 'west_corridor_bot' },
    { idx: 1, x: 850, y: 600, wp: 'central_plaza', target: 'west_corridor_bot' },
    { idx: 2, x: 780, y: 600, wp: 'central_plaza', target: 'west_corridor_bot' },
    { idx: 3, x: 700, y: 600, wp: 'central_plaza', target: 'west_corridor_bot' },
    { idx: 4, x: 620, y: 600, wp: 'central_plaza', target: 'west_corridor_bot' }
  ], 1400, 'A_walk_left');

  // B) WALK RIGHT — moving right along bottom corridor
  await scenario([
    { idx: 0, x: 400, y: 600, wp: 'west_corridor_bot', target: 'war_room_gate' },
    { idx: 1, x: 450, y: 600, wp: 'west_corridor_bot', target: 'war_room_gate' },
    { idx: 2, x: 500, y: 600, wp: 'west_corridor_bot', target: 'war_room_gate' },
    { idx: 3, x: 560, y: 600, wp: 'west_corridor_bot', target: 'war_room_gate' }
  ], 1400, 'B_walk_right');

  // C) WALK UP — from plaza to server room area (north)
  await scenario([
    { idx: 0, x: 680, y: 560, wp: 'central_plaza', target: 'dev_core_north' },
    { idx: 1, x: 680, y: 460, wp: 'central_plaza', target: 'dev_core_north' },
    { idx: 2, x: 880, y: 560, wp: 'war_room_gate', target: 'dev_core_north_2' }
  ], 1400, 'C_walk_up');

  // D) WALK DOWN — from north to plaza
  await scenario([
    { idx: 0, x: 680, y: 260, wp: 'dev_core_north', target: 'central_plaza' },
    { idx: 1, x: 880, y: 260, wp: 'dev_core_north_2', target: 'war_room_gate' }
  ], 1400, 'D_walk_down');

  // E) COLLISION TEST — agent inside Coding Pods must route around walls to Pantry
  await page.evaluate(() => {
    for (let i = 0; i < agents.length; i++) { agents[i].waitTimer = 0; agents[i].path = null; }
    const a = agents[7]; // Jax
    a.x = 600; a.y = 500; a.wp = 'central_cross_1'; a.targetWp = 'pantry_east_gate';
    // also one from server room to gym (crossing whole map)
    const b = agents[6]; // Vortex
    b.x = 290; b.y = 200; b.wp = 'server_room'; b.targetWp = 'gym_gate';
  });
  // sample positions for 7s — flag any agent inside a wall cell
  const violations = [];
  for (let t = 0; t < 35; t++) {
    const bad = await page.evaluate(() => {
      const out = [];
      for (const a of agents) {
        const c = Math.floor(a.x / GRID_CW), r = Math.floor(a.y / GRID_CH);
        if (r >= 0 && r < GRID_ROWS && c >= 0 && c < GRID_COLS && WALL_GRID[r][c] === '#') {
          out.push({ id: a.id, x: Math.round(a.x), y: Math.round(a.y) });
        }
      }
      return out;
    });
    if (bad.length) violations.push({ t, bad });
    await sleep(200);
  }
  fs.writeFileSync(`${OUT}/E_collision_report.json`, JSON.stringify({ violations }, null, 1));
  await shot('E_collision_7s');

  // F) GROUP SHOT — 10 agents at different facings mid-walk
  await page.evaluate(() => {
    for (let i = 0; i < agents.length; i++) { agents[i].waitTimer = 0; agents[i].path = null; }
    const set = [
      [0, 700, 300, 'dev_core_north', 'dev_core_north_2'],   // facing right
      [1, 760, 300, 'dev_core_north', 'central_cross_1'],    // facing down
      [2, 820, 300, 'central_cross_1', 'dev_core_north_2'],  // facing up? (moving up)
      [3, 880, 300, 'dev_core_north_2', 'central_cross_2'],  // down
      [4, 940, 300, 'central_cross_2', 'pantry_east_gate'],  // right
      [5, 1000, 300, 'central_cross_2', 'dev_core_north_3'], // up
      [6, 700, 500, 'central_plaza', 'west_corridor_bot'],   // left
      [7, 760, 500, 'central_plaza', 'war_room_gate'],       // right
      [8, 820, 500, 'war_room_gate', 'central_plaza'],       // left
      [9, 880, 500, 'war_room_gate', 'pantry_east_gate']     // right
    ];
    for (const [idx, x, y, wp, target] of set) {
      const a = agents[idx];
      a.x = x; a.y = y; a.wp = wp; a.targetWp = target;
    }
    camX = 800; camY = 450; zoomScale = 1.0;
  });
  await sleep(1200);
  await shot('F_group_walk');

  await browser.close();
  console.log('QA SHOTS DONE');
})().catch(e => { console.error('QA FAIL:', e.message); process.exit(1); });
