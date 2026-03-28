# HTML-to-Image Skill Design

**Date:** 2026-03-28
**Status:** Approved

---

## Problem

The Claude-in-Chrome MCP server works for HTML-to-image conversion but exhausts tokens at scale. We need a leaner, lower-token path that produces high-resolution, well-cropped images that faithfully render the HTML layout.

---

## Interface

```
/html-to-image /path/to/file.html
/html-to-image /path/to/file.html --width 800
/html-to-image /path/to/file.html --format jpeg
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `<file>` | required | Path to HTML file on disk |
| `--width <px>` | `1400` | Viewport width in CSS pixels |
| `--format png\|jpeg` | `png` | Output image format |

**Output:** `~/Downloads/<html-filename>.png` (or `.jpg`)

---

## Key Design Decisions

- **`puppeteer-core` not `puppeteer`** — reuses system Chrome, no 150MB browser download
- **`networkidle0`** — waits for fonts, images, and CSS to fully load before screenshotting
- **`deviceScaleFactor: 2`** — retina quality (2800px effective pixel width at 1400px layout width)
- **`getBoundingClientRect` for height** — more accurate than `scrollHeight` when content is shorter than initial viewport
- **`--prefix "$TMPDIR"`** for npm install — avoids `cd` issues if install fails mid-flight
- **JPEG quality 95** — visually lossless for card/UI renders

---

## Error Handling

| Failure | Behavior |
|---------|----------|
| Input file not found | Stop, report exact path |
| Chrome not found | Stop, tell user to install Chrome |
| `puppeteer-core` install fails after retry | Surface exact npm error, stop |
| Script exits non-zero | Surface exact error message |
| `networkidle0` timeout | Surface timeout, note CDN/font dependencies as likely cause |

---

## Non-Goals

- No PDF output
- No remote URL support (file:// only)
- No multi-page / scroll capture
- No Windows/Linux Chrome path support (macOS only)
