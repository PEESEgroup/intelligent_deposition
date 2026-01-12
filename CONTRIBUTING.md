# Contributing

PRs are welcome for maintaining paper entries and taxonomy labels.

## Recommended workflow
1. Add or correct entries in `data/papers.yaml` (e.g., DOI, link, brief notes).
2. Add or adjust categories in `data/taxonomy.yaml` (keep scope stable and definitions clear).
3. Generate docs with the build script:
   ```bash
   python scripts/build_catalog.py
   ```
4. Commit your changes.

## Conventions
- Only include papers relevant to this review topic (oCVD / CVD polymer deposition + AI for MbD).
- Prefer existing tags; if a new category is needed, describe its scope and examples in the taxonomy.
