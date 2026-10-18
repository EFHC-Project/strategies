# EFHC Strategies — on-chain market research

Read-only, reproducible research repository for EFHC market dynamics, TON/ST​ON.fi liquidity pools and RBTC correlations. No private keys or trading execution.

## Current state (2026-10-18)
**Start here:** [Active research state](docs/ACTIVE_RESEARCH_STATE_2026-10-18.md). It contains the latest evidence, owner observations, causal hypotheses, strategy and open tasks.

**Primary evidence:** `archive/dyor/2026-10-18/manifest.json` with `EFHC.jsonl.gz` (135 records, API feed exhausted) and `RBTC.jsonl.gz` (20,000 records, explicit cap). These are DYOR indexed *token* transactions, not all necessarily belonging to target EFHC pools.

**Baseline analysis:** `reports/dyor/analysis.md`, `reports/dyor/analysis.json`; GitHub Actions run 39147398659. Earlier partial TON account history: `archive/ton-history/2026-10-18-run-39142840992/`. Architecture and strict evidence standards: `docs/RESEARCH_ARCHITECTURE_v001.md`.

## Monitored TON pools
- USDT/EFHC: `EQB2iz4-oG50xuXjbRYc-h-TR-Siow7ynH0XGNsor_lgg8D2`
- GRAM/EFHC: `EQDMCqRzSnMtKjltr6jf4Fqah1o14Gdyq6sU5-XsNGkuIY9F`
- RBTC/EFHC: `EQAlrp2dgYMHbtp1X0_KujyZvpTHkjjEvic4kBa1FlNRZa8s`

## Research workflow
`tools/dyor/archive_transactions.py`: bounded collection, maximum 20,000 records per token. `tools/dyor/analyze_transactions.py`: reproducible baseline analysis. GitHub Actions workflows archive and analyze data and store reports. DYOR is secondary indexer evidence; TON canonical traces and pool state remain necessary to validate economic claims.

**Interpretation:** Counts of buys and sells do not measure net volume or prove price pressure. Address overlap and temporal correlation do not prove coordinated actors. The repository documents hypotheses and unresolved checks rather than asserting manipulation.
