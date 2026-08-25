#!/usr/bin/env python3
"""GATE 13 — PWA INSTALLABLE APP patch for ARENA AI TYCOON
Zillion (lead) + Cody — prepared during worker downtime, deployed 2026-08-25

2 surgical replacements on builds/arena_ai_simulator/index.html:
  R1: <head> -> inject manifest link + theme-color + apple-touch-icon
  R2: inject SW registration before the title-screen dialogue IIFE comment

Files deployed alongside (via tmpfiles bundle): manifest.json, sw.js,
icon-192.png, icon-512.png (server.py already serves static files).
"""
import sys, shutil, hashlib

PATH = sys.argv[1] if len(sys.argv) > 1 else "index.html"

R1_ANCHOR = "<head>"
R1_NEW = """<head>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#0f0f1a">
<link rel="apple-touch-icon" href="icon-192.png">"""

R2_ANCHOR = "// Hide dialogue box while title screen is up (show only inside game)"
R2_NEW = """// ===== GATE 13: PWA — service worker registration =====
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    navigator.serviceWorker.register('sw.js').catch(function (e) { console.log('SW reg failed:', e); });
  });
}

// Hide dialogue box while title screen is up (show only inside game)"""


def main():
    html = open(PATH, encoding="utf-8").read()
    orig_len = len(html)

    if "GATE 13: PWA" in html:
        print("ALREADY PATCHED — abort (idempotent guard)")
        return 1

    for name, anchor in [("R1", R1_ANCHOR), ("R2", R2_ANCHOR)]:
        n = html.count(anchor)
        if n != 1:
            print(f"ANCHOR {name} count={n} (expected 1) — ABORT, file untouched")
            return 1

    shutil.copyfile(PATH, PATH + ".bak_pre_g13")

    html = html.replace(R1_ANCHOR, R1_NEW, 1)
    html = html.replace(R2_ANCHOR, R2_NEW, 1)

    open(PATH, "w", encoding="utf-8").write(html)

    new_len = len(html)
    print(f"PATCHED OK: {orig_len:,} -> {new_len:,} chars (+{new_len - orig_len:,})")
    print("checks: PWA block x" + str(html.count("GATE 13: PWA"))
          + " manifest-link x" + str(html.count('rel="manifest"'))
          + " sw-reg x" + str(html.count("serviceWorker.register"))
          + " theme-color x" + str(html.count('name="theme-color"')))
    print("sha256:", hashlib.sha256(open(PATH, 'rb').read()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
