# WORKFLOW: GAUNTLET (VANGUARD) LOOP
1. Implementer submits report_template + evidence.
2. Vanguard (independent session/model) reviews spec, diff, tests, runtime evidence, regression risk.
3. PASS → Chronos records acceptance → pipeline continues.
4. FAIL → fix task back to owner with FAIL template (EXPECTED/ACTUAL/EVIDENCE/ROOT CAUSE/REQUIRED FIX/REGRESSION TEST).
5. Cycle counter++ ; if >3 → STOP, escalate Zillion→Boss with full evidence chain.
6. Chronos logs every cycle in QA_STATE.md (append-only).
