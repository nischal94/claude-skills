# Design Engineering Skill Design

**Date:** 2026-03-29
**Status:** Approved

---

## Problem

UI code is often technically correct but feels wrong — animations are too slow, easing curves are weak, hover states are missing, and transitions are janky under load. Claude's default design advice is generic. We need a skill that encodes specific, opinionated design engineering knowledge so Claude gives concrete, actionable guidance instead of vague suggestions.

---

## Interface

```
/design-eng
/design-eng [question or code snippet]
```

Invoked directly with a question, or against a code snippet for review. Claude loads the skill's philosophy, animation framework, and review checklist, then responds with specific guidance.

**Primary use cases:**
- Reviewing UI component code for animation and polish issues
- Deciding whether and how to animate a UI element
- Choosing easing curves, durations, and spring parameters
- Applying the invisible-details philosophy to component design

---

## Key Design Decisions

- **Opinionated over neutral** — the skill takes clear positions (never `ease-in`, never `scale(0)`, never animate keyboard actions) rather than presenting options
- **Before/After table format** — code reviews output a markdown table with Before/After/Why columns, not prose, so issues are scannable and actionable
- **Animation decision framework** — structured as a series of questions (should it animate? what purpose? what easing? how fast?) to prevent over-animating
- **Performance rules baked in** — `transform`/`opacity` only, GPU acceleration caveats for Framer Motion, CSS vs JS tradeoffs
- **Accessibility included** — `prefers-reduced-motion` and `hover: hover` media query patterns are part of the checklist, not an afterthought

---

## Non-Goals

- Not a general CSS reference
- Not a component library or code generator
- Not a design systems guide (tokens, spacing scales, color systems)
- Not framework-specific (React, Vue, etc.) — the principles are framework-agnostic
