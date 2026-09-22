---
name: game-programming
description: "Cody: smallest-safe-change implementation on the single-file canvas engine."
version: 1.0.0
platforms: [linux]
metadata: {hermes: {tags: [code, html5, canvas]}}
related_skills: [git-safe-workflow]
---
# Game Programming
Inspect -> smallest safe change -> test -> report FILES_CHANGED + KNOWN_RISKS.
Never hand-edit builds/**/index.html; use build scripts + sha-verified deploy pattern (tools/patch_gate*.py lineage).
Reuse global: software-development/*, python-project-qa for rig code.
