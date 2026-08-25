#!/usr/bin/env python3
"""
build_minimal_mode.py - Insert MINIMAL MODE toggle layer into index.html.
MINIMAL disables: store (btn+FAB+modal), boss spawn, beer party, zone legend,
vertical switcher, arcade, agent stat bars. Keeps: title screen, office world,
10 agents, clock/day, dialogue, zoom, save/load, BGM.
Persistent via localStorage; tiny corner toggle to switch back to FULL.
"""
import re, os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index_minimal.html')

PATCH = r"""
<!-- ==================== MINIMAL MODE LAYER (Boss toggle) ==================== -->
<style id="minimal-mode-css"></style>
<button id="mode-toggle-btn" title="Toggle MINIMAL / FULL modes">🎯 MODE: MINIMAL</button>
<script>
(function () {
  var isFull = (function () {
    try { return localStorage.getItem('arena_mode') === 'full'; } catch (e) { return false; }
  })();
  var HIDE = [
    '#retro-header .vertical-select',   // vertical switcher
    '#vertical-selector',               // vertical switcher (alt)
    '#floating-store-fab',              // store FAB
    '#control-bar .store-main-btn',     // store button
    '#boss-spawn-toggle',               // boss avatar
    '#party-btn',                       // beer friday
    '#zone-legend',                     // zone nav bar
    '#agent-stat-bars'                  // 3 stat bars
  ];
  function applyMode() {
    var css = document.getElementById('minimal-mode-css');
    if (isFull) { css.textContent = ''; }
    else {
      css.textContent = HIDE.join(',') + '{display:none !important;}';
      // keep game clean & centered: hide store modal & arcade modal entirely
      css.textContent += '#store-modal,#arcade-modal{display:none !important;}';
    }
    var btn = document.getElementById('mode-toggle-btn');
    if (btn) {
      btn.textContent = '🎯 MODE: ' + (isFull ? 'FULL' : 'MINIMAL');
      btn.style.position = 'fixed';
      btn.style.left = '8px';
      btn.style.bottom = '8px';
      btn.style.zIndex = '9999';
      btn.style.fontSize = '11px';
      btn.style.fontWeight = 'bold';
      btn.style.fontFamily = 'monospace';
      btn.style.padding = '6px 10px';
      btn.style.border = '2px solid #ffcc00';
      btn.style.borderRadius = '6px';
      btn.style.background = 'rgba(12,12,24,0.85)';
      btn.style.color = '#ffcc00';
      btn.style.cursor = 'pointer';
      btn.style.opacity = '0.85';
      btn.style.boxShadow = '0 0 10px rgba(255,204,0,0.4)';
    }
  }
  // Neutralize optional feature entry points when in MINIMAL
  function neutralize() {
    if (isFull) return;
    try {
      window.openStore = function () { };
      window.toggleBossAvatar = function () { };
      window.toggleParty = function () { };
      window.openArcade = function () { };
      window.switchVertical = function () { };
      window.focusZone = function () { };
      window.shootArcadeLaser = function () { };
      window.closeArcade = function () { };
      window.closeStore = function () { };
      window.showStore = function () { };
      window.buyStoreItem = function () { };
      // stop automated boss/party triggers if any
      var sc = document.getElementById('store-modal'); if (sc) sc.classList.add('hidden');
      var am = document.getElementById('arcade-modal'); if (am) am.classList.add('hidden');
    } catch (e) { /* silent */ }
  }
  var btn = document.getElementById('mode-toggle-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      try {
        localStorage.setItem('arena_mode', (isFull ? 'minimal' : 'full'));
      } catch (e) { }
      location.reload();
    });
  }
  applyMode();
  neutralize();
  // re-apply when DOM settles (some elements load dynamically)
  document.addEventListener('DOMContentLoaded', function () { applyMode(); neutralize(); });
})();
</script>
</body>"""

html = open(SRC, encoding='utf-8').read()
# strip any previously inserted minimal layer (idempotent)
html = re.sub(r'<!-- =+ MINIMAL MODE LAYER.*?</body>', '</body>', html, flags=re.S)
html = html.replace('</body>', PATCH, 1)
open(OUT, 'w', encoding='utf-8').write(html)
print("WROTE", OUT, len(html), "bytes")
