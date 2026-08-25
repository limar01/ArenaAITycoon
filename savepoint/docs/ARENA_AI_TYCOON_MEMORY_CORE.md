# 🧠 ARENA AI TYCOON — MEMORY CORE v2.0
> **Persistent project brain.** Every session starts here. Last updated: **2026-08-25** (Asia/Manila)
> Owner: **Boss** (final approval authority). Lead: **Zillion**. Team: 10 sub-agents.
> Canonical copies: `~/projects/hermes_game_studio/docs/ARENA_AI_TYCOON_MEMORY_CORE.md` (phone) ↔ `/home/user/MEMORY_CORE.md` (sandbox). Machine snapshot: `memory_core.json`.

---

## 0. ONE-LINE SUMMARY
A cozy **top-down pixel-art studio life sim** ("virtual AI office world") where **10 AI personas work/live in a canvas office**, with upgrades, stats, minigames, save/load, PWA, and **live LLM brains (Ollama on phone)** — branded **ARENA AI TYCOON**. Runs as a single HTML5 canvas game served from **Termux + Python http.server on the phone**, mobile-first.

---

## 1. BOSS GATE WORKFLOW (NON-NEGOTIABLE)
```
Gate N work → QA (Jax) → Auditor (Vanguard) report → PRESENT to Boss →
  1 = APPROVE  → next gate
  2 = ASSIGN BACK → team fixes same gate
  3 = REJECT   → fresh ideas needed (new direction)
```
- Boss is the ONLY approver. Never auto-approve.
- Reports must be **Taglish, direct, "Boss-style"**.
- Every task is **classified and assigned to named sub-agents** (see §2).

---

## 2. TEAM ROSTER + MODEL MATRIX (Ollama on phone, port 11434)
| # | Persona | Role | Render | Ollama model | Game sprite id |
|---|---------|------|--------|--------------|----------------|
| 0 | **Zillion** | Technical Director (LEAD), dark coat, silver/blue glasses | leads | `qwen2.5:1.5b` | `zillion` |
| 1 | **Marcus** | Producer, rolled shirt + vest | | `llama3.2:1b` | `marcus` |
| 2 | **Aria** | Systems/Narrative Designer, purple sweater | | `llama3.2:1b` | `aria` |
| 3 | **Cody** | Lead Programmer, hoodie + backward cap | movement/input/integration | `qwen2.5-coder:1.5b` | `cody` |
| 4 | **Pixel** | Graphic Artist, beret + apron | sprites/title art | `qwen2.5:1.5b` | `pixel` |
| 5 | **Echo** | Audio Director, leather jacket + headphones | | `qwen2.5:1.5b` | `echo` |
| 6 | **Vortex** | Shader Architect, neon cyan hair | | `qwen2.5-coder:1.5b` | `vortex` |
| 7 | **Jax** | QA Bug Hunter, denim jacket + rubber duck | QA/screenshot audit | `deepseek-r1:1.5b` | `jax` |
| 8 | **Vanguard** | Judge (AAA auditor), suit + pocket watch + mustache | gate auditor | `deepseek-r1:1.5b` | `vanguard` |
| 9 | **Chronos** | Memory Anchor/Keeper, blazer + vintage watch + journal | memory core | `qwen2.5:1.5b` | `chronos` |

Installed models (verified via `/api/tags`): `llama3.2:1b`, `deepseek-r1:1.5b`, `qwen2.5-coder:1.5b`, `qwen2.5:1.5b`.

---

## 3. LOCKED DECISIONS (BOSS-VOTED — DO NOT REVERT)
1. **Title/branding:** **ARENA AI TYCOON** (was: Arena AI Simulator: Studio Life → now final).
2. **Office layout:** **1080p Widescreen Campus** (`office_1080p.png`) — layout switcher **DISABLED** (no map variants).
3. **Title screen:** LEAN — one group **background image** of the 10 AI characters with label **"Arena AI Tycoon"**.
4. **No overlays blocking gameplay:** minimap ❌, compiler-pipeline HUD ❌ (removed permanently).
5. **Sprite scale:** natural NPC proportion — `sw = 28`, `sh ≈ 44` (matches background NPCs).
6. **Default camera:** `zoomScale = 1.4`, start `camX = 800, camY = 450`. Canvas **1600×900**.
7. **Directional walking (Boss requirement):**
   - walk **right** → **side/right view**
   - walk **left** → **side/left view**
   - walk **up** → **back view**
   - walk **down** → **front view**
8. **Ignore Arch Linux** for active work. Mobile/Termux only (installer exists, archived, not foregrounded).
9. **Phone path only:** `~/projects/hermes_game_studio/builds/arena_ai_simulator/` — legacy `castlevania_stage1` DELETED from phone (do not resurrect).
10. **Taglish reporting** to Boss always; assign work to sub-agents explicitly.

---

## 4. ASSET INVENTORY & STATUS
### Title / backgrounds `/home/user/images/` (also on phone)
| File | Size | Status |
|------|------|--------|
| `arena_ai_tycoon_title.png` | 1408×768 (2.5 MB) | ✅ **EMBEDDED in `/home/user/index.html`** (sha256 `e2e99c15…` MATCH verified) — title screen bg |
| `office_1080p.png` | 1408×768 | ✅ Voted map — used as in-game `office_bg` |
| `office_2k.png` / `office_800x600.png` | — | archived alternates (unused) |

### Sprite sheets (directional sheets, checkered bg, need slicing/transparency)
| File | Character | Notes |
|------|-----------|-------|
| `sprite_opt1_director.png` 1408×768 | Zillion | SOUTH row (stand/step1/step2) + back views + WEST side views in sheet |
| `sprite_opt2_programmer.png` | Cody | same layout |
| `sprite_opt3_designer.png` | Aria | same layout |
| `sprite_opt4_artist.png` | Pixel | same layout |
| `sprite_opt5_qa_auditor.png` | Jax | same layout |
> ⚠️ Sheets contain **4-direction rows** (SOUTH/NORTH/WEST/etc.) but have **checkerboard backgrounds** and are **NOT yet sliced/transparent**. The "additional 4 images" from the last turn did NOT persist on disk.
> **MISSING sheets (5):** Marcus, Echo, Vortex, Vanguard, Chronos.

### Live transparent sprites `/home/user/assets/` (used by game NOW)
`zillion.png`, `marcus.png`, `aria.png`, `cody.png`, `pixel.png`, `echo.png`, `vortex.png`, `jax.png`, `vanguard.png`, `chronos.png` + `*_head.png` portraits. All **front-view only**.

### Office/preview extras
`assets/office_topdown_preview.png`, `assets/character_sprites_preview.png`, `assets/comic_dialogue_preview.png` (user attachments), `extracted_assets/office_bg.png`, `sprites_extracted/*.png` (10 character crops).

---

## 5. BUILD STATE (VERIFIED 2026-08-25)
**Canonical build:** `/home/user/index.html` (10.2 MB, single-file, base64-embedded)
- ✅ Title text "ARENA AI TYCOON"; title bg = `arena_ai_tycoon_title.png` **embedded + hash-verified**
- ✅ `office_1080p.png` embedded as `ASSETS.office_bg` (sha verified)
- ✅ Sprite natural scale `sw=28 / sh≈44`; canvas 1600×900; zoom 1.4
- ✅ Directional logic present: `a.facing` from movement (`|dx|>|dy|` → right/left else down/up)
- ✅ Render: LEFT = `ctx.scale(-1,1)` flip; UP = `brightness(0.85)` tint only; DOWN/RIGHT = front sprite
- ✅ NO minimap, NO compiler-pipeline HUD (removed)
- ✅ Features in build: 10 agents + zones (exec/dev_desks/war_room/lounge/arcade/gym/pantry), upgrade store (8 items), save/load (localStorage), vertical switcher (🎮/🏗️/✍️), arcade minigame, billiards physics, 24h clock, 3 stat bars (Energy/Focus/Happiness), touch pan/pinch, zone bar, boss avatar
- ⚠️ **KNOWN GAP:** sprites are still **single front images** — TRUE 4-DIRECTION (real back/side frames) NOT yet implemented. Partial simulation only (flip + darken).
- Builder scripts (`build_proportional_directional.py` = current; others = historical; `build_clean_fullscreen_game.py`, `build_master_all_in_one.py`, etc.). `index_modular.html` = modular variant for phone/assets split.

---

## 5b. 🧹 WORKSPACE CLEANUP 2026-08-25 (BOSS ORDER) → REVERTED: RESTORED & ALIGNED
- ❗ **Restored/updated 2026-08-25 (Boss: "update mo muna workspace ko from backup para align ang files ko").**
- Full workspace pulled back from phone (`tmpfiles.org` link, phone→sandbox, NO chunks needed — fast route proven; upload ~30s, download ~5s).
- **SHA-256 verified PERFECT COPY:** `021398a72cf2d20119b068a7c2dcfa2ac6c3680be39decbfdbe1a4b367b98bd4` (88,199,698 bytes).
- **Extracted (excluded newer local files):** MEMORY_CORE.md, memory_core.json, bridge/, mq.sh (kept local NEWER versions); projects/ EXCLUDED (contains legacy castlevania_stage1 — never resurrect).
- **Verified vs phone snapshot:** index.html = 10,216,965 bytes ✅ · 9 images ✅ · 23 assets ✅ · 19 scripts ✅ · ARENA AI TYCOON ×2 ✅ · title bg embedded MATCH True ✅.
- **Current local size: 92MB.** `~` workspace is FULLY ALIGNED with phone snapshot now.
- **Fast-transfer method for future:** phone uploads tar to tmpfiles.org → sandbox downloads + sha verify. (Alternative slow: MQTT put_file chunks 700KB×124.)
- Local scratch `/tmp` cleaned after restore.

### Old cleanup record (history only — no longer applies):
- Local sandbox was CLEANED: 132MB → 654KB (deleted index.html, images/, assets/, projects/, uploads/, scripts, arch stuff; retained only memory+bridge). All safe on phone (sha `021398a7…`, HTTP 200). → **Reversed today by full restore.**

## 6. PHONE / TERMUX DEPLOYMENT
### 🗃️ WORKSPACE SNAPSHOT 2026-08-25 (FULL BACKUP ON PHONE ✅)
- **Backup tarball:** `~/projects/hermes_game_studio/backups/workspace_20260825.tar.gz` — **88,199,698 bytes**, sha256 `021398a72cf2d20119b068a7c2dcfa2ac6c3680be39decbfdbe1a4b367b98bd4` (verified MATCH with sandbox)
- **Extracted snapshot:** `~/projects/hermes_game_studio/workspace_snapshot_20260825/` — **116 files, 91MB**
- Transfer method: MQTT `put_file` chunked **700KB x 124 parts** → reassembled + sha verified (broker packet limit ~700KB; HTTP preview path BLOCKED by e2b traffic token — do not retry)
- Tool: `bridge/sync_push.py` (resumable, state `/tmp/sync_state.json`, parts `/tmp/sync_parts/`)
- Excluded from snapshot: `arch_release/`, `arena_ai_simulator_archlinux.*`, `install_arena_studio.sh` (Arch — Boss said ignore), `.local/` (pip pkgs)
- **LIVE GAME DEPLOYED:** `builds/arena_ai_simulator/index.html` = **10,216,965 bytes**, title **"ARENA AI TYCOON - PROPORTIONAL SPRITES & DIRECTIONAL WALKING"**, `ARENA AI TYCOON` count=2 → server restarted, **HTTP 200** ✅
- Old Gate5 build saved as `index.html.bak_gate5` (do not restore unless Boss says so)

### Base
- **Project root:** `~/projects/hermes_game_studio/`
- **Active build dir:** `~/projects/hermes_game_studio/builds/arena_ai_simulator/` (serve: `index.html` + `server.py`)
- **Server:** `fuser -k 8888/tcp; nohup python3 server.py > server.log 2>&1 &` → `http://localhost:8888`
- **Docs dir:** `~/projects/hermes_game_studio/docs/` (pitch G1, brainstorm, GDD G2, audio G3, SUBAGENT_SKILLSET_AUDIT, SUBAGENT_MODEL_MATRIX, TEAM_CHALLENGE_ANALYSIS)
- **ArenaBridge Worker v4 (SYNC+APPROVALS):** `python ~/arenabridge/worker.py` (Termux)
  - SID `53cf4a5803c91726b892e5d0785085c6` · key `[REDACTED-see-~/arenabridge/arenabridge.key]`
  - brokers: `broker.emqx.io` (primary), `broker.hivemq.com`, `test.mosquitto.org`
  - topics `arenabridge/{SID}/cmd` / `/res` — HMAC-authenticated
  - Sandbox client: `bash /home/user/mq.sh ping` | `bash /home/user/mq.sh send "<cmd>"`
  - ⚠️ Worker can time out (Termux/browser app switch) → Boss asked to just restart `python ~/arenabridge/worker.py`
- **Ollama:** `nohup ollama serve > ~/projects/hermes_game_studio/ollama.log 2>&1 &` (localhost:11434)

---

## 7. QA LOG (Jax findings → fixes)
| # | Finding | Owner | Status |
|---|---------|-------|--------|
| Q1 | Character too big vs background NPCs | Pixel | ✅ FIXED (sw=28 natural scale) |
| Q2 | Always front-facing, no side/back views while walking | Pixel+Cody | ⚠️ PARTIAL (flip/tint only — true frames pending) |
| Q3 | Minimap + compiler HUD covered main display | Cody | ✅ FIXED (removed) |
| Q4 | Legacy "castlevania_stage1" in phone repo | Jax | ✅ FIXED (deleted; path locked) |
| Q5 | Title screen not lean; no team group image | Pixel | ✅ FIXED (arena_ai_tycoon_title.png embedded) |
| Q6 | Layout switcher still active / wrong office | Cody | ✅ FIXED (1080p locked, switcher disabled) |

---

## 8. BACKLOG / NEXT GATES
- [ ] **G-NEXT (Pixel):** Generate **5 more** directional sprite sheets (Marcus, Echo, Vortex, Vanguard, Chronos) — replace the lost "additional 4 images" batch.
- [ ] **G-NEXT (Pixel+Cody):** Slice `sprite_opt1..5` + new sheets into **true 4-direction frames** (down/front, left, right, up/back) with **transparent backgrounds**; wire into renderer (replace flip/tint hack).
- [ ] **G-NEXT (Cody):** Idle (stand) + walk animation cycles (2-step + bob already partial).
- [ ] **G-NEXT (Jax):** Full mobile QA pass with screenshots (Chrome, Termux server, 8888).
- [ ] **G-NEXT (Zillion):** Re-deploy `index.html` → phone, restart server, verify title screen + sprites on device.
- [ ] Backlog: live LLM brains wiring via Ollama; PWA manifest; Beer Friday event; coffee-machine incident; dynamic soundtrack.
- ⚠️ **IMPORTANT (Jax):** The interrupted previous turn's "additional 4 images" did NOT persist — verify before declaring assets complete.

---

## 9. COMMAND CHEATSHEET (sandbox)
- Verify title bg embedded: `python3` script comparing sha256 of CSS `url(data:image...)` vs `images/arena_ai_tycoon_title.png` (last check: MATCH `e2e99c15…`)
- Rebuild: run `python3 build_proportional_directional.py` then re-verify title bg (builders overwrite → re-embed title image after build!)
- Deploy: `bash mq.sh send "python3 - <<'EOF' ... EOF"` (use `os.path.expanduser('~/…')` — `$HOME` does NOT expand in remote `sh`)
## 5c. ⏸️ SPRITE DIRECTION GATE — PAUSED (Boss order 2026-08-25)
- **"Wag muna i-enable, ayos na lahat, konti na lang tayo"** — Boss STOPPED the true 4-direction gate.
- Partial slicer work exists locally ONLY (sandbox, NOT deployed): `slice_bands.py`, `slice_sheets.py`, `dir_frames/` (zillion, cody, aria, pixel, jax 4-row sheets — aria/zillion rough, cody/pixel/jax good).
- ⚠️ DO NOT deploy dir_frames or change sprite rendering without Boss approval.
- **Live game = FINAL for now:** `builds/arena_ai_simulator/index.html` (10,216,965 B, ARENA AI TYCOON, HTTP 200). Uses natural scale sprites (sw=28) + flip/brightness directional simulation. Keep it as-is.
- Remaining backlog: 5 missing sheets (marcus, echo, vortex, vanguard, chronos) + finalize slicing + wire into renderer — resume only on Boss command.

## 5d. 🎯 MINIMAL MODE (Boss order 2026-08-25 — live NOW)
- **Boss: "Disable muna yung mga feature, konti na lang yung game."** → MINIMAL MODE **DEPLOYED & LIVE** sa phone.
- **MINIMAL disables:** 🛒 store (button+FAB+modal), 👑 boss spawn, 🍺 beer party, 🗺️ zone legend nav, 🎮 vertical switcher, 🕹️ arcade, 📊 3 stat bars.
- **MINIMAL keeps:** title screen (team image), office world + 10 agents, ⏰ 24h clock + day, 💬 dialogue/persona talk, 🔍 zoom, 💾 save/load, 🎵 BGM.
- **Toggle button:** small 🎯 pill bottom-left — `MODE: MINIMAL` ↔ `MODE: FULL`, persists via localStorage (`arena_mode`), no redeploy needed.
- **Files:** phone `builds/arena_ai_simulator/index.html` = minimal build (10,220,276 B, MINIMAL MODE LAYER ×1, HTTP 200 ✅). Full build backup = `index.html.bak_full` (10,216,965 B). Local sandbox masters: `index.html` (FULL) + `index_minimal.html` (MINIMAL) + `build_minimal_mode.py` + `deploy_minimal_remote.py` (remote variant, expanduser paths).
- **Deploy method used:** wrote `deploy_minimal_remote.py` (~4KB) to phone via MQTT put_file → ran it locally on phone → patched its own index.html → swap + restart. (No 10MB transfer needed.)

## 5e. 🧹 WORKSPACE CLEAN v2 (Boss order 2026-08-25 — FINAL STATE)
- **Boss: "Mapupuno na naman, dapat memory lang at bridge ang laman; lahat nasa phone storage ko."**
- **Local = 57KB ONLY:** `MEMORY_CORE.md`, `memory_core.json`, `bridge/`, `mq.sh`. (paho-mqtt reinstalled as bridge dependency; NOT project data.)
- **Phone = FULL ARCHIVE (208MB), everything verified:**
  - Live game: `builds/arena_ai_simulator/index.html` (MINIMAL build, sha `0016ee09…`, HTTP 200)
  - Full build backup: `index.html.bak_full` (sha `923b36fc…`)
  - Backup tar: `backups/workspace_20260825.tar.gz` (88MB, sha `021398a7…`)
  - Snapshot: `workspace_snapshot_20260825/` (116 files)
  - New work: `workspace_updates_20260825/` (9 files: build_minimal_mode.py, slice_bands.py, slice_sheets.py, dir_frames/*.png+meta — all pushed 2026-08-25, hashes verified)
  - Docs: `docs/` (memory core v2 + GDDs + audits)
- **⚠️ put_file lands in `~/arenabridge/workspace_mirror/` (SYNC_ROOT) — remember to `mv` to projects dir after push.**
- **All future work:** pull files from phone via `get_file`/tmpfiles, or build on phone directly with small scripts pushed via MQTT.


## 5f. 📱 PHONE = THE WORKSPACE (Boss order 2026-08-25 — STANDARD)
- **Boss: "Gamitin mo yung phone storage sa work profile ko."** → **PHONE STORAGE IS THE PRIMARY WORKSPACE. Period.**
- **Canonical workspace:** `/data/data/com.termux/files/home/projects/hermes_game_studio/` (209MB, work-profile Termux storage) — 87GB FREE on device.
- Contains: `builds/arena_ai_simulator/` (LIVE index.html minimal + index.html.bak_full), `backups/` (tar 88MB), `workspace_snapshot_20260825/`, `workspace_updates_20260825/`, `docs/`, `memory/`, `qa/`, `reports/`, `studio.py`, `zillion_studio_master.py`, `start_studio.sh`, `cli.py`, `AAA_STUDIO_ROADMAP.md`, ollama logs.
- **Sandbox (here) = READ-ONLY CONTROL ROOM, 57KB max:** MEMORY_CORE.md + memory_core.json + bridge/ + mq.sh only. Never keep project files here.
- **Workflow from now on (FAST, no big transfers):**
  1. Need to edit/build/run project stuff? → push small script via MQTT `put_file` (lands in `workspace_mirror/`, then `mv` to project) → run it ON the phone → done.
  2. Need a file back here? → `get_file` (<2MB) or phone→tmpfiles.org upload (big files).
  3. All game deploys happen on-phone (`builds/arena_ai_simulator/` + server restart via `fuser -k 8888/tcp`).
- Speed note: no more 100MB syncs in either direction. Phone stays source of truth.

## 5g. 📱 MOBILE FULLSCREEN COVER (Boss order 2026-08-25 — LIVE)
- **Boss (screenshot): "ang liit pag naka mobile, gawin natin whole screen."** → Fullscreen Cover patch **DEPLOYED & LIVE**.
- **What changed (2 patches on phone, `deploy_fs_patch.py` + `deploy_fs_patch2.py`):**
  - CCS: body/html 100%, `#game-wrapper` = 100dvh, no border/radius; canvas fills container (`aspect-ratio:auto`; 16/9 removed); `.canvas-container` flex:1; compact header/control/dialogue; hide header on short screens (<560px).
  - Render math: `clearRect/translate` now use `canvas.width/height`; world scale = `zoomScale * __fitScale` where `__fitScale = max(canvas.w/1600, canvas.h/900)` → **COVER fit (no letterbox, buong screen napupuno)**.
  - Touch/mouse: tap→world conversion + pan deltas now divide by `zoomScale * __fitScale` (was hard-coded 1600/900 vs clientWidth).
- **QA (Jax):** JS syntax-checked w/ node on the pulled copy — **3/3 script blocks OK, 0 errors**; sha phone-live `759c09f74e85cf569c5d214dfb8b0cdbe27f58f5aa2b55d5488e412c05b7e38e` = verified identical to checked copy; server **HTTP 200**; temp files cleaned.
- **Files (phone):** live `index.html` (10,222,556 B), backups: `index.html.bak_pre_fs` (minimal 10,220,279 B), `index.html.bak_pre_fs2` (patched-1), `index.html.bak_full` (full features). Scripts: `deploy_fs_patch.py`, `deploy_fs_patch2.py` in workspace_mirror.
- **Behavior note:** portrait phone => cover fit crops sides horizontally (map is 16:9 landscape); pan/pinch to explore; zoom range still 1.0–2.5.


## 5h. 🎬 TRUE 4-DIRECTION ANIMATION + LAYOUT FIX (Boss order 2026-08-25 — LIVE)
- **Boss (screenshot circles):** (1) title box+button sobrang taas → ibaba; (2) dialogue box lumalabas sa title screen → dapat sa loob ng game lang; (3) PRIORITY: pangit animation — naka-harap lagi, static emps kahit steady, kailangan tamang galaw + mini dialogue.
- **Pixel:** generated 5 missing directional sheets (marcus, echo, vortex, vanguard, chronos) + 2 improved (zillion, aria) in exact 16-bit chibi style (4 rows: down/up/left/right × 3 frames); compiled ALL 10 into clean transparent sheets (`/tmp/anim_sheets` → phone `~/projects/hermes_game_studio/anim_sheets_master/`).
- **Cody:** patch_anim.py (6 patches): ASSETS +10 dir sheets (~1.4MB base64), dirSprites loader, updateSimulation `isMoving`+`walkFrame%3`+ambient idle bubbles, render true 4-direction frames with walk cycle (frame0=stand, 1-2=steps; NO bob when idle), title screen content anchored lower (flex-end + 6vh), dialogue hidden while title screen up (shown on startPlay).
- **QA (Jax):** node syntax 3/3 OK; deployed file sha `e7e04a1ce1c56cf68b914eba8c559af387363bf692a3eb60081c4168c3022bf4` EXACT match local verified; server HTTP 200; backup `index.html.bak_pre_anim` (11,689,829 B? no — bak_pre_anim = 10,222,356 pre-anim live).
- **Files (phone):** live `index.html` 11,690,026 B; backups row: `index.html.bak_pre_anim` (no anim), `index.html.bak_pre_fs2`, `index.html.bak_pre_fs`, `index.html.bak_full`; source sheets `anim_sheets_master/` (11 files).
- **Backups on phone for rollback:** bak_pre_anim → back to pre-animation (fullscreen+minimal still on).


## 5i. 🔬 SPRITE SCALE + ZOOM + SPEECH BUBBLE FIX (Boss QA 2026-08-25 — LIVE)
- **Boss QA (screenshot):** "QA pls fix the animation priority" — sprites masyadong MALAKI vs background NPCs; masyadong zoomed-in sa portrait; speech bubble malaki.
- **Measure:** background NPC heads ~10px / full body ~35px (sa 1376x768 asset) → agents dapat ~34px world (dating 46px, ~35% sobra).
- **Fixes (deploy_scale_fix.py):** (1) `targetH 46→34` (NPC-scale match); (2) zoom defaults `1.4→1.0` (declaration, initialZoom, resetZoom, zoomDisp HTML); (3) **portrait auto-zoom**: sa FS applyFit, kung portrait (`innerHeight>innerWidth`) → zoomScale=1.0; (4) speech bubble compact: box 210x34→162x24, font 9/10px→8px, 34→26 chars, mas malapit sa ulo (y-58).
- **QA (Jax):** node syntax **3/3 OK**; deployed sha `ad8bb98d149f62f98dfb4111fbe6c5a703610bf25ae3a227dbe52400539997c2` EXACT match; server HTTP 200; backup `index.html.bak_pre_scale`.
- **Tool on phone:** `~/projects/hermes_game_studio/tools/deploy_scale_fix.py`.
- **Files (phone):** live `index.html` 11,690,226 B; backups: `bak_pre_scale` (11,690,026), `bak_pre_anim`, `bak_pre_fs2`, `bak_pre_fs`, `bak_full`.


## 5j. 🎬 GATE 7 — ANIMATION POLISH (APPROVED gate → LIVE)
- **Boss approved (1) → Gate 7 executed.** Root cause ng "pangit na animation" natukoy ng Jax via orientation analysis:
  - **Front/back rows OK sa lahat ng 10**; pero **side rows ng marami (zillion, marcus, aria?, pixel, echo, chronos, jax) PAREHO ang left/right direction** (AI generated same profile) → kaya hindi nagbabago ang side view.
- **Fixes (patch_gate7.py, +764 B):**
  1) **NATIVE_RIGHT flip:** characters na may genuine RIGHT row (cody, vortex, vanguard) → use row 3; lahat ng iba → RIGHT = LEFT row (row 2) **horizontally flipped** (guaranteed correct facing).
  2) **Walk cycle throttle:** `stepFrame % 9` — dahan-dahang paglakad (dating 60fps frame-switch = takbong garapal).
  3) **Idle breathing:** `sin(stepFrame*0.035)*0.5` — subtle 0.5px bob lang (walang talon).
- **QA (Jax):** node syntax 3/3 OK; deployed sha **c7489460**64... EXACT match; HTTP 200; backup `index.html.bak_pre_g7`.
- **Files:** live `index.html` 11,690,990 B; backups: `bak_pre_g7` (11,690,029), `bak_pre_scale`, `bak_pre_anim`, `bak_pre_fs2`, `bak_pre_fs`, `bak_full`. Tool: `~/projects/hermes_game_studio/tools/patch_gate7.py`.


## 5k. 🔄 GATE 8 — PER-CHARACTER SIDE MAPPING (Boss QA: "pag lakad pa kaliwa side view not present" — LIVE)
- **Boss QA:** paglalakad pakaliwa — walang tamang side view. Root cause: lahat ng characters gumamit ng row2 para sa KALIWA, pero **7/10 ang row2 ay nakaharap KANAN** (AI dup profile) o BACK view ang row3.
- **Full audit (Jax, visual ground truth sa lahat ng 10 sheets):**
  - row2 ay LEFT-facing: zillion, aria, cody, jax · row3 ay RIGHT-facing: cody, vortex, vanguard (vortex/vanguard swapped: row2=right, row3=left)
  - row2 ay RIGHT-facing (kailangan i-flip for left): marcus, pixel, echo, chronos · row3 BACK/FRONT/broken: zillion, aria (back), echo (front), jax (broken frame)
- **Fix (Gate 8):** `SIDE` map per character: `2` = row2 as-is, `3` = row3 as-is, `'2f'` = row2 flipped.
  zillion{left:2,right:2f} marcus{2f,2} aria{2,2f} cody{2,3} pixel{2f,2} echo{2f,2} vortex{3,2} jax{2,2f} vanguard{3,2} chronos{2f,2}
- **QA:** node syntax 3/3 OK; deployed sha **d339f056e21def9e9b67c77f9f179f6fd1158980cee532a331e2a7f03880ffe5** EXACT match; HTTP 200; backup `index.html.bak_pre_g8`.
- **Files:** live `index.html` 11,691,431 B; tool `~/projects/hermes_game_studio/tools/side_map_fix.py`.
- Result expected: LAHAT ng characters — pakaliwa = side view na nakatingin kaliwa, pakanan = side view na nakatingin kanan (native o flipped).


## 5l. 🧪 QA RIG + ROOT CAUSE FIX (Boss: "walang side view" — TOTOONG dahilan — LIVE)
- **Boss:** "Walang naka side view. Ask ko lang pano mag QA, nakikita ba nila yung game?" → **Bumuo tayo ng HEADLESS BROWSER QA RIG** (puppeteer sa sandbox, `qa/qa_visual.js`): binubuksan ang aktwal na game file, pinapatakbo, at kumukuha ng totoong screenshots + collision report. **Ang QA team AY NAKAKAKITA na ng game.**
- 🚨 **ROOT CAUSE (Jax):** Mula pa sa unang animation deploy (patch_anim.py), ang ASSETS injection ay **NAWALAN ng `data:image/png;base64,` prefix** sa lahat ng 10 `{id}_dir` entries → **HINDI NAG-LOAD ang directional sheets sa browser/phone** (`naturalWidth: 0` → laging front-fallback) — kaya lahat ng "side view" fixes (gate 7 side map, gate 8) ay tumatakbo sa patay na code path. **Ito ang totoong dahilan ng "walang side view"!**
- **FIX:** idagdag ang `data:image/png;base64,` prefix sa lahat ng 10 dir entries (gate9_fixed.html). Verified sa browser: `naturalWidth` 177/168/183... = **sheets LOAD na**.
- **GATE 9 (collision) kasama sa deploy:** WALL_GRID (80x45, built from office map: wall-color + black outline, morphological opening 4x4 + closing 3x3, comps >2500px) + A* `findPath` + movement rewrite (path-follow, walang cross-wall). A* verified sa Python: **0 no-path pairs sa lahat ng waypoint neighbors**.
- **QA RIG RESULTS (headless Chromium):** A/B/C/D/F screenshots (walk left/right/up/down + group); **E_collision_report: ZERO violations** (walang agent sa wall cell sa loob ng 7s+); naka-zoom shot A_zoom_left: **SIDE VIEWS VISIBLE** (Vanguard, Zillion side-facing).
- **QA (Jax):** node syntax 3/3 OK; deployed sha **bebd628a8cdca58fd53fe77dc3dea4bbf2dbbbd00efcdf0ca517784e6961b1eb** EXACT match; `data:image` prefix present, findPath x2, WALL_GRID 45 rows, server HTTP 200; backup `index.html.bak_pre_g9`.
- **Files:** live `index.html` 11,697,784 B; tools: `tools/patch_gate9.py`, `qa/qa_visual.js`; QA evidence: `qa/shots/*.png.gz` (A/B/F zooms + full shots).
- ⚠️ **LESSON:** laging mag-load-test sa browser before deploy (QA rig) — huwag umasa lang sa code review.

## 5m. 🎭 GATE 10 — GLITCH FIX + FOOT-STEP WALK + LIVING NPCs (Boss QA — LIVE)
- **Boss QA (screenshot):** (1) may glitch/transparent character si Jax; (2) naglalakad pero hindi gumagalaw ang paa, naka-lutang ng konti; (3) mga static NPC kahit nakatayo lang kailangan may movement + dialogue.
- **Fixes (patch_gate10.py):**
  1) **SOLIDIFY** sa loader: alpha < 48 → 0, else 255 (hard cut) → **WALANG GHOST/TRANSPARENT** (verified: jaxAlpha semi=0, solid=21453, pct 0.00%).
  2) **Grounded:** feet anchor `-dh + 3 + bob` (touching floor, hindi lutang), walk = step bounce ±0.8px + `ctx.rotate(±0.045)` tilt, frame alt; idle = 0.35px breathing lang.
  3) **8 STATIC NPCs** (positions validated sa WALL_GRID - lahat open floor): Intern Rei, HR Dana, Barista Nia, Trainee Ben, Janitor Oli, Security Sam, Accountant Faye, Agent Zed. May idle sway, 24px shuffle left/right (may tamang directional frames + SIDE map), at **periodic mini-dialogue bubbles** (Taglish phrases).
- **QA (QA rig headless Chromium):** violations=0 (6s, agents+NPCs); jaxAlpha 0% semi; shots 1_jax_idle_zoom (solid na, may duck), 2a/2b walk frames (frame change + side views visible), 3a/3b NPC bubbles (Agent Zed "Testing ng bagong shader!⚡" visible), 4_collision_6s. Node syntax 3/3 OK.
- **QA (Jax):** deployed sha **1d05db11e876946572c63cdc13df60b7faf7b63199592c0cebb854a25569883e** EXACT match; HTTP 200; backup `index.html.bak_pre_g10`.
- **Files:** live `index.html` 11,703,732 B; tools `tools/patch_gate10.py`, `qa/qa_g10.js`; evidence `qa/shots10/*` (local sandbox, delete-on-clean).

