# claude-skills

A collection of Claude Code skills — installable, zero dependencies, built for real workflows.

Skills are markdown files that Claude reads at invocation time. They give Claude specialized knowledge and step-by-step instructions for specific tasks — without burning tokens on repeated setup.

## How skills work

When you invoke a skill, Claude loads a focused instruction set (<5k tokens) instead of relying on your system prompt or project context. Skills use a three-tier model:
1. ~100 token metadata scan (name + description) — always loaded
2. Full SKILL.md — loaded on invocation
3. Referenced sub-files — loaded on demand

## Install

**Claude Code (recommended):**
```
/plugin marketplace add nischal94/claude-skills
```

**Manual:**
```bash
git clone https://github.com/nischal94/claude-skills.git ~/.claude/skills/claude-skills
```

## Skills

| Skill | Description |
|-------|-------------|
| [html-to-image](./html-to-image/) | Convert HTML files to high-resolution PNG or JPEG using Puppeteer and system Chrome. No browser download required. |
| [design-eng](https://github.com/emilkowalski/skill) | UI polish, component design, animation decisions, and the invisible details that make software feel great. |

## Requirements

- [Claude Code](https://claude.ai/code)
- macOS (current skills assume macOS paths)
- Node.js + npm (for `html-to-image`)
- Google Chrome installed at `/Applications/Google Chrome.app`

## License

MIT
