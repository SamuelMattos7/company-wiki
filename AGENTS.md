# Company research wiki instructions

Use Markdown pages in `wiki/` and source documents in `raw/`. Select a profile before editing or querying. Read the `[research]` coverage and page conventions in `profiles/semiconductors.toml` by default. If the operator names another profile, read that TOML file instead. Demo entries select prepared fixtures only. Keep existing pages and paths available when adding a profile.

## Shared research rules

- **Direct** (`[direct, source: raw/path]`) means a company-issued source explicitly states the claim. Use filings, earnings releases, official transcripts or company announcements. Put the source path on every direct claim.
- **Synthesis** (`[synthesis, from: raw/one, raw/two]`) combines evidence or computes a result from it. List the supporting paths and explain the inference or calculation.
- **Assessment** (`[assessment]`) is a judgment about meaning, causality or sufficiency. Label it as judgment. Analyst notes and news may inform assessments.
- **Unverified** (`[unverified]`) identifies a claim whose support could not be confirmed. Never use it to justify an answer.
- Store evidence under `raw/` and reference each processed source from a wiki page. Leave existing paths intact. Use forward-slash repository-relative paths in markers.
- Start wiki pages with YAML frontmatter including `type` and `updated`. Index quarter pages from their company page. Use the profile for sector-specific fields and conventions.
- For material M&A, list `ma_events` on the quarter page and distinguish organic from inorganic changes. Record native reporting currency first and cite the exchange rate for any conversion.
- Preserve both versions of a restated quarter. Mark the original `status: superseded` with `superseded_by`; set `restated: true` and `restates` on the replacement. Index both.

## Operations

- **Ingest** a named source under `raw/`. Identify company and period, draft or update the relevant pages, mark claims, link evidence and update the company index. Show the diff for human review.
- **Query** from the relevant wiki pages. Cite them and preserve their evidence distinctions. State which company and period the answer covers. If the available pages cannot answer, state what evidence is missing.
- **Validate** with `python scripts/lint_markers.py` from the repository root. Review source coverage, unmarked claims, unsupported assertions, stale quarters (>100 days), financial basis, M&A, currency, broken links and contradictions separately. Read the cited documents when verifying claims.

S3 is optional. Run the sync scripts only as directed by the operator. Follow the README for credentials and review steps.
