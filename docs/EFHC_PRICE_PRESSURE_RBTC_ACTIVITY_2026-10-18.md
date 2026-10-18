# EFHC price pressure and RBTC activity — owner observation

Date: 2026-10-18
Status: OPEN HYPOTHESIS / NOT ATTRIBUTED

## Owner observation

The owner reports price pressure on EFHC and notable RBTC activity. These are separate investigation tracks; no claim of coordinated or intentional manipulation is established by this record.

## Evidence currently collected

- DYOR STON.fi token transaction feed: EFHC 135 unique records, end of API feed reached; RBTC 20,000 unique records, explicit cap reached, not full history.
- Source: `archive/dyor/2026-10-18/manifest.json` and corresponding `EFHC.jsonl.gz`, `RBTC.jsonl.gz`.
- The DYOR token feed spans multiple pools; it is not yet restricted to the three target EFHC pools.

## Verification tasks

1. Map DYOR raw pool identifiers to on-chain pool addresses and filter USDT/EFHC, GRAM/EFHC and RBTC/EFHC.
2. Separate swaps from liquidity actions, and identify actual EFHC buy/sell direction and volume, respecting token decimals.
3. Reconstruct chronological price and reserve movements per pool; quantify net flow, slippage and intervals of downward pressure.
4. Inspect RBTC transactions interacting with EFHC, separating unrelated RBTC pool activity.
5. Compare trader wallets, repeated transaction sequences, transaction hashes and temporal coincidences; distinguish correlations from evidence of common control.
6. Cross-check material events with canonical TON transactions/traces, and grade source reliability.

## Interpretation rule

Price pressure is an analytical hypothesis, not a finding of market manipulation. RBTC transaction volume in its overall token feed cannot be attributed to EFHC without pool filtering. Preserve contrary evidence and uncertainty. No accusations or wallet attribution without independently corroborated evidence.
