#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) < 2:
    print("Usage: split_inbox.py <raw.txt> [delimiter]")
    sys.exit(1)

raw = Path(sys.argv[1])
delimiter = sys.argv[2] if len(sys.argv) > 2 else "---"

docs = Path(__file__).resolve().parent.parent / "docs" / "inbox"
docs.mkdir(parents=True, exist_ok=True)

chunk, n = [], 0
with raw.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if line.strip() == delimiter:
            if chunk:
                n += 1
                (docs / f"dump-{n:04d}.md").write_text("".join(chunk), encoding="utf-8")
                chunk = []
        else:
            chunk.append(line)
if chunk:
    n += 1
    (docs / f"dump-{n:04d}.md").write_text("".join(chunk), encoding="utf-8")

print(f"Wrote {n} note(s) to {docs}")
