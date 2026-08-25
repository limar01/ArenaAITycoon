#!/usr/bin/env python3
"""GATE 14 — LIVING OFFICE patch for ARENA AI TYCOON
Day cycle (rollover + weekday), auto Beer Friday, Coffee Machine Incident
event (smoke + LLM-aware complaints + fix resolution), dynamic time-of-day
BGM (morning/midday/evening/night/party), event-aware LLM situations.
8 surgical replacements. Idempotent. Zillion/Cody/Aria — 2026-08-25.
"""
import sys, shutil, hashlib

PATH = sys.argv[1] if len(sys.argv) > 1 else "index.html"

G14_BLOCK = "// ===== GATE 14: LIVING OFFICE (day cycle + events + dynamic BGM) — Zillion/Cody/Aria =====\nconst DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];\nfunction dayOfWeek() { return (inGameDay + 3) % 7; } // 0=Mon..6=Sun (day 43 = Friday)\nfunction isFridayNow() { return dayOfWeek() === 4; }\nfunction updateDayDisplay() { dayDisplay.innerText = inGameDay + ' \\u00b7 ' + DAY_NAMES[dayOfWeek()]; }\nlet partyTriggeredToday = false;\nlet coffeeIncident = { active: false, until: 0, smoke: [], lastBubble: 0, lastCheck: -1 };\n\nfunction tickCoffeeIncident() {\n  if (coffeeIncident.active) {\n    if (stepFrame % 3 === 0) coffeeIncident.smoke.push({ x: 1130 + (Math.random() * 30 - 15), y: 706, r: 3, a: 0.5 });\n    for (let s of coffeeIncident.smoke) { s.y -= 0.8; s.x += Math.sin(s.y * 0.05) * 0.4; s.r += 0.16; s.a -= 0.008; }\n    coffeeIncident.smoke = coffeeIncident.smoke.filter(s => s.a > 0);\n    if (stepFrame - coffeeIncident.lastBubble > 420) {\n      coffeeIncident.lastBubble = stepFrame;\n      const near = agents.filter(a => Math.hypot(a.x - 1130, a.y - 720) < 280);\n      if (near.length) {\n        const a = near[Math.floor(Math.random() * near.length)];\n        activeBubble = { agent: a, text: a.name + ': ' + a.phrase };\n        bubbleTimer = 200;\n        llmAsk(a, 'ambient');\n      }\n    }\n    if (simMinutes >= coffeeIncident.until) {\n      coffeeIncident.active = false; coffeeIncident.smoke = [];\n      activeBubble = { agent: { name: 'Coffee Machine', x: 1130, y: 700 }, text: 'Cody fixed the coffee machine! \\u2615\\u2705 Espresso flow restored!' };\n      bubbleTimer = 220; playSFX('cheer');\n    }\n    return;\n  }\n  const hr = Math.floor(simMinutes / 60);\n  if (hr !== coffeeIncident.lastCheck && hr >= 9 && hr < 16 && Math.random() < 0.22) {\n    coffeeIncident.lastCheck = hr;\n    coffeeIncident.active = true;\n    coffeeIncident.until = simMinutes + 300;\n    coffeeIncident.lastBubble = stepFrame;\n    activeBubble = { agent: { name: 'Coffee Machine', x: 1130, y: 700 }, text: '\\u2615\\ud83d\\udca5 SIRANG SIRA ANG COFFEE MACHINE! May usok! Kailangan ng kape ang lahat!' };\n    bubbleTimer = 240; playSFX('pool_hit');\n  }\n}\n\nfunction bgmPeriod() {\n  const h = Math.floor(simMinutes / 60);\n  if (isBeerFriday) return 'party';\n  if (h >= 6 && h < 11) return 'morning';\n  if (h >= 11 && h < 16) return 'midday';\n  if (h >= 16 && h < 22) return 'evening';\n  return 'night';\n}\nconst BGM_PERIODS = {\n  morning: { type: 'triangle', skip: 1, notes: [261.63, 293.66, 329.63, 392.00, 440.00, 392.00, 329.63, 293.66] },\n  midday:  { type: 'triangle', skip: 0, notes: [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 440.00, 493.88] },\n  evening: { type: 'sine',     skip: 1, notes: [220.00, 261.63, 293.66, 329.63, 293.66, 261.63, 220.00, 196.00] },\n  night:   { type: 'sine',     skip: 2, notes: [196.00, 220.00, 246.94, 196.00] },\n  party:   { type: 'square',   skip: 0, notes: [392.00, 440.00, 493.88, 523.25, 587.33, 523.25, 493.88, 440.00] }\n};\nupdateDayDisplay();\n\nfunction updateClock() {"

R1B_ANCHOR = "  simMinutes = (simMinutes + 0.15) % (24 * 60);"
R1B_NEW = '  const prevSim = simMinutes;\n  simMinutes = (simMinutes + 0.15) % (24 * 60);\n  if (simMinutes < prevSim) {\n    inGameDay++;\n    partyTriggeredToday = false;\n    if (isBeerFriday) toggleParty();\n    updateDayDisplay();\n  }'

R2_ANCHOR = "  if (hrs === 16 && mins === 0 && !isBeerFriday) {\n    toggleParty();\n  }"
R2_NEW = "  if (hrs >= 16 && hrs < 21 && !isBeerFriday && !partyTriggeredToday && isFridayNow()) {\n    partyTriggeredToday = true;\n    toggleParty();\n    setDialogue({ name: 'Marcus', role: 'Producer', phrase: 'BEER FRIDAY NA, Boss! \\ud83c\\udf7a Tapikin mo ako para sa live AI greeting!' });\n    llmAsk(agents[1], 'ambient');\n  }\n  if (hrs === 0 && mins < 1 && isBeerFriday) {\n    toggleParty();\n    setDialogue({ name: 'Chronos', role: 'Memory Anchor', phrase: 'New day, new save point! \\u{1f570}\\ufe0f Naka-save ang progress natin kahapon.' });\n  }"

R3_ANCHOR = "  updateClock();\n  llmAmbient();"
R3_NEW = "  updateClock();\n  llmAmbient();\n  tickCoffeeIncident();"

R4_ANCHOR = 'function startBGM() {\n  if (bgmPlaying || !actx) return;\n  bgmPlaying = true;\n  bgmBtn.innerText = "BGM: ON 🔊";\n  const notes = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 440.00, 493.88];\n  let noteIdx = 0;\n  if (bgmInterval) clearInterval(bgmInterval);\n  bgmInterval = setInterval(() => {\n    try {\n      if (!bgmPlaying || !actx || gameState === 2) return;\n      const now = actx.currentTime;\n      const osc = actx.createOscillator();\n      osc.type = isBeerFriday ? \'square\' : \'triangle\';\n      osc.frequency.setValueAtTime(notes[noteIdx], now);\n      const noteGain = actx.createGain();\n      noteGain.gain.setValueAtTime(0.025, now);\n      noteGain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);\n      osc.connect(noteGain);\n      noteGain.connect(actx.destination);\n      osc.start(now);\n      osc.stop(now + 0.18);\n      noteIdx = (noteIdx + 1) % notes.length;\n    } catch(e){}\n  }, 200);\n}'
R4_NEW = 'function startBGM() {\n  if (!actx) return;\n  bgmPlaying = true;\n  bgmBtn.innerText = "BGM: ON \\ud83d\\udd0a";\n  if (bgmInterval) clearInterval(bgmInterval);\n  let noteIdx = 0;\n  let tickN = 0;\n  let curPeriod = bgmPeriod();\n  let cfg = BGM_PERIODS[curPeriod] || BGM_PERIODS.midday;\n  bgmInterval = setInterval(() => {\n    try {\n      if (!bgmPlaying || !actx || gameState === 2) return;\n      tickN++;\n      const p = bgmPeriod();\n      if (p !== curPeriod) { curPeriod = p; cfg = BGM_PERIODS[p] || BGM_PERIODS.midday; noteIdx = 0; tickN = 0; }\n      if (cfg.skip && (tickN % (cfg.skip + 1) !== 1)) return;\n      const now = actx.currentTime;\n      const osc = actx.createOscillator();\n      osc.type = cfg.type;\n      osc.frequency.setValueAtTime(cfg.notes[noteIdx], now);\n      const noteGain = actx.createGain();\n      noteGain.gain.setValueAtTime(cfg.type === \'square\' ? 0.02 : 0.025, now);\n      noteGain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);\n      osc.connect(noteGain);\n      noteGain.connect(actx.destination);\n      osc.start(now);\n      osc.stop(now + 0.18);\n      noteIdx = (noteIdx + 1) % cfg.notes.length;\n    } catch(e){}\n  }, 200);\n}'

R5_ANCHOR = "const situation = mode === 'tap' ? 'The Boss just walked up to talk to you' : 'It is a normal workday moment in the office';"
R5_NEW = "const situation = mode === 'tap' ? 'The Boss just walked up to talk to you' : (typeof coffeeIncident !== 'undefined' && coffeeIncident.active ? 'The coffee machine just broke down and is smoking nearby, everyone is grumpy without caffeine' : (isBeerFriday ? 'It is Beer Friday party time in the office, music playing and drinks flowing' : (Math.floor(simMinutes / 60) < 12 ? 'It is a calm morning in the office' : 'It is a normal workday moment in the office')));"

R6_ANCHOR = "    dayDisplay.innerText = inGameDay;"
R6_NEW = "    updateDayDisplay();"

R7_ANCHOR = "if (bubbleTimer > 0 && activeBubble) {"
R7_NEW = "// GATE 14: coffee machine smoke render\nif (typeof coffeeIncident !== 'undefined' && coffeeIncident.active) {\n  for (let s of coffeeIncident.smoke) {\n    ctx.globalAlpha = Math.max(0, Math.min(1, s.a));\n    ctx.fillStyle = '#9aa3ad';\n    ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); ctx.fill();\n  }\n  ctx.globalAlpha = 1;\n  ctx.font = 'bold 13px monospace';\n  ctx.fillStyle = '#ffcc00';\n  ctx.fillText('\\u2615\\ud83d\\udca5', 1116, 688);\n}\nif (bubbleTimer > 0 && activeBubble) {"


def main():
    html = open(PATH, encoding="utf-8").read()
    orig_len = len(html)

    if "GATE 14: LIVING OFFICE" in html:
        print("ALREADY PATCHED — abort (idempotent guard)")
        return 1

    repls = [
        ("R1a-inject", "function updateClock() {", G14_BLOCK),
        ("R1b-rollover", R1B_ANCHOR, R1B_NEW),
        ("R2-beerfriday", R2_ANCHOR, R2_NEW),
        ("R3-tick", R3_ANCHOR, R3_NEW),
        ("R4-bgm", R4_ANCHOR, R4_NEW),
        ("R5-situation", R5_ANCHOR, R5_NEW),
        ("R6-day", R6_ANCHOR, R6_NEW),
        ("R7-smoke", R7_ANCHOR, R7_NEW),
    ]

    for name, anchor, new in repls:
        n = html.count(anchor)
        if n != 1:
            print(f"ANCHOR {name} count={n} (expected 1) — ABORT, file untouched")
            return 1
        html = html.replace(anchor, new, 1)

    shutil.copyfile(PATH, PATH + ".bak_pre_g14")

    open(PATH, "w", encoding="utf-8").write(html)
    new_len = len(html)
    print(f"PATCHED OK: {orig_len:,} -> {new_len:,} chars (+{new_len - orig_len:,})")
    print("checks: G14 x" + str(html.count("GATE 14: LIVING OFFICE"))
          + " dayNames x" + str(html.count("DAY_NAMES"))
          + " coffee x" + str(html.count("tickCoffeeIncident"))
          + " bgmPeriods x" + str(html.count("BGM_PERIODS"))
          + " partyCycle x" + str(html.count("partyTriggeredToday")))
    print("sha256:", hashlib.sha256(open(PATH, "rb").read()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
