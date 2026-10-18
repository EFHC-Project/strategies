# EFHC Strategies — Scientific Research Architecture v001

Date: 2026-10-18. Status: DESIGN / NOT IMPLEMENTED. Scope: three STON.fi V2 TON pools, on-chain economics and reproducible evidence.

## 1. Evidence baseline
Observed: GitHub Actions run 39142840992, archived under `archive/ton-history/2026-10-18-run-39142840992/`. Collector reports 13 USDT/EFHC, 39 GRAM/EFHC, 44 RBTC/EFHC transaction records (96 total). USDT and GRAM incomplete due to lite server code -400 cannot locate historical LT. RBTC marked complete by collector's chain-termination criterion only; independent archive verification remains pending. Current records are tx.String() summaries, not canonical transaction BOCs. No verified decoded swaps, prices, trader identities or fee totals exist.

## 2. Scientific questions and hypotheses
H1: pool prices converge via economically viable cross-pool arbitrage after accounting for all costs.
H2: repeated contract messages represent fewer economic events than on-chain account transactions.
H3: distinct observed message senders may belong to common router/jetton-wallet infrastructures; identity resolution must be supported by contract state/code and traces, not sender equality.
H4: liquidity depth and trade size predict realized slippage and price impact.
H5: USDT/EFHC, GRAM/EFHC and RBTC/EFHC share an EFHC price system but may have different liquidity and independent demand.

Hypotheses are not findings. Pre-register measurable criteria and counterexamples before evaluation.

## 3. Pipeline
A. Sources: archival TON node and at least one independent indexed provider; preserve provider URL/type, retrieval time, block, account, cursor, retry history, errors and source response digests. Never commit API keys.
B. Raw: store canonical BOC or independently verified canonical transaction hash, transaction LT, prev hash/LT, block shard/seqno, inbound/outbound messages, bodies and state changes; immutable, content-addressed snapshots.
C. Normalize: deterministic schema version; raw addresses plus friendly addresses; amounts as integer nano units and token decimals; timestamps UTC; deduplicate by (account, lt, tx hash).
D. Decode: identify STON.fi V2 pool/router and jetton wallet code versions; map opcode and query_id; trace internal messages; classify swap, deposit, withdrawal, refund, bounced, fee, transfer, unknown; maintain decoder provenance.
E. Economic events: group multiple account transactions into one economic action by verified message hashes and causal traces; distinguish actor wallet, router, jetton wallet and pool. Mark attribution confidence.
F. Analytics: reserve time series, executed prices, liquidity, slippage, fees, routing, cross-pool spread, arbitrage feasibility, counterfactual simulations.
G. Reports: reproducible notebooks/scripts, dated JSON results, human-readable Markdown, links to exact chain evidence and code revision.

## 4. Quantitative methods
For a verified constant-product pool with reserves x (quote) and y (EFHC), spot quote price is x/y. For an input dx and fee fraction f, theoretical EFHC output is dy = y*dx*(1-f)/(x+dx*(1-f)). This is only a model until pool contract fee logic and token behavior are verified.
Normalize USD prices using time-aligned, provenance-stamped external rates: P_USDT = U/E_U * USD_per_USDT; P_GRAM = G/E_G * USD_per_GRAM; P_RBTC = R/E_R * USD_per_RBTC.
A positive apparent spread is not sufficient: model gas, pool fees, multi-hop fees, slippage, execution latency, price movement, failed routes and liquidity constraints. Do not present modeled opportunity as executed profit.
Use uncertainty bands and sensitivity analysis when source prices, reserves or decimals are missing.

## 5. Scientific controls
- Completeness is a per-account, per-interval property with explicit earliest/latest verified LT and chain continuity. `PrevTxLT==0` is a provisional signal, not independent proof.
- Reconcile each account chain by prev LT/hash and cross-check transaction hashes with a second source.
- Test TON bounce/refund semantics; message-value is not trade volume.
- Verify jetton master and wallet contracts, decimals, metadata and STON.fi V2 deployment identities.
- Distinguish source observation, decoded fact, inference, hypothesis and unresolved lead.
- Preserve unknown classifications; never silently force swaps.
- Deterministic reruns; pinned dependencies and `go.sum`; SHA-256 manifests; schema migrations and regression fixtures.
- Avoid secrets, private user information and deanonymization claims; on-chain address is not legal identity.

## 6. Repository target
```
README.md
AGENTS.md
docs/CANON/RESEARCH_CANON.md
docs/NORM/EVENT_SCHEMA.md
docs/METHODS/PRICE_AND_ARBITRAGE.md
config/pools.json
sources/source_registry.json
tools/ton-history/
tools/decoder/
tools/tracer/
tools/analysis/
tests/fixtures/
archive/ton-history/
data/normalized/
data/events/
reports/
.github/workflows/
```
Data directories can be generated and excluded from Git when large. For small verified evidence snapshots, Git is acceptable; for large histories use versioned releases or object storage with immutable checksums and a Git manifest. Do not commit huge BOCs blindly.

## 7. Bounded implementation phases
P0: update stale status, pin dependencies, validate artifact contents and provenance, add smoke/unit tests and CI gates.
P1: implement BOC capture, canonical hashes, explicit cursor checkpoints, continuity validator, incremental append and restart safety.
P2: archival-provider fallback with coverage report and independent cross-check for all three pools.
P3: STON.fi V2 contract/version detection and message-body decoding with fixtures from verified chain data.
P4: causal transaction graph and economic-event reconstruction; label router and wallet contracts.
P5: historical reserves, quotes, slippage, fees, and cross-pool price/arbitrage studies with confidence intervals.
P6: reproducible periodic reports and anomaly alerts with anti-duplication and bounded data retention.

Each phase requires code review, tests, source provenance and explicit PASS/FAIL/INCOMPLETE evidence. Do not mark any phase complete solely from file creation.

## 8. Initial acceptance criteria
- Every archived record has account, LT, transaction hash, UTC timestamp, canonical raw payload reference, source, schema version.
- No duplicate (account,LT,hash) records; continuity breaks explicitly listed.
- All three pool addresses verified against chain contract state and STON.fi deployment metadata.
- One independently traced swap demonstrates a complete causal path and validated token deltas.
- Three pools each have an explicit time-bounded completeness report.
- Any financial metric links to its underlying verified economic events, price source and code revision.

## 9. Priority
The highest-value change is full raw capture and trace reconstruction, not adding dashboards or more aggregate charts. Until then the observed 96 account transactions should not be converted into claims about trading volume, unique users, arbitrage profit or fees.
