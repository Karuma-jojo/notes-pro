#!/usr/bin/env python3
from pathlib import Path
import json, re, yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "index.json"
FRONT = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)

records = []
for p in DOCS.rglob("*.md"):
    if p.name.startswith("_index"):
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    m = FRONT.match(text)
    fm = yaml.safe_load(m.group(1)) if m else {}
    rec = {
        "title": fm.get("title") or p.stem.replace("-", " ").title(),
        "tags": fm.get("tags", []),
        "tldr": fm.get("tldr", ""),
        "path": str(p.relative_to(DOCS)),
    }
    records.append(rec)

OUT.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT} ({len(records)} records)")
