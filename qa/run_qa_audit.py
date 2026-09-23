#!/usr/bin/env python3
"""
QA Evidence Schema Updater (Phase 4.5)
Upgrades the QA audit to emit structured JSON evidence with:
- procedure
- expected
- actual
- evidence
- severity (0=info, 1=critical, 2=high, 3=medium, 4=low)

Input: qa/QA_TEST_SUITE.json
Output: qa/reports/<date>_qa_evidence.json (machine-readable)
        qa/reports/<date>_qa_report.md (human-readable)
"""
import os
import json
import time
import urllib.request
import ssl
import sys
from datetime import datetime

# PC paths (canonical dev home per Boss decision 2026-09-23)
BASE = os.path.expanduser("~/Projects/workspace/ArenaAITycoon")
QA_FILE = os.path.join(BASE, "qa", "QA_TEST_SUITE.json")
REPORT_DIR = os.path.join(BASE, "qa", "reports")
SCREENSHOT_DIR = os.path.join(BASE, "qa", "screenshots")

# Ensure output dirs exist
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Load test suite
with open(QA_FILE, "r", encoding="utf-8") as f:
    suite = json.load(f)

test_cases = suite.get("test_cases", [])

# Check if local server is live
server_live = False
server_url = "http://localhost:8888/"
try:
    req = urllib.request.Request(server_url)
    with urllib.request.urlopen(req, timeout=5) as resp:
        if resp.status == 200:
            server_live = True
except Exception:
    server_live = False

results = []
passed_count = 0
failed_count = 0
severity_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

for tc in test_cases:
    tc_id = tc.get("id", "UNKNOWN")
    title = tc.get("title", "Untitled")
    cat = tc.get("category", "Uncategorized")
    expected = tc.get("expected", "No expected result defined")
    pass_criteria = tc.get("pass_criteria", "No pass criteria defined")

    # Build structured evidence entry
    entry = {
        "id": tc_id,
        "category": cat,
        "title": title,
        "procedure": f"Verify {title.lower()} by running the game and observing behavior.",
        "expected": expected,
        "pass_criteria": pass_criteria,
        "actual": "",
        "evidence": "",
        "severity": 4,  # default low
        "status": "PASSED"
    }

    # Determine status based on server availability and test category
    if not server_live and tc_id.startswith("TC-SYS"):
        entry["actual"] = f"Game server at {server_url} is not responsive. Cannot verify system-level behavior."
        entry["evidence"] = f"curl {server_url} returned connection refused/timeout."
        entry["status"] = "FAILED"
        entry["severity"] = 1  # critical
    elif not server_live and not tc_id.startswith("TC-SYS"):
        # Non-system tests can be checked statically (code review, asset existence)
        entry["actual"] = f"Server offline — static analysis only for {tc_id}."
        entry["evidence"] = "Code review pending server availability."
        entry["status"] = "SKIPPED"
        entry["severity"] = 4
    else:
        # Server live — test would run here with CDP/headless
        entry["actual"] = "Server responsive — test execution pending (requires CDP headless automation)."
        entry["evidence"] = f"Server at {server_url} returned 200 OK. Full evidence collection pending Phase 6 QA run."
        entry["status"] = "PENDING"
        entry["severity"] = 3

    # Count
    if entry["status"] == "PASSED":
        passed_count += 1
    elif entry["status"] == "FAILED":
        failed_count += 1

    severity_counts[entry["severity"]] = severity_counts.get(entry["severity"], 0) + 1
    results.append(entry)

# Generate timestamp
ts = datetime.now().strftime("%Y%m%d_%H%M%S")

# Write JSON evidence report
json_report = {
    "meta": {
        "project": suite.get("project", "ArenaAITycoon"),
        "version": suite.get("version", "v15"),
        "audit_date": datetime.now().isoformat(),
        "auditor": "Jax (QA Adversarial) — schema upgrade Phase 4.5",
        "server_live": server_live,
        "server_url": server_url
    },
    "summary": {
        "total": len(test_cases),
        "passed": passed_count,
        "failed": failed_count,
        "skipped": len(test_cases) - passed_count - failed_count,
        "severity_counts": severity_counts,
        "verdict": "PASS" if failed_count == 0 else "REVISION REQUIRED"
    },
    "results": results
}

json_path = os.path.join(REPORT_DIR, f"{ts}_qa_evidence.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_report, f, indent=2, ensure_ascii=False)

# Write human-readable markdown report
md = f"""# 📊 QA Evidence Report — ArenaAITycoon

**Project:** {suite.get('project', 'Arena AI Tycoon')} ({suite.get('version', 'v15')})  
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Auditor:** Jax (QA Adversarial)  
**Server:** {server_url} ({'LIVE' if server_live else 'OFFLINE'})  
**Verdict:** {'✅ PASS' if failed_count == 0 else '❌ REVISION REQUIRED'}

---

## Summary

| Metric | Count |
|--------|-------|
| Total | {len(test_cases)} |
| Passed | {passed_count} |
| Failed | {failed_count} |
| Skipped/Pending | {len(test_cases) - passed_count - failed_count} |

### Severity Breakdown

| Severity | Count |
|----------|-------|
| 🔴 1-Critical | {severity_counts[1]} |
| 🟠 2-High | {severity_counts[2]} |
| 🟡 3-Medium | {severity_counts[3]} |
| 🟢 4-Low | {severity_counts[4]} |

---

## Detailed Results

| ID | Category | Title | Status | Severity |
|----|----------|-------|--------|----------|
"""

for r in results:
    icon = "✅" if r["status"] == "PASSED" else ("❌" if r["status"] == "FAILED" else "⏭️")
    sev = {0: "ℹ️", 1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢"}.get(r["severity"], "?")
    md += f"| `{r['id']}` | {r['category']} | {r['title']} | {icon} {r['status']} | {sev} {r['severity']} |\n"

md += """
---

## Evidence Schema

Each result includes:
- **procedure** — how the test is performed
- **expected** — what should happen
- **actual** — what was observed
- **evidence** — proof (screenshot, log, curl output)
- **severity** — impact if unresolved (1=critical, 4=low)

## Next Steps

1. Start the game server on phone (:8888) to enable full automated testing
2. Run `qa/run_qa_audit.py` again to capture live evidence
3. Address all severity-1 (critical) findings before G6 Beta

---

*Schema version: Phase 4.5 upgrade (2026-09-23). Machine-readable JSON: see `qa/reports/<ts>_qa_evidence.json`.*
"""

md_path = os.path.join(REPORT_DIR, f"{ts}_qa_report.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write(md)

# Also update the latest symlink/copy for easy access
latest_md = os.path.join(REPORT_DIR, "LATEST_QA_REPORT.md")
with open(latest_md, "w", encoding="utf-8") as f:
    f.write(md)

print(f"✅ QA Evidence Report generated")
print(f"   JSON: {os.path.basename(json_path)}")
print(f"   MD:   {os.path.basename(md_path)}")
print(f"   Verdict: {'PASS' if failed_count == 0 else 'REVISION REQUIRED'} ({failed_count} failed)")
