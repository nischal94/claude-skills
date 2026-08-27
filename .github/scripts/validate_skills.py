#!/usr/bin/env python3
"""Validate skill directories against the marketplace manifest.

Fails when: the manifest lists a skill with no SKILL.md, a skill
directory is missing from the manifest, or a SKILL.md lacks the
frontmatter fields the plugin loader needs (name, description).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"

errors = []

manifest = json.loads(MANIFEST.read_text())
listed = {s for p in manifest["plugins"] for s in p["skills"]}

on_disk = {
    d.name
    for d in ROOT.iterdir()
    if d.is_dir() and not d.name.startswith(".") and (d / "SKILL.md").is_file()
}

for name in sorted(listed - on_disk):
    errors.append(f"manifest lists '{name}' but {name}/SKILL.md does not exist")
for name in sorted(on_disk - listed):
    errors.append(f"'{name}/SKILL.md' exists but is not listed in marketplace.json")

for name in sorted(on_disk & listed):
    text = (ROOT / name / "SKILL.md").read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        errors.append(f"{name}/SKILL.md: no YAML frontmatter block")
        continue
    fm = m.group(1)
    for field in ("name", "description"):
        if not re.search(rf"^{field}:", fm, re.MULTILINE):
            errors.append(f"{name}/SKILL.md: frontmatter missing '{field}:'")
    fm_name = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
    if fm_name and fm_name.group(1) != name:
        errors.append(
            f"{name}/SKILL.md: frontmatter name '{fm_name.group(1)}' "
            f"does not match directory name"
        )

if errors:
    print("Skill validation failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"OK: {len(on_disk)} skills, manifest in sync, frontmatter complete")
