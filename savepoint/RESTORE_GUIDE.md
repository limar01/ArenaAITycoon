# 📦 ZILLION SAVE POINT — RESTORE GUIDE (v1.0 — 2026-08-25)
> **Para sa susunod na account/session ni Boss.** Kapag na-attach ang `MEMORY_CORE.md` at sinabi ni Boss na "Zillion" / "restore" / "save point", sundan ang protocol na ito — awtomatiko itong ibabalik ang lahat ng important files.

---

## 🎯 ANG PROTOCOL (para sa bagong Zillion instance)

### STEP 0 — Confirmation
- Basahin ang `MEMORY_CORE.md` (attached ni Boss). Hanapin ang section **"SAVE POINT & NEW-ACCOUNT BOOT PROTOCOL"**.
- Kung may kasamang `memory_core.json` — gamitin din.
- I-verify ang credentials (SID + KEY) nasa section 6 o sa ibaba.

### STEP 1 — Rebuild ang BRIDGE (mula lang sa memory file, ~4KB)
```bash
pip install paho-mqtt --quiet
mkdir -p bridge
```
- Isulat ang `bridge/mqagent.py` gamit ang embedded source code sa ibaba (nasa MEMORY_CORE.md).
- Isulat ang `bridge/__init__.py` (empty).
- Isulat ang `mq.sh` (nasa embedded section).

### STEP 2 — Test ang koneksyon sa phone ni Boss
```bash
bash mq.sh ping
# Expected: "Worker online! Output: PONG"
```
- Kung OFFLINE: sabihan si Boss na i-restart ang worker:
  ```bash
  python ~/arenabridge/worker.py
  ```
  (o i-check kung bukas pa ang Termux at naka-run ang `python ~/arenabridge/worker.py`)

### STEP 3 — Hilingin sa phone ang FULL SAVEPOINT (mabilis na route)
I-utos sa phone (via `mq.sh send` / python):
```bash
cd ~/projects/hermes_game_studio
tar czf ~/savepoint_full.tgz savepoint/ tools/ qa/ docs/ memory/ 2>/dev/null
# upload sa tmpfiles:
curl -s -F "file=@/data/data/com.termux/files/home/savepoint_full.tgz;filename=sp.tgz;type=application/gzip" \
  -A "Mozilla/5.0" --max-time 300 https://tmpfiles.org/api/v1/upload > ~/up_sp.log 2>&1
cat ~/up_sp.log   # kunin ang URL, tapos hanapin ang /dl/ link
```
Tapos i-download ito sa BAGONG workspace at i-extract:
```bash
curl -sL -o sp.tgz --max-time 300 "<DL_LINK>"
tar xzf sp.tgz
```
- ✅ I-verify sa `sha256sum` (ang expected hash nasa phone side / memory core).

### STEP 4 — Laman ng savepoint (lahat ito ibabalik sa bagong workspace)
| Folder/File | Laman |
|---|---|
| `MEMORY_CORE.md`, `memory_core.json` | Buong utak ng proyekto (bersyon ng savepoint) |
| `bridge/` + `mq.sh` | Remote control (MQTT) sa phone ni Boss |
| `tools/` | deploy_fs_patch.py, deploy_fs_patch2.py, deploy_scale_fix.py, patch_gate7.py, side_map_fix.py, patch_gate9.py, patch_gate10.py, deploy_minimal_remote.py |
| `qa/` | qa_visual.js, qa_g10.js, shots, E_collision_report.json, QA_TEST_SUITE.json |
| `docs/` | Lahat ng GDD, pitch, audits, memory core copies |
| `memory/` | (kung may laman) |

### STEP 5 — I-sync ang master game (kung kailangan)
- Live game: `~/projects/hermes_game_studio/builds/arena_ai_simulator/index.html` (kumpleto, 11.7MB — nasa phone, di kasama sa savepoint bundle para maliit).
- Kung kailangan ng kopya sa bagong workspace: hilingin sa phone na i-upload ito via tmpfiles (gzip) — paraan na ginamit natin.

---

## 🔑 CREDENTIALS (oops — nasa MEMORY_CORE.md section 6)
```
SID : 53cf4a5803c91726b892e5d0785085c6
KEY : [REDACTED-see-~/arenabridge/arenabridge.key]
BROKER: broker.emqx.io  (port 1883)
TOPIC: arenabridge/{SID}/cmd, arenabridge/{SID}/res, arenabridge/{SID}/pres
VMIRror: ~/arenabridge/workspace_mirror  (SYNC_ROOT — doon nakalapag ang put_file)
```

## ⚠️ MGA ARAL (huwag ulitin!)
1. **LAGING i-QA sa browser (headless puppeteer rig) bago i-deploy** — may QA kit ang savepoint (`qa/qa_visual.js`, `qa/qa_g10.js`).
2. **put_file lands sa `workspace_mirror/`** → i-`mv` papuntang `projects/hermes_game_studio/`.
3. **tmpfiles**: huwag i-upload ang `.html` diretso (blocked "Invalid file type") — i-gzip muna o `.bin`.
4. Ang `data:image/png;base64,` prefix sa EVERY embedded asset — kung makalimutan, hindi maglo-load (root cause ng "walang side view").
5. `~` sa remote `sh` commands — gamitin ang `os.path.expanduser` sa python, o buong path `/data/data/com.termux/...`.

---
*Gawa ni Zillion + Chronos. Save point #001. Phone ang master storage; ang bagong workspace = restored copy.*
