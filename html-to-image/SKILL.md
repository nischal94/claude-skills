---
name: html-to-image
description: Convert an HTML file to a high-resolution PNG or JPEG image using Puppeteer and the system Chrome installation. Use this when the user asks to render, screenshot, or export HTML to an image, or when you have just generated HTML and want to produce an image from it without using the Claude-in-Chrome MCP server.
---

# HTML-to-Image Conversion

Convert an HTML file to a high-resolution PNG or JPEG. Uses Puppeteer with the system Chrome install — no browser download required.

## When invoked

The user will call this as:
```
/html-to-image /path/to/file.html
/html-to-image /path/to/file.html --width 800
/html-to-image /path/to/file.html --format jpeg
```

Or you may invoke it internally after generating HTML — write your HTML to `$TMPDIR/<descriptive-name>.html` first, then follow this skill.

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `<file>` | required | Absolute path to the HTML file |
| `--width <px>` | `1400` | Viewport width in CSS pixels |
| `--format png\|jpeg` | `png` | Output image format |

## Steps

### 1. Parse arguments

Extract from the invocation:
- `INPUT_FILE` — the HTML file path (required)
- `WIDTH` — viewport width, default `1400`
- `FORMAT` — `png` or `jpeg`, default `png`

Derive output filename from the input filename:
- Strip directory and extension from `INPUT_FILE`
- `OUTPUT_FILE="$HOME/Downloads/<basename>.<format>"`
- Example: `/tmp/card.html` → `~/Downloads/card.png`

```bash
BASENAME=$(basename "$INPUT_FILE" .html)
OUTPUT_FILE="$HOME/Downloads/${BASENAME}.${FORMAT}"
```

### 2. Validate inputs

**Check input file exists:**
```bash
if [ ! -f "$INPUT_FILE" ]; then
  echo "[html-to-image] Input file not found: $INPUT_FILE"
  exit 1
fi
```

**Check Chrome exists:**
```bash
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -f "$CHROME_PATH" ]; then
  echo "[html-to-image] Chrome not found at: $CHROME_PATH"
  echo "Install Google Chrome or update CHROME_PATH in the script."
  exit 1
fi
```

### 3. Write the Puppeteer script

Write the following to `$TMPDIR/html-to-image.cjs` using the Write tool:

```js
const puppeteer = require('puppeteer-core');
const path = require('path');

const inputFile = process.argv[2];
const outputFile = process.argv[3];
const width = parseInt(process.argv[4]) || 1400;
const format = process.argv[5] || 'png';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height: 800, deviceScaleFactor: 2 });
  await page.goto(`file://${path.resolve(inputFile)}`, { waitUntil: 'networkidle0' });

  // Measure actual content height using last element's bottom edge.
  // getBoundingClientRect is more accurate than scrollHeight when content
  // is shorter than the initial viewport height (scrollHeight returns full viewport).
  const contentHeight = await page.evaluate(() => {
    const allElements = document.querySelectorAll('*');
    let maxBottom = document.body.getBoundingClientRect().bottom;
    allElements.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.bottom > maxBottom) maxBottom = rect.bottom;
    });
    return Math.max(Math.ceil(maxBottom), 1);
  });
  await page.setViewport({ width, height: contentHeight, deviceScaleFactor: 2 });

  const type = format === 'jpeg' ? 'jpeg' : 'png';
  const quality = type === 'jpeg' ? 95 : undefined;

  await page.screenshot({
    path: outputFile,
    fullPage: false,
    omitBackground: false,
    type,
    ...(quality !== undefined ? { quality } : {}),
  });

  await browser.close();
  console.log(`[html-to-image] Saved: ${outputFile}`);
})().catch((err) => {
  console.error(`[html-to-image] Failed: ${err.message}`);
  process.exit(1);
});
```

### 4. Install puppeteer-core if needed

Check if `puppeteer-core` is available in `$TMPDIR/node_modules`. If not, install it:

```bash
if [ ! -d "$TMPDIR/node_modules/puppeteer-core" ]; then
  echo "[html-to-image] Installing puppeteer-core..."
  npm install puppeteer-core --prefix "$TMPDIR" --loglevel=error
  if [ $? -ne 0 ]; then
    echo "[html-to-image] Install failed, retrying once..."
    npm install puppeteer-core --prefix "$TMPDIR" --loglevel=error
    if [ $? -ne 0 ]; then
      echo "[html-to-image] Failed to install puppeteer-core. Check npm and network."
      exit 1
    fi
  fi
fi
```

### 5. Run the script

```bash
SCRIPT_PATH="$TMPDIR/html-to-image.cjs"
cd "$TMPDIR" && node "$SCRIPT_PATH" "$INPUT_FILE" "$OUTPUT_FILE" "$WIDTH" "$FORMAT"
```

If exit code is non-zero, surface the exact error to the user. Do not swallow it.

### 6. Report result

Tell the user:
```
Image saved to: ~/Downloads/<filename>.<format>
```

> **Note:** If a file with the same name already exists in `~/Downloads/`, it will be silently overwritten.

### 7. Clean up

If `INPUT_FILE` was written to `$TMPDIR` by you (inline HTML case), delete it:
```bash
rm -f "$INPUT_FILE"
```

Always delete the script:
```bash
rm -f "$TMPDIR/html-to-image.cjs"
```

Do NOT delete `$TMPDIR/node_modules/puppeteer-core` — leave it cached for subsequent invocations.

## Error reference

| Error | Action |
|-------|--------|
| Input file not found | Stop, report exact path |
| Chrome not found | Stop, tell user to install Chrome |
| `puppeteer-core` install fails after retry | Surface npm error, stop |
| Script exits non-zero | Surface exact error message |
| `networkidle0` timeout (30s) | HTML loads remote resources that never settle; check for CDN/font dependencies |
