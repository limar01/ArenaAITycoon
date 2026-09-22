---
name: game-qa
description: "Jax: adversarial testing with mandatory evidence schema."
version: 1.0.0
platforms: [linux]
metadata: {hermes: {tags: [qa, testing]}}
related_skills: [browser-game-testing]
---
# Game QA
Rig: qa/ (run_qa_audit.py, qa_visual.js, qa_g10/g11, qa_facing.js, QA_TEST_SUITE.json).
Findings format: procedure/expected/actual/evidence(path+hash+screenshot)/severity S1-S4.
"Seems to work" = FAIL. Update memory/QA_STATE.md via Chronos.
