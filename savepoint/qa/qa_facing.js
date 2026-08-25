const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox','--disable-setuid-sandbox','--mute-audio'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 900 });
  await page.goto('http://127.0.0.1:8899/game.html', { waitUntil: 'load', timeout: 60000 });
  await new Promise(r => setTimeout(r, 2500));
  const res = await page.evaluate(() => {
    startPlay(); gameState = 0; zoomScale = 1.0; window.__fitScale = 1.0;
    const keys = ['zillion','marcus','aria','cody','pixel','echo','vortex','jax','vanguard','chronos'];
    const W=40, H=48;
    const grab = () => canvas.getContext('2d').getImageData(780, 410, W, H).data;
    // background frame (all chars away)
    for (const o of agents) { o.x=-99999; o.y=-99999; }
    for (const n of staticNPCs) { n.x=-99999; n.y=-99999; }
    render(); const BG = grab();

    const skinCent = (F) => {
      let sx=0, n=0;
      for (let y=0;y<H;y++) for (let x=0;x<W;x++) {
        const i=(y*W+x)*4;
        const dr=Math.abs(F[i]-BG[i]), dg=Math.abs(F[i+1]-BG[i+1]), db=Math.abs(F[i+2]-BG[i+2]);
        if (dr+dg+db > 40 && F[i]>F[i+1] && F[i+1]>F[i+2] && F[i]>120 && F[i+1]>55) { sx+=x; n++; }
      }
      return n>=4 ? (sx/n).toFixed(1) : 'none';
    };
    const out = {};
    for (const k of keys) {
      const a = agents.find(x=>x.id===k);
      a.x=800; a.y=450; a.isMoving=true; a.walkFrame=1; camX=800; camY=450;
      a.facing='left'; render(); const L = grab();
      a.facing='right'; render(); const R = grab();
      out[k] = { left: skinCent(L), right: skinCent(R) };
      a.x=-99999;
    }
    return out;
  });
  console.log('char       | skinX(left) | skinX(right) | verdict (left<20<right = correct)');
  let bad = 0;
  for (const k of Object.keys(res)) {
    const l = parseFloat(res[k].left), r = parseFloat(res[k].right);
    const ok = !isNaN(l) && !isNaN(r) && l < 20 && r > 20;
    if (!ok) bad++;
    console.log(`${k.padEnd(10)} | ${res[k].left.padStart(10)} | ${res[k].right.padStart(11)} | ${ok?'OK':'CHECK'}`);
  }
  console.log('chars needing attention:', bad);
  await browser.close();
})();
