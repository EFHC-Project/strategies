# Research consolidation report — 2026-10-18

Status: DOCUMENTATION UPDATED / RAW DATA PRESERVED / CAUSAL TESTS PENDING

## Changes
- Added `docs/ACTIVE_RESEARCH_STATE_2026-10-18.md` as consolidated working state.
- Updated repository README to point to current evidence and analytical methods.
- Preserved existing raw DYOR and partial TON archives without modification.

## Evidence
- DYOR EFHC 135, exhausted feed; RBTC 20,000, bounded sample.
- EFHC: 59 buys, 52 sells, 23 liquidity deposits, 1 withdrawal.
- RBTC: 5,125 buys, 14,829 sells, 28 deposits, 18 withdrawals across 14 pool IDs.
- 9 overlapping transaction hashes. All are indexed observations, not independently decoded TON economic events.
- No confirmed causal attribution, net sell volume, price impact, trader ownership, or manipulation finding.

## Defects and risks identified
- DYOR raw pool identifiers not yet verified against target friendly TON pool addresses.
- First profiler omits DYOR `who` field in wallet-frequency report; absence of output does not mean absence of wallets.
- The source architecture document retains its original design-era status; this currentization supersedes only its implementation-status section, not its methods.
- No fully reproducible physical ZIP release generated; Git repository is current working archive.
- Partial TON lite-server records do not support exact swap metrics.

## Acceptance / next cycle
1. Implement canonical TON address normalization and verified pool mapping.
2. Fix wallet-field detection and run identity-safe address-role profiling.
3. Verify token decimals, units and direction; reconstruct per-pool net flows.
4. Decode 9 overlapping hashes and inspect EFHC high-activity interval.
5. Produce time-aligned reserves, liquidity, impact, cross-pool spread and falsification tests.
6. Generate immutable release manifest and reproducible downloadable ZIP after data and analysis acceptance.

Source of truth: `docs/ACTIVE_RESEARCH_STATE_2026-10-18.md`.
