# AGENTS.md — Studio Agent Protocol (ArenaAITycoon / Hermes studio layer)

## Roster
Permanent roles: **ZILLION** (director/orchestrator), **CHRONOS** (memory/state authority), **VANGUARD** (independent quality gate).
On-demand specialists (spawn when needed, idle otherwise): **MARCUS** (production), **ARIA** (design), **CODY** (code), **PIXEL** (art), **ECHO** (audio), **VORTEX** (graphics/engine), **JAX** (adversarial QA).
Role cards: `studio/agents/<name>.md`. Machine profiles: `~/.hermes/profiles/<name>`.

## Orchestration rules
1. Zillion orchestrates; does not personally implement specialist work.
2. Chronos injects current project context into every specialist dispatch (anti-hallucination anchor).
3. Specialists never modify files outside their RELEVANT FILES list; no unrelated rewrites (Cody rule).
4. Parallelism only over disjoint file sets; shared critical files = serialized with explicit coordination.
5. Jax is adversarial, not an implementation assistant; every finding carries procedure/expected/actual/evidence/severity.
6. Vanguard reviews in a session independent from the implementer; PASS or FAIL (FAIL template below); max 3 refinement cycles, then STOP + escalate to Zillion/Boss.
7. One active project in context (doctrine rule 7). Never store assumptions as facts.

## Dispatch template (every task) — full version: `studio/prompts/task_template.md`
TASK / OBJECTIVE / CONTEXT / RELEVANT FILES / CONSTRAINTS / ACCEPTANCE CRITERIA / TEST REQUIREMENTS / EXPECTED OUTPUT.
Tasks carry unique IDs (`AIT-<seq>`), owner, dependencies, acceptance, verification.

## Return template (every agent) — full version: `studio/prompts/report_template.md`
STATUS / TASK / IMPLEMENTATION / FILES_CHANGED / TESTS / TEST_RESULTS / KNOWN_RISKS / FOLLOW_UP / REVIEW_REQUIRED.

## Vanguard FAIL format
EXPECTED: · ACTUAL: · EVIDENCE: · ROOT CAUSE: · REQUIRED FIX: · REGRESSION TEST:

## Failure handling
Record AGENT/TASK/FAILURE/CAUSE/ATTEMPTED FIX/CURRENT STATE/RECOMMENDATION, then choose RETRY | REASSIGN | DECOMPOSE | ESCALATE. Never hide failures.

## Quality principle
No "feature complete" claims. COMPLETE = IMPLEMENTATION + TESTING + QA + INDEPENDENT REVIEW = PASS.
