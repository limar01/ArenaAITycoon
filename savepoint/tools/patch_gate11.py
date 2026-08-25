#!/usr/bin/env python3
"""
ARENA AI TYCOON — GATE 11 PATCH (Zillion, 2026-08-25)
Boss order: "Zillion ikaw na mag fix at mag QA" — feet don't move, no side/back view, NPCs static.

ROOT CAUSE (Jax + Zillion, headless-browser verified):
  Gate 10 solidified dirSprites[k] into a <canvas>, but the agent render guard still checked
  `dir.complete && dir.naturalWidth > 0` (Image-only props) -> always FALSE -> fallback front
  sprite. So side/back rows + walk frames never rendered. (NPC guard used `ds.width > 0`, so
  NPCs drew sheets but had no real idle motion.)

FIXES:
  F1  Agent guard accepts canvas (width>0) too.
  F2  Walk cycle: full 0->1->2 frame cycle + stronger bob/tilt + squash/stretch (feet visibly move).
  F3  NPCs: idle breathing bob + sway tilt + slow weight-shift frame cycle; more frequent
      shuffle + idle turns (alive even when standing still).
  F4  SIDE map: echo & vortex side rows both face LEFT (measured) -> left=row2, right=row2 flipped.
"""
import sys

def apply(html: str) -> str:
    out = html
    count = {}

    def rep(old, new, tag):
        n = out.count(old)
        assert n >= 1, f"NOT FOUND ({tag}): {old[:60]!r}"
        count[tag] = count.get(tag, 0) + n
        return out.replace(old, new)

    # ---- F1: agent render guard accepts canvas ----
    out = rep(
        "      const dir = dirSprites[a.id];\n"
        "      if (dir && dir.complete && dir.naturalWidth > 0) {",
        "      const dir = dirSprites[a.id];\n"
        "      if (dir && ((dir.complete && dir.naturalWidth > 0) || dir.width > 0)) {",
        "F1_guard")

    # ---- F2: agent walk cycle + animation ----
    out = rep(
        "        const moving = !!a.isMoving;\n"
        "        // frame 0 = stand/idle; frames 1-2 = walk steps\n"
        "        const frame = moving ? (1 + (a.walkFrame % 2)) : 0;\n"
        "        const sx = frame * fw;\n"
        "        const sy = row * fh;\n"
        "        const targetH = 34;\n"
        "        const scaleF = targetH / fh;\n"
        "        const dw = fw * scaleF;\n"
        "        const dh = fh * scaleF;\n"
        "        // grounded: feet touch floor; breathing when idle, step bounce + tilt when walking\n"
        "        const stepPh = (a.walkFrame % 2) === 0 ? -1 : 1;\n"
        "        const bob = moving ? stepPh * 0.8 : Math.sin(stepFrame * 0.03 + a.x * 0.05) * 0.35;\n"
        "        const tilt = moving ? stepPh * 0.045 : 0;",
        "        const moving = !!a.isMoving;\n"
        "        // frame 0 = stand/idle; frames 1-2 = walk steps (full 0->1->2 cycle = visible legs)\n"
        "        const frame = moving ? (a.walkFrame % 3) : 0;\n"
        "        const sx = frame * fw;\n"
        "        const sy = row * fh;\n"
        "        const targetH = 34;\n"
        "        const scaleF = targetH / fh;\n"
        "        const dw = fw * scaleF;\n"
        "        const dh = fh * scaleF;\n"
        "        // grounded feet; breathing idle; step bounce + tilt + squash/stretch when walking\n"
        "        const stepPh = (a.walkFrame % 2) === 0 ? -1 : 1;\n"
        "        const bob = moving ? stepPh * 1.5 : Math.sin(stepFrame * 0.03 + a.x * 0.05) * 0.5;\n"
        "        const tilt = moving ? stepPh * 0.07 : Math.sin(stepFrame * 0.02 + a.x) * 0.012;\n"
        "        const sq = moving ? 1 + stepPh * 0.03 : 1;",
        "F2_anim")

    out = rep(
        "        // True directional frame from spritesheet (with flip when needed)\n"
        "        if (flip) {\n"
        "          ctx.scale(-1, 1);\n"
        "        }\n"
        "        if (tilt) ctx.rotate(tilt);\n"
        "        ctx.drawImage(dir, sx, sy, fw, fh, -dw / 2, -dh + 3 + bob, dw, dh);\n"
        "        ctx.restore();",
        "        // True directional frame from spritesheet (with flip when needed)\n"
        "        if (flip) {\n"
        "          ctx.scale(-1, 1);\n"
        "        }\n"
        "        if (tilt) ctx.rotate(tilt);\n"
        "        ctx.scale(1, sq);\n"
        "        ctx.drawImage(dir, sx, sy, fw, fh, -dw / 2, -dh + 3 + bob, dw, dh);\n"
        "        ctx.restore();",
        "F2_draw")

    # ---- F4: SIDE map (agent) ----
    out = rep(
        "          echo:     { left: '2f', right: 2 },",
        "          echo:     { left: 2, right: '2f' },",
        "F4_echo")
    out = rep(
        "          vortex:   { left: 3, right: 2 },",
        "          vortex:   { left: 2, right: '2f' },",
        "F4_vortex")
    out = rep(
        "          cody:     { left: 2, right: 3 },",
        "          cody:     { left: 2, right: '2f' },",
        "F4_cody")

    # ---- F3: NPC render (idle motion) ----
    out = rep(
        "        const frame = n.isMoving ? (1 + (n.walkFrame % 2)) : 0;\n"
        "        const sx = frame * fw;\n"
        "        const targetH = 34, scaleF = targetH / fh;\n"
        "        const dw = fw * scaleF, dh = fh * scaleF;\n"
        "        const bob = n.isMoving ? ((n.walkFrame % 2 === 0 ? -1 : 1) * 0.7) : Math.sin(stepFrame * 0.03 + n.x) * 0.3;\n"
        "        ctx.save();\n"
        "        ctx.translate(n.x, n.y);",
        "        const frame = n.isMoving ? (n.walkFrame % 3) : (Math.floor(stepFrame / 16) % 3);\n"
        "        const sx = frame * fw;\n"
        "        const targetH = 34, scaleF = targetH / fh;\n"
        "        const dw = fw * scaleF, dh = fh * scaleF;\n"
        "        const stepPhN = (n.walkFrame % 2) === 0 ? -1 : 1;\n"
        "        const bob = n.isMoving ? (stepPhN * 1.2) : Math.sin(stepFrame * 0.03 + n.x) * 0.9;\n"
        "        const tiltN = n.isMoving ? (stepPhN * 0.05) : Math.sin(stepFrame * 0.018 + n.x) * 0.02;\n"
        "        ctx.save();\n"
        "        ctx.translate(n.x, n.y);",
        "F3_npc_anim")

    out = rep(
        "        if (flip) ctx.scale(-1, 1);\n"
        "        ctx.drawImage(ds, sx, sy2, fw, fh, -dw / 2, -dh + 3 + bob, dw, dh);\n"
        "        ctx.restore();",
        "        if (flip) ctx.scale(-1, 1);\n"
        "        if (tiltN) ctx.rotate(tiltN);\n"
        "        ctx.drawImage(ds, sx, sy2, fw, fh, -dw / 2, -dh + 3 + bob, dw, dh);\n"
        "        ctx.restore();",
        "F3_npc_draw")

    # ---- F4: SIDE_N map (NPC) ----
    out = rep(
        "echo:{left:'2f',right:2}",
        "echo:{left:2,right:'2f'}",
        "F4_npc_echo")
    out = rep(
        "vortex:{left:3,right:2}",
        "vortex:{left:2,right:'2f'}",
        "F4_npc_vortex")
    out = rep(
        "cody:{left:2,right:3}",
        "cody:{left:2,right:'2f'}",
        "F4_npc_cody")

    # ---- F3b: NPC update — more alive (frequent shuffle + idle turns) ----
    out = rep(
        "    } else if (n.timer <= 0) {\n"
        "      const roll = Math.random();\n"
        "      if (roll < 0.5) {\n"
        "        // mini dialogue bubble\n"
        "        activeBubble = { agent: n, text: n.name + ': ' + n.phrase };\n"
        "        bubbleTimer = 140;\n"
        "        playSFX('blip');\n"
        "        n.timer = 260 + Math.floor(Math.random() * 320);\n"
        "      } else if (roll < 0.8 && !n.isMoving) {\n"
        "        // small shuffle 24px to the side then back\n"
        "        n.shift = (Math.random() < 0.5 ? -1 : 1) * 24;\n"
        "        n.isMoving = true;\n"
        "        n.timer = 220 + Math.floor(Math.random() * 240);\n"
        "      } else {\n"
        "        n.timer = 200 + Math.floor(Math.random() * 300);\n"
        "      }\n"
        "    }",
        "    } else if (n.timer <= 0) {\n"
        "      const roll = Math.random();\n"
        "      if (roll < 0.35) {\n"
        "        // mini dialogue bubble\n"
        "        activeBubble = { agent: n, text: n.name + ': ' + n.phrase };\n"
        "        bubbleTimer = 140;\n"
        "        playSFX('blip');\n"
        "        n.timer = 150 + Math.floor(Math.random() * 220);\n"
        "      } else if (roll < 0.75 && !n.isMoving) {\n"
        "        // small shuffle 24px to the side then back\n"
        "        n.shift = (Math.random() < 0.5 ? -1 : 1) * 24;\n"
        "        n.isMoving = true;\n"
        "        n.timer = 110 + Math.floor(Math.random() * 160);\n"
        "      } else if (!n.isMoving) {\n"
        "        // idle turn to another direction (looks alive)\n"
        "        const dirs = ['down', 'up', 'left', 'right'];\n"
        "        n.facing = dirs[Math.floor(Math.random() * 4)];\n"
        "        n.timer = 100 + Math.floor(Math.random() * 180);\n"
        "      } else {\n"
        "        n.timer = 120 + Math.floor(Math.random() * 200);\n"
        "      }\n"
        "    }",
        "F3_npc_update")

    return out, count


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "game.html"
    src = open(path, encoding="utf-8", errors="replace").read()
    new, count = apply(src)
    open(path, "w", encoding="utf-8").write(new)
    print("PATCH OK —", count)
    print("size:", len(src), "->", len(new))
