# Contributing

Skills in this repo follow a consistent structure so Claude can reliably load and execute them.

## Skill structure

```
your-skill/
├── SKILL.md          ← required — the instruction set Claude follows
├── spec.md           ← optional — design decisions and rationale
├── scripts/          ← optional — executable helpers
├── references/       ← optional — reference docs loaded into context
└── assets/           ← optional — templates, fonts, images
```

## SKILL.md format

```markdown
---
name: skill-name
description: One sentence describing what it does and when Claude should use it.
---

# Skill Title

## When invoked
[How the user calls this skill]

## Steps
[Numbered steps Claude follows]

## Error reference
[Table of failure modes and how to handle them]
```

## Guidelines

- Instructions are written for Claude, not the user — use imperative form
- Every step that involves code must show the actual code, not a description
- Every error case must have an explicit action (never "handle gracefully")
- No external dependencies unless absolutely necessary
- macOS-first is fine; document platform assumptions clearly
- Test the skill end-to-end before submitting

## Adding a skill

1. Fork the repo
2. Create `your-skill/SKILL.md`
3. Add a row to the skills table in `README.md`
4. Open a PR with title `feat: add <skill-name> skill`
