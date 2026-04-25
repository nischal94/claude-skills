---
name: product-explainer
description: Build a story-driven HTML slide deck that explains a product to a layman / non-technical friend / non-expert stakeholder. Grounded in the product's actual docs and codebase — no invented features. Produces a master capability map, a single-protagonist narrative, and per-slide capability highlighting. Use when the user says "explain my product to a friend," "make a layman explainer," "build a deck explaining what we built," "explain this product visually," or similar. Not for pitch decks (use a pitch-deck skill) or investor decks where projections matter more than comprehension.
---

# product-explainer

Build a story-driven HTML deck that explains a product to a non-technical audience. The deck makes the entire product comprehensible in 20–30 minutes by following one protagonist through one realistic workflow, with every product capability lighting up at the moment a real person would encounter it.

## When to invoke

- "Explain my product to a friend / my mom / a non-technical stakeholder"
- "Make a layman explainer of [product]"
- "Build a deck that walks through what we built"
- "I need to show someone what this does"

## When NOT to invoke

- Pitch decks for investors (different goal — financials, traction, ask)
- Sales decks (different goal — objection handling, ROI)
- Internal team alignment (different goal — coordination, decisions)
- Documentation (different goal — reference, completeness)

## Output

A single self-contained HTML file (~25–30 slides), opened directly in the browser. Print-ready (`Cmd+P → Save as PDF`). No build step, no dependencies, just `<style>` + `<section class="slide">`.

## Core principles (do not violate)

1. **Audit before listing.** Read the product's docs and codebase before drafting any capability. Every item in the master map must trace to: a route, a component file, an AI module, a Part-N reference in the project's CLAUDE.md / spec, or a shipped checkbox. **Never invent features.**
2. **Story over taxonomy.** Follow one protagonist through one realistic week. The story is the spine; capabilities light up *inside* the protagonist's experience, not as a feature list.
3. **One camera per chapter.** A "chapter" follows one subject — one request, one person, one beat. Switching subject every slide produces the "alternate alternate" feeling that breaks comprehension.
4. **Layman language.** No jargon. Test every label: would a friend who's never used the product understand this in 2 seconds? "Pages" not "surfaces." "Receives" not "subscribed to." "Pages people actually open" not "personal navigation entities."
5. **Visible structure.** Every story slide carries a mini-map showing where in the product we are. Capability badges name what's firing right now.

## The deck's required structure

### Front matter (3–5 slides)
1. **Title** — product name, one-sentence framing, cast of named protagonists with role pills
2. **Master capability map** — every capability in the product, organized by phase/section, with cross-cutting layer below. Color-coded per major section. Big numerals for editorial weight. **This is the source of truth — every later slide must reference items in this map verbatim.**
3. **Setup chapter (1–2 slides)** — the protagonist's "before" state. The pain. Why the product exists.

### Story chapters (12–18 slides)
Each chapter follows one named subject. Each story slide includes:
- A **chapter label** (large, dark pill in top-left)
- A **mini-map** at the top showing all phases/sections, with the active one's items lit
- A **single beat** with a clear h2 and 1–2 paragraphs of body text
- A **visual demonstration** of what's happening (mock UI, decision flow, message, etc.)

Chapters typically map to the product's phase/section structure. Capabilities in the master map fire when the protagonist would encounter them.

### Bridge slides for cross-cutting concerns
When a feature category doesn't fit a phase (e.g. always-on features, principles, infrastructure), give it its own dedicated mini-chapter:
- One **intro slide** introducing all items in that category at once (color-coded, role-tagged)
- 2–3 **deep-dive slides** showing them in action

This prevents fragmentation. Without bridge slides, cross-cutting items get scattered and feel incoherent.

### Recap + close (3–4 slides)
- **The map filled in** — same master map from slide 2, every item touched during the story highlighted in green
- **The point** — a one-line takeaway as a poster-quote (dark slide, big text)
- **Coming next** *(optional)* — what's on the roadmap, grounded in real future work
- **Closing** — product name, philosophy, URL

## The procedure

### Step 1: Audit the codebase
Read in this order:
1. **Project's CLAUDE.md** (or AGENTS.md / README.md / equivalent) — especially the "what's built" section, the AI capabilities section, and any vocabulary lock.
2. **Roadmap or current-sprint doc** — for the "coming next" slide.
3. **Spec docs** — `nav-spec.md`, `onboarding-spec.md`, or equivalent. Look for vocabulary commitments and forbidden terms.
4. **Actual filesystem** — `app/`, `components/`, `lib/` (or equivalent) — what routes and modules exist tells you what's *real* versus *aspirational*.

If the codebase has no docs, ask the user for: protagonist name + role, product mission in one sentence, the product's main user-facing flow, key features. Do not invent.

### Step 2: Build the canonical capability list
For each candidate capability, classify:
- ✓ **REAL** — has a user-facing surface, exists in the codebase, would be experienced as "a thing the product does"
- ⚠ **CONCEPT/STAGE** — a phase or stage name in the data model, not a separate feature. Drop or fold into a parent capability.
- ✗ **INVENTED** — not real. Drop.
- 🔁 **RENAME** — real but using non-canonical vocabulary. Use the project's locked terms.

Aim for the actual count. Don't pad. Don't invent. If the product has 12 capabilities, the master map shows 12 — not 38.

**Test for each item:** "Would a layman understand this as a thing the product does for them?" If no, fold or drop.

### Step 3: Pick the protagonist(s) and the throughline
- One named protagonist (usually the primary user role)
- 1–2 supporting characters (other roles they collaborate with)
- One realistic workflow that touches most major capabilities — typically a single concrete task moving through the product's main phases

The protagonist must be a *named person*, not a generic "user." Memorable names matter: "Priya the designer" beats "the designer."

### Step 4: Outline the story arc
Map each capability to the story beat where it would naturally fire. Some capabilities will share a slide (multiple AI checks in one moment). Some get their own slide (the killer feature, the philosophical hinge). Some are cross-cutting — those get a bridge chapter.

**Camera-consistency check:** trace the deck slide-by-slide. Each chapter should follow one subject. If the camera bounces (request → person → abstract → person), restructure before you start writing.

### Step 5: Write the deck
- Use the structural patterns below (master map, mini-map, capability badge, role pill, etc.)
- Each story slide: chapter label, mini-map, h2 (single beat), 1–2 short paragraphs, one visual demonstration
- Keep each slide focused on one thing. If a slide needs two beats, split it.
- Use real names from the codebase for capabilities. Match the project's vocabulary lock exactly.

### Step 6: Audit before shipping
Before declaring done, verify:
- Every "lit" capability in any mini-map exists verbatim in the master map (slide 2)
- No invented features
- No banned terms (check the project's vocabulary lock)
- Camera consistency — chapters follow one subject
- The recap slide reflects what actually got demonstrated, not what was planned

## Structural patterns (HTML/CSS)

### Master capability map (slide 2)
- 4-column grid (or whatever the product's phase/section count is)
- Each column has: phase numeral (large, ghosted), phase label, phase title, phase subtitle, list of capabilities
- **Color-code per phase.** Distinct accent per phase + faint background tint. Don't make them all grey.
- Below the columns: a row of "screens people open" (personal pages, role-restricted pages) and a strip for "always-on" features.
- Include the total count: *"38 capabilities in total."* — concrete scope tells the layman this is the whole product.

### Mini-map (every story slide)
A compressed version of the master map at the top of every story slide:
- 4-column grid showing all phases/sections
- Active phase: full opacity, colored top border, faint colored background, lit items in green
- Inactive phases: 55% opacity, neutral background, items dimmed
- **Show the full canonical list in every column** — only highlight the in-use ones. Don't hide the inactive items; the layman needs to see "we're using 4 of 7 in Predesign right now."

### Capability "lit" highlighting
- In master map: green highlight pill behind the item name
- In mini-map active column: same green pill
- In mini-map inactive columns: items shown but neutral (not lit)
- In recap slide: every item touched during the story is lit in green

### Role pills
A small dark capsule next to a character's name showing their role:
```html
Priya <span class="role-tag">designer</span>
```
- Add on the **first mention per chapter** (don't repeat every line — gets noisy)
- Don't add inside structured components that already display the role (sign-off cards, briefing role headers, cast cards)
- Don't add inside quoted text or styled poster-quotes (breaks the visual)
- Use the project's canonical role vocabulary (e.g. "designer" / "PM" / "design lead")

### Cast row (slide 1)
Three to five small cards introducing the named protagonists:
- Name (bold)
- Role (small uppercase pill below)
- Restrained styling — translucent white-on-dark cards work well

### Receives banner (deep-dive slides)
When showing role-tailored output (a morning briefing, a dashboard view, etc.):
- Colored band at the top of the card matching the role's color
- "RECEIVES" label centered above
- Capability chips listed below as separate pills (not a comma-separated string)
- This makes the capability dependencies visible at a glance

### Phase color palette
Distinct color per phase. Suggested defaults:
- Phase 1 (e.g. Intake/Predesign): warm clay `#c97a3e`
- Phase 2 (e.g. Design/Build): calm blue `#5a7eb8`
- Phase 3 (e.g. Build/Ship): structured violet `#6b6a8a`
- Phase 4 (e.g. Track/Measure): green `#2d7a4f`

Match the product's existing design tokens if any (`--phase-*`, `--status-*`, etc.) — don't fight the project's design system.

### Chapter labels
Large dark pills (top-left of slide). White text, 8px tall, letter-spacing 2px, uppercase. Visible — not faint grey caption text.

## Things that always go wrong (and how to avoid them)

1. **Mini-map drift.** A capability appears lit in a mini-map but isn't in the master map. Audit before shipping; every lit item must trace to slide 2.
2. **Camera incoherence.** Slides 1–N follow a request, then suddenly switch to "everyone's pages," then back to a person. Reorganize so each chapter has one subject.
3. **Cross-cutting fragmentation.** Always-on features show up scattered across phase slides, never feeling like one coherent layer. Add a bridge intro slide before the deep-dives.
4. **Jargon creep.** "Surfaces," "entities," "primitives," "constructs" — all jargon. Replace with concrete words.
5. **Inventing features.** "Edge Case Generator" sounded plausible but didn't exist. Audit shipped checklist before writing.
6. **Visual flatness.** All-grey master map looks dull. Color-code per phase. Add big phase numerals. Lift the title.
7. **Role implication errors.** "Designer view: My Requests" implies designers don't see Inbox. Be precise: "everyone sees the same items, role only changes ordering."
8. **Receipt direction missing.** When showing always-on features, name *who receives what*. "Lane sends a digest" → "Lane sends the digest **to Anika · design lead only.**"
9. **Cached browser tab.** When iterating, browsers cache local HTML aggressively. Use `?v=$(date +%s)` cache-buster when reopening: `open "file://...?v=$(date +%s)"`.

## Iteration discipline

The user will request changes. Common ones:
- "Make X pop more" → bigger, more contrast, colored band, not italic muted text
- "Show full list everywhere" → mini-maps must show all canonical items, not just the lit ones
- "Why does the order feel off?" → check camera consistency, look for cross-cutting fragmentation
- "Add who-gets-what" → add receive banners showing recipient roles explicitly

Don't argue. Test the request against the principles above. If it improves comprehension for a layman, do it. If it breaks a principle (e.g. user asks to add an invented feature), push back with the principle.

## A note on length

A good layman explainer is 20–30 slides. Less than 15 leaves capabilities undemonstrated. More than 35 loses the layman. If the product has too many capabilities to demonstrate individually, group them: multiple AI features can fire on one slide if they fire at the same narrative moment.

## A note on humor and tone

Restrained warmth beats clever. The protagonist should feel real, not whimsical. The product should feel solid, not cheeky. Don't use emojis in slide content. Don't make pop-culture references. Aim for the feel of a thoughtful colleague walking a friend through their work, not a marketing pitch.
