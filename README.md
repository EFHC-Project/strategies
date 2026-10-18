# EFHC Strategies — on-chain research

Dedicated repository for EFHC strategy research and read-only TON pool transaction audits.

This repository is separate from EFHC application and frontend code. No private keys, wallet credentials or trading operations are permitted.

## Monitored pools (TON mainnet)
- USDT/EFHC: `EQB2iz4-oG50xuXjbRYc-h-TR-Siow7ynH0XGNsor_lgg8D2`
- GRAM/EFHC: `EQDMCqRzSnMtKjltr6jf4Fqah1o14Gdyq6sU5-XsNGkuIY9F`
- RBTC/EFHC: `EQAlrp2dgYMHbtp1X0_KujyZvpTHkjjEvic4kBa1FlNRZa8s`

The workflow runs a read-only historical collector and uploads JSONL plus a completion report as a GitHub Actions artifact. An incomplete history must never be described as complete.
