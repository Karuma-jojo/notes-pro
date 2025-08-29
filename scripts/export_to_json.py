#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
try:
    import yaml
except ImportError:
    print("Please install PyYAML: pip install PyYAML", file=sys.stderr); raise

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "dataset" / "notes.ndjson"

FRONT_MATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)
CODE_BLOCK_RE = re.compile(r'```(\w+)?\n(.*?)\n```', re.DOTALL)

def parse_front_matter(text):
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
    return fm, body

def extract_sections(md):
    sections = []
    current = {"heading": "ROOT", "text": []}
    for line in md.splitlines():
        if line.startswith("#"):
            if current["text"]:
                sections.append({"heading": current["heading"], "text": "\n".join(current["text"]).strip()})
            current = {"heading": line.lstrip("#").strip(), "text": []}
        else:
            current["text"].append(line)
    if current["text"]:
        sections.append({"heading": current["heading"], "text": "\n".join(current["text"]).strip()})
    return sections

def extract_code_blocks(md):
    blocks = []
    for m in CODE_BLOCK_RE.finditer(md):
        lang = (m.group(1) or "").strip()
        code = m.group(2)
        blocks.append({"lang": lang, "code": code})
    return blocks

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with OUT.open("w", encoding="utf-8") as f:
        for p in DOCS.rglob("*.md"):
            if p.name.startswith("_index"):
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            fm, body = parse_front_matter(text)
            sections = extract_sections(body)
            code_blocks = extract_code_blocks(body)
            rec = {
                "path": str(p.relative_to(ROOT)),
                "title": fm.get("title") or p.stem.replace("-", " ").title(),
                "tags": fm.get("tags", []),
                "tldr": fm.get("tldr", ""),
                "platform": fm.get("platform", ""),
                "phase": fm.get("phase", ""),
                "refs": fm.get("refs", []),
                "sections": sections,
                "code_blocks": code_blocks,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            count += 1
    print(f"Wrote {OUT} with {count} records")

if __name__ == "__main__":
    main()
