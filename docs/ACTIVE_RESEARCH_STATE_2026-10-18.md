# EFHC Strategies — Active State and Causal Research Register
Date: 2026-10-18
Status: EVIDENCE BASELINE / ANALYSIS PARTIAL

## Owner mandate
Track EFHC price pressure and RBTC activity; investigate causes, effects, liquidity, market structure, and potential cross-pool relationships without presuming manipulation. Research only: no automated trading or wallet operations.

## Source-of-truth order
1. Raw immutable TON transaction BOC, traces, contract states and verified pool identity (canonical chain evidence).
2. DYOR indexed transaction records with retrieval provenance (secondary market observations).
3. Deterministic normalized events and calculations (derived evidence).
4. Hypotheses, scenarios and strategy (explicitly non-observational).

## Data inventory
- DYOR archive: `archive/dyor/2026-10-18/`. EFHC: 135 unique records, 2 API pages, feed exhausted; 2025-05-06 through 2026-10-18. RBTC: 20,000 records, 201 API pages, limit reached; 2024-11-29 through 2026-10-18; NOT complete history.
- DYOR report: `reports/dyor/analysis.json`, `analysis.md`. EFHC: 59 TT_BUY, 52 TT_SELL, 23 TT_LIQUIDITY_DEPOSIT, 1 TT_LIQUIDITY_WITHDRAW, 3 raw pool IDs. RBTC: 5,125 TT_BUY, 14,829 TT_SELL, 28 TT_LIQUIDITY_DEPOSIT, 18 TT_LIQUIDITY_WITHDRAW, 14 raw pool IDs.
- 9 overlapping transaction hashes between EFHC and RBTC indexed datasets; requires independent event-level inspection.
- Prior TON lite-server collector: 13 USDT/EFHC, 39 GRAM/EFHC, 44 RBTC/EFHC account records; first two incomplete, last marked complete by provisional chain termination; not decoded economic events. See `docs/RESEARCH_ARCHITECTURE_v001.md`.
- Provenance: GitHub Actions DYOR archive run 39146079784; DYOR analysis run 39147398659. All SHA-256 file digests in archive manifest.
- All 20,135 DYOR records are *token-feed* entries, not necessarily transactions involving the three target pools. RBTC overall sell count is NOT an EFHC selling metric.

## Target markets
- USDT/EFHC: EQB2iz4-oG50xuXjbRYc-h-TR-Siow7ynH0XGNsor_lgg8D2
- GRAM/EFHC: EQDMCqRzSnMtKjltr6jf4Fqah1o14Gdyq6sU5-XsNGkuIY9F
- RBTC/EFHC: EQAlrp2dgYMHbtp1X0_KujyZvpTHkjjEvic4kBa1FlNRZa8s
- EFHC master: EQDNcpWf9mXgSPDubDCzvuaX-juL4p8MuUwrQC-36sARRBuw
- RBTC master: EQCD7lrrxpOcq5A5R6nTLeF1kuIbl1BKCe5OnanGe3cB4FVB

## Causal graph: hypotheses and required tests
1. Net EFHC selling *volume* relative to pool depth -> reserve changes -> executed EFHC quote price movement. Test: verified swap direction, normalized amounts, reserves before/after, time-ordered quotes. Count of sells alone insufficient.
2. Liquidity withdrawal -> lower depth -> larger price impact for same trade. Test: confirmed LP withdrawal, reserve time series, counterfactual trade size and fees.
3. RBTC price volatility / RBTC liquidity -> RBTC/EFHC implied EFHC price -> possible cross-pool arbitrage -> transmitted price pressure to USDT/EFHC or GRAM/EFHC. Test: synchronized three-pool reserves, external RBTC/USD and GRAM/USD quotes, route costs, executed TON traces. Not yet established.
4. Repeated addresses or transaction timing -> potential coordinated execution OR shared router infrastructure / automated market-making. Test: identify contract types, causal message graph, gas/fee patterns, funding links and negative controls. Address coincidence is not legal identity or proof of common control.
5. Burst activity -> potential local price discontinuity. Test: 1m/5m/1h time buckets, price-before/after, independent news/market factors, baseline distribution.
6. Apparent price divergence -> arbitrage *possibility* after fees, slippage and latency. Test: route simulations; do not infer executed arbitrage from spreads alone.

## Observed leads
- EFHC hour 2026-10-16T19 UTC has 17 DYOR records (from exploratory hourly counts), a high-activity interval to inspect; do not infer sell-off without price and amount data.
- Nine overlapping EFHC/RBTC hashes merit transaction-level reconciliation. Overlap is not coordination.
- DYOR `who` and `whoFriendly` fields are available, but the first profiler only searched fields containing wallet/trader/sender/receiver; therefore `wallet_fields: {}` does NOT mean no wallet addresses exist. Correct the profiler before wallet analysis.
- DYOR `amount`, `counterpartAmount`, `price` are objects with value and decimals. All monetary calculations must use decimal-safe integer scaling, verify buy/sell semantics, counterpart asset and price units.

## Strategy / decision framework
Research first; no assertion of manipulation without multiple independently corroborated causal events. Prioritize the EFHC pool events (135), then the RBTC records sharing pool IDs/hashes with EFHC; do not conflate 20k broad RBTC activity with EFHC.
Operational goals: verified mapping of all three pool IDs; event ledger; hourly/daily EFHC buy/sell *volume* and reserve-adjusted pressure; address graph distinguishing contracts from traders; chronological RBTC–EFHC coupling; alternative hypotheses and falsification.
Do not change market positions or liquidity based solely on exploratory signals.

## Implementation roadmap
P0 DONE: bounded DYOR acquisition, SHA-256 manifest, first profiler and GitHub CI execution.
P1 OPEN: independently verify TON pool IDs; classify counterpart token, exact amount/price semantics and token decimals.
P2 OPEN: verified economic-event ledger, wallet-role identification, swap traces and 9 overlapping hashes.
P3 OPEN: volume-weighted net flows, reserves, price impact, liquidity-depth stress, time-window alerts.
P4 OPEN: three-pool synchronized arbitrage model with fees, slippage, confidence and counterexamples.
P5 OPEN: scheduled incremental collection, checkpoints, regression tests, immutable dated evidence, ongoing reports.

## Archive conventions
Keep raw data unchanged; append versioned reports. Reports must distinguish OBSERVED / DERIVED / HYPOTHESIS / UNVERIFIED. Include UTC, source, hashes, code revision and coverage. All collectors remain read-only. No secrets or personal deanonymization.
