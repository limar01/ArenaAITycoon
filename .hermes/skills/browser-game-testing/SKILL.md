---
name: browser-game-testing
description: "Headless + on-device testing of the HTML5 game."
version: 1.0.0
platforms: [linux]
metadata: {hermes: {tags: [browser, testing]}}
---
# Browser Game Testing
Targets: phone Chrome via Termux http.server :8888 (primary), PC headless Chromium (dev).
Capture screenshots to qa/shots/; PWA install check; offline SW check; reuse qa/ rig.
Boss's personal Firefox = NEVER for QA (doctrine rule 10).
