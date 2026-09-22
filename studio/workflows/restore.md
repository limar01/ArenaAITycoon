# WORKFLOW: SESSION RESTORE (merged)
Primary: zillion-restore doctrine kit (`zillionCp <PASSPHRASE>` → GATE 0 → LIST D for zillionOM lane).
Project layer: after lane restore, Chronos reads `memory/PROJECT_STATE.md` + `CURRENT_SPRINT.md` + `DECISIONS.md` (never the full legacy core unless needed); private handoff per doctrine rule 20.
Legacy fallback (offline): MEMORY_CORE §0b save-point protocol + `savepoint/` snapshot — FROZEN, use only when git/phone unreachable.
