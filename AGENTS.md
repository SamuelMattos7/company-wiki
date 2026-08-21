# AGENTS.md — Semiconductor Company Research Wiki

## Purpose

Track semiconductor companies across financials (quarterly/annual) and product/roadmap developments. Answers questions that connect a financial fact to a product fact across time — something no single source document does on its own.

## Layout

```
raw/{filings,transcripts,announcements,analyst-notes}/   — source documents
wiki/{companies,quarters,products,themes,index.md}        — wiki pages
scripts/{lint_markers.py,sync-up.sh,sync-down.sh}        — tooling
terraform/                                                — S3 infra (bucket, IAM user, access keys)
```

No package.json, requirements.txt, Makefile, or test framework. The repo is markdown files + shell scripts + terraform.

## Tooling & commands

| Action | Command |
|---|---|
| Validate epistemic markers | `python3 scripts/lint_markers.py` (run from repo root) |
| Sync local → S3 | `bash scripts/sync-up.sh` (requires `.env`) |
| Sync S3 → local | `bash scripts/sync-down.sh` (requires `.env`) |
| Terraform apply | `terraform -chdir=terraform apply` |

**`.env` defines the S3 bucket and AWS profile** — not in `.gitignore` (be careful not to commit secrets).

## Page frontmatter

Every wiki page starts with YAML frontmatter:

**`company`** — `type: company`, `ticker`, `sector: semicap|fabless|idm|foundry`, `status: active|watchlist|inactive`, `updated`, optionally `fiscal_offset`, `reporting_currency`
**`quarter`** — `type: quarter`, `company`, `fiscal_period: Q2-2026`, `period_end`, `source: raw/...`, `reporting_currency`, `updated`, `confidence: direct`, `restated`, optionally `ma_events`, `superseded_by`
**`product`** — `type: product`, `company`, `category: gpu|cpu|asic|memory|foundry-process|other`, `status: announced|shipping|eol`, `first_mentioned`, `updated`
**`theme`** — `type: theme`, `updated`, `related_companies`

Use **calendar-quarter labels** in filenames/frontmatter regardless of source doc labels (e.g. `2026-q2`). Note fiscal offset on the `company` page if different.

## GAAP vs. non-GAAP

Every headline financial figure on a `quarter` page must specify which basis:

```
Gross margin (non-GAAP): 75.1% [direct, source: ...]
Gross margin (GAAP): 72.8% [direct, source: ...]
```

If the source only provides one basis, state that explicitly. Default for cross-page comparisons: non-GAAP.

## Epistemic markers — mandatory on every claim

Three kinds of statements — every substantive claim must be tagged:

- **`[direct, source: <path>]`** — stated explicitly in a source doc
- **`[synthesis, from: <path-or-pathlist>]`** — derived by combining direct facts
- **`[assessment]`** — interpretive/causal judgment, never phrased as fact
- **`[unverified]`** — when the source can't be confirmed

No number appears without a source reference. `[assessment]` is the most commonly omitted tag — enforce it.

Run `python3 scripts/lint_markers.py` for deterministic marker validation. The script enforces exact lowercase syntax (`[direct, source: ...]`, not `[Direct - source: ...]`).

## Sourcing

- Only company-issued docs (10-K, 10-Q, 8-K, earnings releases, official transcripts, roadmap materials) for `[direct]` claims.
- Analyst notes / news articles are `[assessment]` sources only.
- Every `raw/` file must be referenced by at least one wiki page — orphaned files signal incomplete processing.

## M&A, currency, restatements

- **M&A**: `quarter` page after a material event must list `ma_events` in frontmatter. Never compute a `[synthesis]` QoQ/YoY comparison across an M&A boundary without flagging organic vs. inorganic.
- **Currency**: Record in native reporting currency first (`[direct]`). USD conversions are `[synthesis]` with exchange rate noted. `company` pages for foreign filers set `reporting_currency` once.
- **Restatements**: Never overwrite. Original gets `status: superseded` + `superseded_by`. New page gets `restated: true` + `restates`. Both appear on the company page's quarter index.

## Coverage universe

| Category | Companies |
|---|---|
| Semicap | ASML, AMAT, LRCX, TOELY, KLAC, ASMIY, DINRF |
| Fabless | NVDA, AVGO, AMD, QCOM, MRVL, MPWR; watchlist: LSCC, ALAB, Cerebras |
| IDM | INTC (Intel Foundry as separate sub-entity), MU, Samsung, SK Hynix, TXN, ADI, ON; watchlist: NXP, Infineon, STM |
| Foundry | TSM, GFS, UMC, SMIC, TSEM |

Anything outside this list gets `status: watchlist`.

## Operations

**`ingest`**: Identify raw file type/company/period → create/update `quarter` and/or `product` pages → tag every claim → link related pages → update parent `company` page's quarter index.

**`query`**: Answer from wiki pages (not raw sources). Cite page(s). Preserve epistemic markers. Note which quarters/companies had available data.

**`lint`**: Run `scripts/lint_markers.py` first (deterministic), then check: orphaned raw sources, missing markers, GAAP/non-GAAP ambiguity, unflagged M&A comparisons, currency conversions missing native figure, stale quarters (>100 days), cross-quarter contradictions, broken `[[wiki-links]]`, assessment drift.

## S3 sync workflow

Both `raw/` and `wiki/` are synced to S3 bucket `research-llm-wiki` under AWS profile `llm-wiki-agent` (from `.env`). Always sync **down** before editing (to get latest), then sync **up** when done:

```
bash scripts/sync-down.sh   # start of session
bash scripts/sync-up.sh     # after changes
```
