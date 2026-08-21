# company-wiki

A lean, solo-operator framework for building a trusted, version-controlled **semiconductor company research wiki** from raw source documents, using opencode as an agentic layer and AWS S3 as the single source of truth.

## What this is

This repo tracks semiconductor companies across two dimensions that most sources treat separately:

- **Financials** — quarterly and annual results (10-Qs, earnings releases)
- **Products & roadmaps** — architectures, shipping status, export-control impacts

The goal is to answer questions that connect a financial fact to a product fact across time — something no single source document does on its own.

Every substantive claim on a wiki page carries an **epistemic marker** (`[direct, source: ...]`, `[synthesis, from: ...]`, `[assessment]`, `[unverified]`) so you always know whether a statement came from a filing or was inferred. See [AGENTS.md](AGENTS.md) for the full conventions.

## Layout

```
raw/
  filings/          10-Qs and other SEC filings (PDF)
  transcripts/      earnings call transcripts
  announcements/    press releases, roadmap materials
wiki/
  companies/        one page per company (fiscal calendar, quarter index)
  quarters/         one page per calendar quarter per company
  products/         one page per product/architecture
  themes/           cross-company topics
scripts/
  lint_markers.py   validates epistemic-marker syntax across wiki/
  sync-up.sh        push local -> S3
  sync-down.sh      pull S3 -> local
terraform/          S3 bucket + IAM user + access keys
```

## Usage

The wiki is maintained through three agent operations (defined in AGENTS.md):

| Operation | What it does |
|---|---|
| `ingest` | Process a raw document into `quarter` / `product` pages, tag every claim, update the company page |
| `query` | Answer questions from wiki pages (not raw sources), citing pages and preserving markers |
| `lint` | Run deterministic checks: marker syntax, orphaned raw files, GAAP/non-GAAP ambiguity, stale quarters, broken links |

### Commands

```bash
python3 scripts/lint_markers.py   # validate epistemic markers (run from repo root)
bash scripts/sync-down.sh         # start of session — get latest from S3 (requires .env)
bash scripts/sync-up.sh           # after changes — push to S3 (requires .env)
terraform -chdir=terraform apply  # provision S3 infra
```

`.env` defines the S3 bucket (`research-llm-wiki`) and AWS profile (`llm-wiki-agent`). It is intentionally **not** gitignored — be careful not to commit secrets.

## Conventions worth knowing

- Wiki filenames use **calendar-quarter labels** (`2025-q1`), regardless of the fiscal labels in source documents; fiscal offsets are recorded on each company page.
- Headline financial figures always state their basis (GAAP vs non-GAAP). Filings are GAAP-only.
- Restatements never overwrite: the original page is marked superseded and both versions stay indexed.
- Coverage universe and page schemas are defined in [AGENTS.md](AGENTS.md).
