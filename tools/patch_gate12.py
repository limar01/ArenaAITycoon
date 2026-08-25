#!/usr/bin/env python3
"""GATE 12 — LIVE LLM BRAINS (Ollama) patch for ARENA AI TYCOON
Zillion (lead) + Cody (programmer) — Boss-approved 2026-08-25

3 surgical replacements on builds/arena_ai_simulator/index.html:
  R1: inject LLM engine before function setDialogue
  R2: hook llmAsk(a,'tap') into agent tap handler
  R3: hook llmAmbient() into updateSimulation (ambient chatter)

Design: live Ollama fetch (CORS verified OK) + 60s guard + 3-fail
auto-disable + scripted-phrase fallback (zero regression if Ollama off).
"""
import sys, shutil, hashlib

PATH = sys.argv[1] if len(sys.argv) > 1 else "index.html"

LLM_BLOCK = r'''// ===== GATE 12: LIVE LLM BRAINS (Ollama on phone) — Zillion/Cody =====
const LLM = {
  url: 'http://127.0.0.1:11434/api/generate',
  enabled: true, busy: false, fails: 0,
  ambientTimer: 1500 + Math.floor(Math.random() * 2400),
  models: {
    zillion: 'qwen2.5:1.5b', marcus: 'llama3.2:1b', aria: 'llama3.2:1b',
    cody: 'qwen2.5-coder:1.5b', pixel: 'qwen2.5:1.5b', echo: 'qwen2.5:1.5b',
    vortex: 'qwen2.5-coder:1.5b', jax: 'deepseek-r1:1.5b',
    vanguard: 'deepseek-r1:1.5b', chronos: 'qwen2.5:1.5b'
  },
  personas: {
    zillion: 'calm technical director who loves clean architecture and speaks with quiet confidence',
    marcus: 'energetic producer and Beer Friday champion who calls the player Boss and stays optimistic',
    aria: 'thoughtful systems designer who loves game balance and is occasionally poetic',
    cody: 'laser-focused lead programmer who speaks in short technical bursts and is proud of 60 FPS',
    pixel: 'passionate pixel artist obsessed with 16-bit retro aesthetics',
    echo: 'chill audio director who uses music metaphors and laid-back vibes',
    vortex: 'intense shader architect obsessed with neon graphics who talks fast',
    jax: 'sharp QA bug hunter, skeptical, spots bugs everywhere, loves his rubber duck',
    vanguard: 'strict AAA quality judge, formal and demanding, respects only excellence',
    chronos: 'wise memory keeper, nostalgic, speaks about time and saving things'
  }
};

function llmClean(t) {
  t = (t || '').replace(/<think>[\s\S]*?<\/think>/gi, '').replace(/<\/?think>/gi, '').trim();
  t = t.replace(/^["'\u201c]|["'\u201d]$/g, '').trim();
  if (t.length > 140) {
    const cut = t.slice(0, 140);
    const p = Math.max(cut.lastIndexOf('.'), cut.lastIndexOf('!'), cut.lastIndexOf('?'));
    t = p > 50 ? cut.slice(0, p + 1) : cut + '...';
  }
  return t;
}

function llmApply(ag, line, mode) {
  ag.phrase = line;
  setDialogue(ag);
  if (mode === 'tap' && activeBubble && activeBubble.agent === ag && bubbleTimer > 0) {
    activeBubble.text = ag.name + ': ' + line;
    if (bubbleTimer < 150) bubbleTimer = 150;
  }
}

function llmAsk(ag, mode) {
  if (!LLM.enabled || LLM.busy) return;
  const model = LLM.models[ag.id] || 'llama3.2:1b';
  const persona = LLM.personas[ag.id] || ag.role;
  const situation = mode === 'tap' ? 'The Boss just walked up to talk to you' : 'It is a normal workday moment in the office';
  const prompt = 'You are ' + ag.name + ', ' + ag.role + ' at the Arena AI Tycoon game studio in Manila. Personality: ' + persona + '. ' + situation + '. Reply with exactly ONE short casual Taglish sentence (natural mix of Tagalog and English, maximum 16 words). Speak as ' + ag.name + '. No quotes, no emoji, no explanation.';
  const isR1 = model.indexOf('deepseek') === 0;
  LLM.busy = true;
  if (mode === 'tap') diagMessage.innerText = '\uD83D\uDCAD ' + ag.name + ' is thinking... (live AI brain)';
  const guard = setTimeout(() => {
    if (LLM.busy) { LLM.busy = false; LLM.fails++; if (LLM.fails >= 3) LLM.enabled = false; if (mode === 'tap') setDialogue(ag); }
  }, 60000);
  fetch(LLM.url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: model, prompt: prompt, stream: false, options: { num_predict: isR1 ? 120 : 40, temperature: 0.9 } })
  }).then(r => r.json()).then(j => {
    clearTimeout(guard); LLM.busy = false;
    const line = llmClean(j && j.response);
    if (line) { LLM.fails = 0; llmApply(ag, line, mode); }
    else if (mode === 'tap') setDialogue(ag);
  }).catch(() => {
    clearTimeout(guard); LLM.busy = false; LLM.fails++;
    if (LLM.fails >= 3) LLM.enabled = false;
    if (mode === 'tap') setDialogue(ag);
  });
}

function llmAmbient() {
  if (!LLM.enabled || LLM.busy) return;
  if (--LLM.ambientTimer > 0) return;
  LLM.ambientTimer = 2700 + Math.floor(Math.random() * 2700);
  llmAsk(agents[Math.floor(Math.random() * agents.length)], 'ambient');
}

function setDialogue(ag) {'''

R1_ANCHOR = "function setDialogue(ag) {"

R2_ANCHOR = '''      updatePortrait(i);
      activeBubble = { agent: a, text: a.name + ": " + a.phrase };
      bubbleTimer = 220;
      playSFX('blip');
      return;'''

R2_NEW = '''      updatePortrait(i);
      activeBubble = { agent: a, text: a.name + ": " + a.phrase };
      bubbleTimer = 220;
      playSFX('blip');
      llmAsk(a, 'tap');
      return;'''

R3_ANCHOR = '''  updateClock();

  if (bossAvatarActive) {'''

R3_NEW = '''  updateClock();
  llmAmbient();

  if (bossAvatarActive) {'''


def main():
    html = open(PATH, encoding="utf-8").read()
    orig_len = len(html)

    if "GATE 12: LIVE LLM BRAINS" in html:
        print("ALREADY PATCHED — abort (idempotent guard)")
        return 1

    # sanity: each anchor must appear exactly once
    for name, anchor in [("R1", R1_ANCHOR), ("R2", R2_ANCHOR), ("R3", R3_ANCHOR)]:
        n = html.count(anchor)
        if n != 1:
            print(f"ANCHOR {name} count={n} (expected 1) — ABORT, file untouched")
            return 1

    shutil.copyfile(PATH, PATH + ".bak_pre_g12")

    html = html.replace(R1_ANCHOR, LLM_BLOCK, 1)
    html = html.replace(R2_ANCHOR, R2_NEW, 1)
    html = html.replace(R3_ANCHOR, R3_NEW, 1)

    open(PATH, "w", encoding="utf-8").write(html)

    new_len = len(html)
    print(f"PATCHED OK: {orig_len:,} -> {new_len:,} chars (+{new_len - orig_len:,})")
    print("checks: LLM block x" + str(html.count("GATE 12: LIVE LLM BRAINS"))
          + " llmAsk x" + str(html.count("llmAsk"))
          + " llmAmbient x" + str(html.count("llmAmbient"))
          + " models-map x" + str(html.count("deepseek-r1:1.5b")))
    print("sha256:", hashlib.sha256(open(PATH, 'rb').read()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
