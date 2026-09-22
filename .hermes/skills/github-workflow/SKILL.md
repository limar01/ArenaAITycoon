---
name: github-workflow
description: "Project adapter over global github/* skills: remotes, deploy keys, push policy."
version: 1.0.0
platforms: [linux]
metadata: {hermes: {tags: [github]}}
related_skills: [git-safe-workflow]
---
# GitHub Workflow (project adapter)
REUSE global: github/auth, github-pr-workflow, github-repo-management, github-code-review.
Project policy: no PATs in remotes (doctrine rule 12); pushes via registered deploy keys only; ArenaAITycoon push path PENDING Boss decision (audit §7.3) — local commits until then.
