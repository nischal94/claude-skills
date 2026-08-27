---
name: yt-transcript
version: 0.1.0
description: |
  Fetch and clean YouTube video transcripts. Pulls captions (creator-uploaded or
  auto-generated) via yt-dlp, strips timestamps and HTML entities, deduplicates
  rolling caption lines, and saves clean prose. Optionally summarizes the video.
  Use when asked to "transcribe this YouTube video", "get the transcript",
  "summarize this video", or when given a youtube.com / youtu.be URL.
triggers:
  - youtube transcript
  - youtube transcribe
  - get transcript
  - transcribe video
  - summarize youtube
  - summarize this video
allowed-tools:
  - Bash
  - Read
  - Write
---

# yt-transcript

Fetch a YouTube video's transcript, clean it to plain prose, and save it. Optionally summarize.

## When to use

Invoke this skill when the user:
- Pastes a `youtube.com/watch?v=...` or `youtu.be/...` URL and wants the contents
- Asks to "transcribe", "get the transcript", or "summarize" a YouTube video
- Wants to feed video content into another skill (e.g. /learn, /qa)

## Prerequisites — verify before running

```bash
which yt-dlp || echo "MISSING: install with 'brew install yt-dlp'"
```

If missing, stop and tell the user to install it. Do NOT silently substitute another tool.

## The pipeline

### 1. Pull captions

**IMPORTANT**: The network call requires `dangerouslyDisableSandbox: true` in
Claude Code because:
- yt-dlp's Python (Homebrew python@3.14) needs to read its certifi cert bundle
  from `/opt/homebrew/lib/python3.14/site-packages/certifi/cacert.pem`
- The default sandbox blocks reads inside `/opt/homebrew/lib/`, causing
  `SSL: CERTIFICATE_VERIFY_FAILED` errors on the YouTube API call
- Outside Claude Code (user's terminal), no flag needed — sandbox only exists here

Run from a clean output directory:

```bash
OUT=~/Downloads/yt-transcript
mkdir -p "$OUT" && cd "$OUT"
yt-dlp --write-auto-subs --write-subs \
       --skip-download \
       --sub-lang en \
       --sub-format vtt \
       "<URL>"
```

Flags explained:
- `--write-subs`: prefer creator-uploaded captions (more accurate)
- `--write-auto-subs`: fall back to YouTube's auto-generated captions
- `--skip-download`: don't pull the video file, only captions
- `--sub-lang en`: English (change for other languages)
- `--sub-format vtt`: WebVTT format (timestamped text)

Output is `<video-title> [<video-id>].en.vtt` in `$OUT`.

### 2. Clean VTT to prose

The raw VTT is bloated because YouTube auto-captions repeat each phrase across
multiple time-windows for smooth on-screen display. Deduplicate by line.

```python
import re, pathlib, sys

vtt_path = pathlib.Path(sys.argv[1])
lines = vtt_path.read_text().splitlines()
out, seen = [], set()
for ln in lines:
    if not ln.strip(): continue
    if ln.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")): continue
    if "-->" in ln: continue
    if re.match(r"^\d+$", ln): continue
    clean = re.sub(r"<[^>]+>", "", ln).strip()
    clean = clean.replace("&gt;&gt;", ">>").replace("&amp;", "&").replace("&quot;", '"')
    if not clean: continue
    if clean in seen: continue
    seen.add(clean)
    out.append(clean)
text = " ".join(out)
output = vtt_path.with_suffix("").with_suffix(".txt")
output.write_text(text)
print(f"Saved: {output}")
print(f"Words: {len(text.split())}")
```

Notes on the cleanup:
- HTML-encoded entities like `&gt;&gt;` are YouTube's speaker-turn markers; preserved as `>>` so speaker boundaries remain visible.
- `<...>` inline tags (timing hints) are stripped.
- Line-level dedup (not phrase-level) — preserves natural sentence flow while eliminating the rolling-window duplicates.

### 3. (Optional) Summarize

If user asked for a summary, read the cleaned `.txt` and produce:
- A 3-sentence TL;DR
- 5-7 key insights as bullet points
- Notable quotes (if any)
- Speakers/topics covered

Don't auto-summarize unless asked — transcripts can be long, and user may want raw text for their own use.

## Error handling

| Error | Cause | Fix |
|---|---|---|
| `SSL: CERTIFICATE_VERIFY_FAILED` | Sandbox blocking cert read | Set `dangerouslyDisableSandbox: true` |
| `Subtitle format not found` | Video has no English captions | Try `--sub-lang <other>` or fall back to audio + Whisper |
| `Video unavailable` | Private, region-blocked, or removed | Tell the user; no workaround |
| `Operation not permitted` (Cellar) | Homebrew permissions broken | `sudo chown -R $USER /opt/homebrew/Cellar` (user runs this) |

## What this skill does NOT do

- Translate transcripts to other languages (use a separate translation step)
- Transcribe videos with no captions (would need yt-dlp audio download + Whisper — different pipeline)
- Process entire playlists in one shot (loop over URLs manually for now)
- Strip filler words ("um", "you know") — leaves transcript faithful to source

## Anti-scope

Do NOT extend this skill to:
- Download the video itself (use `yt-dlp` directly)
- Generate video summaries with embedded timestamps (separate workflow)
- Post-process transcripts into chapters or sections (separate workflow)

Keep this skill focused on: URL in → clean transcript out.
