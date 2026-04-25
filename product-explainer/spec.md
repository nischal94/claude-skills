# product-explainer — design spec

## Goal

Make a complete software product comprehensible to a non-technical person — a friend, a parent, a stakeholder outside engineering — in a single 20–30 minute viewing of an HTML slide deck.

The deck succeeds when the viewer can, unprompted, describe what the product does, who it's for, and why it matters.

## Non-goals

- **Pitch decks for investors.** Different success criteria — financials, traction, market size, ask. Use a pitch-deck skill.
- **Sales decks.** Different success criteria — objection handling, ROI, competitive positioning.
- **Internal team alignment.** Different success criteria — coordination, decisions, ownership.
- **Reference documentation.** Different success criteria — completeness, searchability, accuracy at the API level.

A layman explainer is none of these. Conflating them produces a deck that fails at all four jobs.

## Core constraints

1. **Audit before listing.** Every capability mentioned must trace to a real artifact in the codebase: a route, a component file, an AI module, a Part-N reference in CLAUDE.md or the spec, or a shipped checkbox. No invented features. No aspirational features. No "we plan to."

2. **Single protagonist, single workflow.** The deck follows one realistic person through one realistic task. Comprehension collapses when the audience has to track multiple personas or branching flows.

3. **Capabilities light up at the moment of encounter.** Each slide highlights the specific capability the protagonist uses on that slide — not a feature list dumped on slide 3. The audience learns the product by watching it get used.

4. **Master capability map exists before slides do.** Before drafting any slide, produce the full inventory of capabilities. The narrative then chooses which capabilities to illuminate and in what order. Without the map, slides drift toward whatever was easiest to write.

## Output shape

- **Single self-contained HTML file.** No build step, no bundler, no external assets that can break.
- **~25–30 slides.** Fewer feels thin; more loses the audience.
- **`<style>` + `<section class="slide">`.** Plain semantic HTML. No framework dependency.
- **Print-ready.** `Cmd+P → Save as PDF` produces a usable artifact for sharing.
- **Opened directly in the browser.** No server required.

## Why HTML and not [other format]

- **Not Keynote/PowerPoint** — binary format, version-locked, can't be regenerated from source, hard to diff in git.
- **Not Markdown + reveal.js** — adds a dependency and a build step; one more thing that can break in 6 months.
- **Not Google Slides** — requires login, lives outside the project repo, can't be version-controlled with the code.
- **HTML wins** because the deck lives next to the code it describes, regenerates deterministically, diffs cleanly, and prints to PDF without extra tooling.

## What can go wrong (and how the constraints prevent it)

| Failure mode | Constraint that prevents it |
|---|---|
| Deck describes features that don't exist | Audit-before-listing |
| Audience loses the thread halfway through | Single protagonist |
| Feels like a marketing brochure, not a tour | Capabilities light up at moment of encounter |
| Author cherry-picks favorite features, skips the rest | Master capability map written first |
| Deck rots when the product changes | Plain HTML, traceable to source artifacts, regeneratable |

## When to revisit this spec

- The skill is being used for a non-layman audience (re-evaluate goal).
- The single-protagonist rule is breaking on a genuinely multi-sided product (e.g. a marketplace).
- HTML output is becoming a constraint instead of an enabler (e.g. user always wants Keynote).
