
import os, sys
PATH = os.path.expanduser('~/projects/hermes_game_studio/builds/arena_ai_simulator/index.html')
html = open(PATH, encoding='utf-8').read()
OLD = "        const ROW = { down: 0, up: 1, left: 2, right: 3 };\n        // characters with a genuine RIGHT row (verified via orientation analysis);\n        // everyone else: RIGHT = LEFT row horizontally flipped (always correct direction)\n        const NATIVE_RIGHT = { cody: 1, vortex: 1, vanguard: 1 };"
NEW = "        const ROW = { down: 0, up: 1, left: 2, right: 3 };\n        const SIDE = { zillion: { left: 2, right: '2f' }, marcus: { left: '2f', right: 2 }, aria: { left: 2, right: '2f' }, cody: { left: 2, right: 3 }, pixel: { left: '2f', right: 2 }, echo: { left: '2f', right: 2 }, vortex: { left: 3, right: 2 }, jax: { left: 2, right: '2f' }, vanguard: { left: 3, right: 2 }, chronos: { left: '2f', right: 2 } };"
if OLD in html:
    html = html.replace(OLD, NEW, 1)
    html = html.replace("        let row = (ROW[a.facing] !== undefined) ? ROW[a.facing] : 0;\n        let flip = false;\n        if (a.facing === 'right') {\n          if (NATIVE_RIGHT[a.id]) { row = 3; }\n          else { row = 2; flip = true; }\n        } else if (a.facing === 'left') {\n          row = 2; flip = false;\n        }", "        let row = (ROW[a.facing] !== undefined) ? ROW[a.facing] : 0;\n        let flip = false;\n        if (a.facing === 'left' || a.facing === 'right') {\n          const m = (SIDE[a.id] || { left: 2, right: '2f' })[a.facing];\n          if (m === 2 || m === 3) { row = m; flip = false; }\n          else { row = 2; flip = true; }\n        }", 1)
    open(PATH, 'w', encoding='utf-8').write(html)
    print('SIDE MAP PATCHED OK')
else:
    print('ALREADY PATCHED or pattern missing')
