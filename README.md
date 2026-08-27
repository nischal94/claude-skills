# skills

**Production-grade agent skills — map your unknowns before you build, prove you understand what shipped, turn work into artifacts people read, and transcribe any video offline.**

[![License: MIT](https://img.shields.io/badge/License-MIT-0e6b5c.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-8-1c2b2a.svg)](#the-skills)
[![CI](https://img.shields.io/badge/CI-validated%20%2B%20pinned-0e6b5c.svg)](./.github/workflows)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-9a6a1e.svg)](./CONTRIBUTING.md)

Skills are focused instruction sets that an agent loads on demand. Each one packages a proven workflow — with its checklists, output formats, and guardrails — so you get the same high-quality result every time, in any project, without re-explaining your process.

Built for [Claude Code](https://claude.ai/code), portable by format: every skill is a standard `SKILL.md` with YAML frontmatter (the open Agent Skills convention), so any agent or installer that reads the format can use them. A few skills use Claude Code affordances — the Artifact tool, sandbox flags — and fall back to local equivalents elsewhere.

---

## Contents

- [Quick start](#quick-start)
- [The skills](#the-skills)
  - [Understanding & workflow](#understanding--workflow)
  - [Transcription](#transcription)
  - [Creation & design](#creation--design)
- [How skills work](#how-skills-work)
- [Repository layout](#repository-layout)
- [Requirements](#requirements)
- [Contributing & security](#contributing--security)
- [Credits](#credits)

---

## Quick start

**Install as a plugin in Claude Code (recommended):**

```
/plugin marketplace add nischal94/skills
```

**Or install manually:**

```bash
git clone https://github.com/nischal94/skills.git ~/.claude/skills/skills
```

**Then invoke any skill by name:**

```
/blindspot I'm adding a new auth provider and I don't know this part of the codebase.
```

---

## The skills

### Understanding & workflow

Three skills that operationalize one discipline: *surface what you don't know before implementing, and prove you understand what shipped before merging.*

#### `blindspot` — find your unknown unknowns first

Pre-implementation reconnaissance. **Codebase mode** explores the target area and produces blindspot cards — each names a pothole you didn't know existed, why it bites, the evidence, and a copyable prompt-fix — ending with a four-quadrant map of the task and one assembled implementation prompt. **Domain mode** teaches you the vocabulary of an unfamiliar field (color grading, backpressure, auth flows) until you can specify what you want.

```
/blindspot Codebase mode. Target: the policy engine I'm about to build.
I've read the spec but never touched the surrounding modules.
```

#### `explain-diff` — understand a change before you merge it

Turns any diff, commit, or PR into a rich HTML explainer: background on the surrounding system, the intuition behind the change, a literate walkthrough in narrative order — and a five-question quiz at the end. The rule that gives it teeth: **don't merge a load-bearing change until you pass the quiz fully.**

```
/explain-diff PR #42 — I need to actually understand the streaming logic before I merge.
```

#### `pitch` — one document that gets the work approved

Assembles your prototype, spec, implementation notes, and diff into a single demo-led buy-in doc: the working thing first, then what and why, evidence, every reviewer objection pre-answered, and the exact ask with named sign-offs.

```
/pitch Package the prototype, the spec, and the deviations log into one doc for sign-off.
```

### Transcription

Two complementary skills behind one routing rule: *captions when they exist, offline speech-to-text when they don't.* Each skill's description points at the other, so the agent picks correctly without overlap.

#### `yt-transcript` — YouTube, in seconds

Downloads the video's existing caption track (creator-uploaded preferred, auto-generated fallback) with yt-dlp, strips VTT timestamps and entities, deduplicates the rolling caption windows, and saves clean prose. No model, no transcription — captions download in seconds.

```
/yt-transcript https://youtube.com/watch?v=... — get me the transcript.
```

#### `media-transcript` — everything without captions, fully offline

X/Twitter posts, podcasts, direct media links — anything yt-dlp reaches that has no caption track. Extracts audio and transcribes locally with whisper.cpp; the audio never leaves your machine. Hardened by construction: the whisper model is SHA-256-pinned and verified before every run, URLs are treated as untrusted input, livestreams are timeout-guarded, and audio past ~20 minutes asks before committing your CPU.

```
/media-transcript https://x.com/user/status/... — transcript please.
```

### Creation & design

| Skill | What it does |
|-------|--------------|
| [`html-to-image`](./html-to-image/) | Convert HTML files to high-resolution PNG or JPEG using Puppeteer and system Chrome — no browser download required. |
| [`design-eng`](./design-eng/) | UI polish, component design, animation decisions, and the invisible details that make software feel great. |
| [`product-explainer`](./product-explainer/) | A story-driven HTML slide deck that explains your product to a non-technical audience — grounded in the real docs and codebase, no invented features. |

---

## How skills work

Skills load in three tiers, so they cost almost nothing until used:

1. **Metadata scan** (~100 tokens) — name and description, always loaded, lets the agent know the skill exists
2. **Full `SKILL.md`** — loaded only on invocation
3. **Referenced sub-files** — loaded on demand

The understanding & workflow skills publish their output as self-contained HTML — via the Claude Code Artifact tool when available, or as a local HTML file otherwise. No external dependencies either way.

---

## Repository layout

```
skills/
├── blindspot/            SKILL.md — unknown-unknowns reconnaissance
├── explain-diff/         SKILL.md — literate diff explainer + merge-gate quiz
├── pitch/                SKILL.md — demo-led buy-in document
├── yt-transcript/        SKILL.md — YouTube captions → clean prose
├── media-transcript/     SKILL.md — offline whisper.cpp transcription
├── html-to-image/        SKILL.md — HTML → PNG/JPEG rendering
├── design-eng/           SKILL.md — UI craft and polish
├── product-explainer/    SKILL.md + spec.md — layman product decks
├── .claude-plugin/       marketplace.json — plugin manifest
└── .github/              CI: validate-skills (manifest ↔ directories sync,
                          frontmatter completeness), gitleaks, actionlint,
                          PR-title lint, dependency review — all actions
                          pinned to commit SHAs
```

---

## Requirements

| Skill | Needs |
|-------|-------|
| `blindspot`, `explain-diff`, `pitch` | Nothing — dependency-free |
| `design-eng`, `product-explainer` | Nothing — dependency-free |
| `yt-transcript` | `yt-dlp`, `python3` |
| `media-transcript` | `yt-dlp`, `whisper-cpp`, `ffmpeg`, and a whisper model (~141 MB, SHA-verified on first use; the skill walks you through the download) |
| `html-to-image` | Node.js + npm, Google Chrome at `/Applications/Google Chrome.app` (macOS) |

---

## Contributing & security

- **Contributing:** skills follow a consistent structure so agents can load them reliably — see [CONTRIBUTING.md](./CONTRIBUTING.md). CI enforces it: `validate-skills` fails any PR whose skill directories and manifest drift apart.
- **Security:** report vulnerabilities privately via [SECURITY.md](./SECURITY.md). This repo's own CI runs secret scanning on every push and PR, every workflow action is pinned to a commit SHA, and `main` is protected by required status checks.

---

## Credits

The understanding & workflow skills implement patterns from [Thariq Shihipar's *"Finding Your Unknowns"*](https://thariqs.github.io/html-effectiveness/unknowns/) framework — blindspot passes, buy-in docs, and merge-gate quizzes.

## License

[MIT](./LICENSE)
