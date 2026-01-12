#!/usr/bin/env python3
"""
Build README.md from data/papers.yaml + data/taxonomy.yaml.

Usage:
  python scripts/build_catalog.py
"""
from __future__ import annotations
import os
from collections import defaultdict
import yaml

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")

def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _clean_period(s: str) -> str:
    s = (s or "").strip()
    while s.endswith("."):
        s = s[:-1].rstrip()
    return s

def readme_bullet(e: dict) -> str:
    title = _clean_period(e.get("title") or f"Ref {e['id']}")
    year = e.get("year")
    venue = _clean_period(e.get("venue") or "")
    doi = e.get("doi")
    url = e.get("url")

    meta_parts = []
    if year:
        meta_parts.append(str(year))
    if venue:
        meta_parts.append(venue)
    meta_str = ", ".join(meta_parts)
    if meta_str:
        meta_str = f", {meta_str}."

    link = None
    if doi:
        doi_clean = str(doi).rstrip(".")
        link = f"https://doi.org/{doi_clean}"
    elif url:
        link = url
    link_str = f" [[📄 Paper]({link})]" if link else ""

    return f"- **{title}**{meta_str}{link_str}".rstrip()

def main():
    papers = load_yaml(os.path.join(DATA_DIR, "papers.yaml"))
    taxonomy = load_yaml(os.path.join(DATA_DIR, "taxonomy.yaml"))

    tag_to_papers=defaultdict(list)
    untagged=[]
    for e in papers:
        tags = e.get("tags", [])
        if not tags:
            untagged.append(e)
        for t in tags:
            tag_to_papers[t].append(e)
    def _sort_key(e: dict):
        year = e.get("year")
        try:
            year_val = int(year)
        except (TypeError, ValueError):
            year_val = 0
        return (-year_val, e["id"])

    for t in tag_to_papers:
        tag_to_papers[t].sort(key=_sort_key)

    # docs generation removed; README is the single source of truth

    # README
    readme = []
    readme.append("# Awesome-Intelligent-Deposition-Papers\n")
    readme.append(
        "This repository contains the list of representative works in the survey "
        "\"*Intelligent Deposition: Artificial Intelligence in Organic Chemical Vapor Deposition for "
        "Emerging Materials Technologies*\", along with relevant reference materials.\n"
    )
    for tag, meta in taxonomy.items():
        desc = (meta.get("desc") or "").strip()
        readme.append(f"## {meta['name']}\n")
        if desc:
            readme.append(f"> {desc}\n")
        plist = tag_to_papers.get(tag, [])
        if plist:
            readme.append("\n".join(readme_bullet(e) for e in plist))
        readme.append("")
    if untagged:
        untagged.sort(key=_sort_key)
        readme.append("## Uncategorized\n")
        readme.append("\n".join(readme_bullet(e) for e in untagged))
        readme.append("")
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(readme))

if __name__ == "__main__":
    main()
