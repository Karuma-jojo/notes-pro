#!/usr/bin/env python3
from pathlib import Path
import re, yaml, sys, unicodedata

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
FRONT_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)

def slugify(value):
    value = str(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)

def main():
    for p in DOCS.rglob("*.md"):
        if p.name.startswith("_index"):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        m = FRONT_RE.match(text)
        fm = yaml.safe_load(m.group(1)) if m else {}
        title = fm.get("title") or p.stem
        tags = [t.lower() for t in fm.get("tags", [])]
        top = "inbox"
        for cand in ["ctf","math","ai","kaggle","swe","notes"]:
            if cand in tags:
                top = cand; break
        sub = None
        if top == "ctf":
            for c in ["web","crypto","pwn","reversing","forensics","osint","stego"]:
                if c in tags:
                    sub = c; break
        dest_dir = DOCS / top / (sub if sub else "")
        dest_dir.mkdir(parents=True, exist_ok=True)
        new_name = slugify(title) + ".md"
        dest = dest_dir / new_name
        if dest.resolve() == p.resolve():
            continue
        dest.write_text(text, encoding="utf-8")
        p.unlink()
        print(f"Moved {p} -> {dest}")

if __name__ == "__main__":
    main()
