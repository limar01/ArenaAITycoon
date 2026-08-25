// qa_g10.js - QA rig for Gate 10: glitch/Jax opacity, walk feet, NPC life, collision
const puppeteer = require('puppeteer');
const fs = require('fs');
const GAME = '/home/user/_g10/gate10.html';
const OUT = '/home/user/_g10/qa/shots10';
fs.mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox', '--disable-gpu', '--hide-scrollbars'] });
  const page = await browser.newPage();
  page.on('pageerror', e => console.log('[PAGEERROR]', e.message.slice(0, 250)));
  await page.setViewport({ width: 1200, height: 620 });
  await page.goto('file://' + GAME, { waitUntil: 'load', timeout: 60000 });
  await page.waitForFunction(() => {
    if (typeof dirSprites === 'undefined') return false;
    const d = dirSprites || {};
    const keys = Object.keys(d);
    return keys.length >= 10 && keys.every(k => d[k] && ((d[k].complete && d[k].naturalWidth > 0) || d[k].width > 0));
  }, { timeout: 30000 });
  await sleep(800);

  await page.evaluate(() => {
    if (typeof startPlay === 'function') startPlay();
    zoomScale = 2.0; camX = 620; camY = 600;
    for (let i = 0; i < agents.length; i++) { agents[i].waitTimer = 0; agents[i].path = null; }
  });
  await sleep(400);
  const shot = (n) => page.screenshot({ path: `${OUT}/${n}.png` });

  // ---- 1) JAX opacity check (Jax at center, zoom in) ----
  await page.evaluate(() => {
    const a = agents.find(x => x.id === 'jax');
    a.x = 620; a.y = 600; a.wp = 'central_plaza'; a.targetWp = 'central_plaza';
    a.waitTimer = 9999; a.isMoving = false; a.facing = 'down';
    camX = 620; camY = 600; zoomScale = 2.5;
  });
  await sleep(500);
  await shot('1_jax_idle_zoom');

  // ---- 2) WALK FEET: two frames 600ms apart while walking ----
  await page.evaluate(() => {
    zoomScale = 1.6; camX = 800; camY = 450;
    for (let i = 0; i < agents.length; i++) {
      const a = agents[i];
      a.waitTimer = 0; a.x = 980 + i * 24; a.y = 600; a.wp = 'war_room_gate';
      a.targetWp = 'central_plaza'; // walking left
    }
  });
  await sleep(900); await shot('2a_walk_frame1');
  await sleep(600); await shot('2b_walk_frame2');

  // ---- 3) NPC LIFE: wait for bubbles/shuffles, screen near several NPCs ----
  await page.evaluate(() => {
    zoomScale = 1.3; camX = 780; camY = 700;
    for (const n of staticNPCs) { n.timer = 1; } // trigger soon
  });
  await sleep(2500); await shot('3a_npc_bubbles');
  await sleep(3500); await shot('3b_npc_bubbles2');

  // ---- 4) COLLISION VIOLATIONS over 6s (jax + vortex cross-map) ----
  await page.evaluate(() => {
    for (let i = 0; i < agents.length; i++) { agents[i].waitTimer = 0; agents[i].path = null; }
    const b = agents[7]; b.x = 600; b.y = 500; b.wp = 'central_cross_1'; b.targetWp = 'pantry_east_gate';
    const c = agents[6]; c.x = 290; c.y = 200; c.wp = 'server_room'; c.targetWp = 'gym_gate';
  });
  const violations = [];
  for (let t = 0; t < 30; t++) {
    const bad = await page.evaluate(() => {
      const out = [];
      for (const a of agents) {
        const c = Math.floor(a.x / GRID_CW), r = Math.floor(a.y / GRID_CH);
        if (r >= 0 && r < GRID_ROWS && c >= 0 && c < GRID_COLS && WALL_GRID[r][c] === '#') out.push(a.id);
      }
      for (const n of staticNPCs) {
        const c = Math.floor(n.x / GRID_CW), r = Math.floor(n.y / GRID_CH);
        if (r >= 0 && r < GRID_ROWS && c >= 0 && c < GRID_COLS && WALL_GRID[r][c] === '#') out.push('npc:' + n.id);
      }
      return out;
    });
    if (bad.length) violations.push({ t, bad });
    await sleep(200);
  }
  fs.writeFileSync(`${OUT}/4_collision_report.json`, JSON.stringify({ violations }, null, 1));
  await shot('4_collision_6s');

  // ---- 5) NPC opacity sample: check no ghost ----
  const jaxAlpha = await page.evaluate(() => {
    // sample dirSprites jax canvas: fraction of semi-transparent pixels
    const c = dirSprites['jax'];
    if (c && c.getContext) {
      const cx = c.getContext('2d');
      const id = cx.getImageData(0, 0, c.width, c.height);
      let semi = 0, solid = 0;
      for (let i = 3; i < id.data.length; i += 4) {
        if (id.data[i] > 0 && id.data[i] < 255) semi++;
        else if (id.data[i] === 255) solid++;
      }
      return { semi, solid, pct: (100 * semi / Math.max(1, semi + solid)).toFixed(2) };
    }
    return null;
  });
  fs.writeFileSync(`${OUT}/5_jax_alpha.json`, JSON.stringify(jaxAlpha));

  await browser.close();
  console.log('G10 QA DONE: violations=', violations.length, 'jaxAlpha=', JSON.stringify(jaxAlpha));
})().catch(e => { console.error('QA FAIL:', e.message); process.exit(1); });
