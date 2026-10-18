# EFHC TON history status

Collector prepared for manual GitHub Actions execution. No successful run or historical transactions verified yet.

Scope: three TON mainnet STON.fi V2 pool addresses from OWNER.

Collector walks the account transaction chain backwards from latest LT/hash to genesis and writes JSONL. Each record currently contains the transaction string, not verified decoded jetton swap amounts or fees. `status.json` records completeness. If lite server history is pruned, an archive node/indexer is needed.

Future phases: decode STON.fi V2 swap payloads, LP deposits/withdrawals, fees and cross-pool traces; identify external traders without falsely counting internal transactions as separate swaps.
