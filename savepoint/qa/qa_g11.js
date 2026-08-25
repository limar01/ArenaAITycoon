const puppeteer = require('puppeteer');
const fs = require('fs');

const URL = 'http://127.0.0.1:8899/game.html';
const OUT = '/home/user/game_work/shots11';
fs.mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--autoplay-policy=no-user-gesture-required', '--mute-audio']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 900, deviceScaleFactor: 1 });

  const consoleErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', e => consoleErrors.push('PAGEERROR: ' + e.message));

  await page.goto(URL, { waitUntil: 'load', timeout: 60000 });
  await new Promise(r => setTimeout(r, 2500)); // let images decode

  // ---- 1. LOAD STATUS of dir sheets + sprites ----
  const loadStatus = await page.evaluate(() => {
    const keys = ['zillion','marcus','aria','cody','pixel','echo','vortex','jax','vanguard','chronos'];
    const out = {};
    for (const k of keys) {
      const d = dirSprites[k];
      const s = sprites[k];
      out[k] = {
        dirType: d ? (d.constructor && d.constructor.name) : 'null',
        dirW: d ? (d.naturalWidth || d.width || 0) : 0,
        dirH: d ? (d.naturalHeight || d.height || 0) : 0,
        dirComplete: d ? !!d.complete : false,
        frontW: s ? (s.naturalWidth || s.width || 0) : 0,
        frontComplete: s ? !!s.complete : false
      };
    }
    return out;
  });

  // ---- 2. START GAME ----
  await page.evaluate(() => { try { startPlay(); } catch(e) { return 'startPlay err: '+e.message; } return 'ok'; });

  // ---- 3. PASSIVE RUN: capture motion over time (what Boss sees) ----
  const passive = await page.evaluate(async () => {
    const snap = () => {
      const c = canvas;
      const w = c.width, h = c.height;
      const cx = c.getContext('2d');
      const d = cx.getImageData(0, 0, w, h).data;
      // downsample to 40x22 luminance grid for cheap diff
      const gw = 40, gh = 22;
      const grid = new Uint8Array(gw * gh);
      for (let gy = 0; gy < gh; gy++) for (let gx = 0; gx < gw; gx++) {
        const px = Math.floor(gx * w / gw), py = Math.floor(gy * h / gh);
        const i = (py * w + px) * 4;
        grid[gy * gw + gx] = (d[i] + d[i+1] + d[i+2]) / 3;
      }
      return { grid, agents: agents.map(a => ({ id: a.id, x: Math.round(a.x), y: Math.round(a.y), f: a.facing, mv: a.isMoving, wf: a.walkFrame })) };
    };
    const s0 = snap();
    await new Promise(r => setTimeout(r, 2000));
    const s1 = snap();
    await new Promise(r => setTimeout(r, 2000));
    const s2 = snap();
    const diff = (a, b) => { let d = 0; for (let i = 0; i < a.grid.length; i++) d += Math.abs(a.grid[i] - b.grid[i]); return d; };
    return { diff01: diff(s0, s1), diff12: diff(s1, s2), t0: s0.agents, t1: s1.agents, t2: s2.agents };
  });

  // ---- 4. ACTIVE: forced 4-direction render crop analysis per character ----
  const cropMetrics = await page.evaluate(async () => {
    const keys = ['zillion','marcus','aria','cody','pixel','echo','vortex','jax','vanguard','chronos'];
    const results = {};
    // freeze simulation so agents don't drift while we sample
    gameState = 0;
    zoomScale = 1.0;
    if (window.__fitScale !== undefined) window.__fitScale = 1.0;
    const facings = ['down','up','left','right'];
    for (const k of keys) {
      const a = agents.find(x => x.id === k);
      if (!a) { results[k] = 'missing'; continue; }
      // park agent at fixed spot, camera centered
      const px = 800, py = 450;
      a.x = px; a.y = py; a.isMoving = true;
      camX = px; camY = py;
      results[k] = {};
      for (const f of facings) {
        a.facing = f; a.walkFrame = 1;
        render();
        const w = canvas.width, h = canvas.height;
        const ctx = canvas.getContext('2d');
        // agent center = canvas center (800,450). crop 60x70 region.
        const c = ctx.getImageData(800 - 30, 450 - 46, 60, 70);
        // metrics
        let alphaCount = 0, alphaSum = 0;
        const rgb = new Array(c.width * c.height);
        for (let i = 0, p = 0; i < c.width * c.height; i++, p += 4) {
          alphaSum += c.data[p + 3];
          if (c.data[p + 3] > 40) alphaCount++;
          rgb[i] = (c.data[p] + c.data[p+1] + c.data[p+2]) / 3;
        }
        // symmetry: compare left half vs mirrored right half
        let symAcc = 0, symN = 0;
        for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width / 2; x++) {
          const i = (y * c.width + x) * 4, j = (y * c.width + (c.width - 1 - x)) * 4;
          if (c.data[i+3] > 40 && c.data[j+3] > 40) { symAcc += Math.abs(rgb[y * c.width + x] - rgb[y * c.width + (c.width - 1 - x)]); symN++; }
        }
        // face offset: skin-ish pixels in upper-middle region
        let fx = 0, fn = 0;
        for (let y = 0; y < Math.floor(c.height * 0.4); y++) for (let x = 0; x < c.width; x++) {
          const p = (y * c.width + x) * 4;
          const R = c.data[p], G = c.data[p+1], B = c.data[p+2], A = c.data[p+3];
          if (A > 40 && R > G && G > B && R > 120 && G > 60) { fx += x; fn++; }
        }
        results[k][f] = {
          alpha: alphaCount,
          sym: symN ? Math.round(symAcc / symN) : -1,
          face: fn > 4 ? Math.round((fx / fn) - c.width / 2) : null
        };
      }
      // walk cycle: down row, walkFrame 1 vs 2 vs 0
      a.facing = 'down';
      const grab = (wf) => { a.walkFrame = wf; render(); return canvas.getContext('2d').getImageData(800 - 30, 450 - 46, 60, 70).data; };
      const d0 = grab(0), d1 = grab(1), d2 = grab(2);
      const pdiff = (A, B) => { let acc = 0, n = 0; for (let i = 0; i < A.length; i += 4) { if (A[i+3] > 40 || B[i+3] > 40) { acc += Math.abs(A[i] - B[i]) + Math.abs(A[i+1] - B[i+1]) + Math.abs(A[i+2] - B[i+2]); n++; } } return n ? Math.round(acc / (n * 3)) : -1; };
      results[k].walk = { d01: pdiff(d0, d1), d12: pdiff(d1, d2), d02: pdiff(d0, d2) };
      // restore
      a.isMoving = false; a.walkFrame = 0;
    }
    gameState = 1;
    return results;
  });

  // ---- 5. NPC presence + motion over time ----
  const npcInfo = await page.evaluate(async () => {
    const info = staticNPCs.map(n => ({ id: n.id, name: n.name, spr: n.spr, x: Math.round(n.x), y: Math.round(n.y), facing: n.facing, moving: n.isMoving }));
    const x0 = staticNPCs.map(n => n.x);
    await new Promise(r => setTimeout(r, 4000));
    const moved = staticNPCs.map((n, i) => Math.abs(n.x - x0[i]) > 2 ? n.name : null).filter(Boolean);
    return { info, movedIn4s: moved };
  });

  // ---- 6. screenshots for evidence ----
  await page.evaluate(() => {
    gameState = 0; zoomScale = 1.0; window.__fitScale = 1.0;
    const a = agents.find(x => x.id === 'zillion');
    a.x = 800; a.y = 450; a.isMoving = true; camX = 800; camY = 450;
  });
  for (const f of ['down','up','left','right']) {
    await page.evaluate((facing) => {
      const a = agents.find(x => x.id === 'zillion');
      a.facing = facing; a.walkFrame = 2; render();
    }, f);
    await page.screenshot({ path: `${OUT}/zillion_${f}.png` });
  }
  // full office screenshot (game running)
  await page.evaluate(() => { gameState = 1; camX = 800; camY = 450; zoomScale = 1.0; });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: `${OUT}/office_full.png` });
  // NPC area zoom (bottom row of NPCs around y 782)
  await page.evaluate(() => { camX = 750; camY = 700; zoomScale = 2.0; });
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: `${OUT}/npc_zone.png` });

  fs.writeFileSync(`${OUT}/report.json`, JSON.stringify({
    consoleErrors,
    loadStatus,
    passive,
    cropMetrics,
    npcInfo
  }, null, 2));

  console.log('=== CONSOLE ERRORS ===');
  console.log(JSON.stringify(consoleErrors, null, 2));
  console.log('=== LOAD STATUS ===');
  console.log(JSON.stringify(loadStatus, null, 2));
  console.log('=== PASSIVE MOTION ===');
  console.log(JSON.stringify(passive, null, 2));
  console.log('=== CROP METRICS ===');
  console.log(JSON.stringify(cropMetrics, null, 2));
  console.log('=== NPC INFO ===');
  console.log(JSON.stringify(npcInfo, null, 2));

  await browser.close();
})();
