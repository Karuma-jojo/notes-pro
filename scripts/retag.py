#!/usr/bin/env python3
from pathlib import Path
import sys, re, yaml

if len(sys.argv) < 4:
    print("Usage: retag.py <glob> add <tag1,tag2,...>  | retag.py <glob> replace <tag1,tag2,...>")
    sys.exit(1)

glob, mode, tags_csv = sys.argv[1], sys.argv[2], sys.argv[3]
new_tags = [t.strip() for t in tags_csv.split(",") if t.strip()]

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
FRONT_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)

changed = 0
for p in DOCS.rglob("*.md"):
    if not p.match(str(DOCS / glob)):
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    m = FRONT_RE.match(text)
    if not m:
        fm = {"tags": new_tags}
        body = text
    else:
        fm = yaml.safe_load(m.group(1)) or {}
        body = text[m.end():]
        if mode == "replace":
            fm["tags"] = new_tags
        elif mode == "add":
            fm["tags"] = sorted(set(fm.get("tags", []) + new_tags))
        else:
            print("Mode must be add|replace"); sys.exit(1)
    front = yaml.safe_dump(fm, sort_keys=False).strip()
    p.write_text(f"---\n{front}\n---\n{body}", encoding="utf-8")
    changed += 1

print(f"Retagged {changed} file(s)")
