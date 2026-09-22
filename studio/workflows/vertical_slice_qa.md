# WORKFLOW: VERTICAL SLICE QA (Jax)
Loop under test (ArenaAITycoon): START → ENTER ARENA → GAMEPLAY (walk/A*/collision/zoom) → AI ACTIVITY (LLM tap, fallback phrases) → PLAYER INTERACTION → EVENT (Beer Friday/coffee) → REWARD/PROGRESSION → SAVE → LOAD.
Per node: run headless rig (`qa/run_qa_audit.py`, `qa_visual.js`, `qa_g10/g11`, `qa_facing.js`) on phone Chrome :8888 + PC headless; capture screenshots to `qa/shots/`; emit JSON findings with procedure/expected/actual/evidence/severity.
Severity S1 crash/save-loss · S2 broken loop node · S3 visual/audio defect · S4 polish. G5 exit requires S1=S2=0.
