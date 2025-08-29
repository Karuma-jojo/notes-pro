# My Knowledge Base (Pro scaffold)

Low-cost, **searchable** knowledge system with:
- Markdown + tags
- MkDocs Material site (GitHub Pages-ready)
- Bulk tools: retag, slugify/move, inbox splitter
- Exporter to **NDJSON** for ML/training
- Optional Fuse.js index (small JSON) if you want custom on-page filtering later

## Quick start

```bash
pip install PyYAML mkdocs-material
mkdocs serve    # local preview with search
python scripts/export_to_json.py   # create dataset/notes.ndjson
```

## Bulk operations

- **Dump raw text** → `docs/inbox/`, then split:
```bash
python scripts/split_inbox.py raw_dump.txt '---'
```
- **Bulk retag** matching a glob:
```bash
python scripts/retag.py 'ctf/**/*.md' add ctf,linux,privesc
python scripts/retag.py 'docs/**/*.md' replace base,notes
```
- **Auto move + slugify** based on tags:
```bash
python scripts/slugify_and_move.py
```
- **Small JSON index** (optional for custom Fuse.js UI):
```bash
python scripts/build_fuse_index.py
```

## GitHub Pages deploy (Actions)

Push to GitHub and enable Pages. This repo includes a workflow in `.github/workflows/gh-pages.yml` that builds and deploys on every push to `main`.

## Where to store heavy files

- Use **GitHub Releases** for up to 2 GiB per asset; link to them from notes.
- Or use S3/B2/R2 + CDN for very large datasets.

## Safety

Keep it legal; remove sensitive data; credit sources.
