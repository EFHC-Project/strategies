#!/usr/bin/env python3
"""Archive DYOR token transactions with cursor continuity and auditable coverage."""
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

TOKENS = {
    "EFHC": "EQDNcpWf9mXgSPDubDCzvuaX-juL4p8MuUwrQC-36sARRBuw",
    "RBTC": "EQCD7lrrxpOcq5A5R6nTLeF1kuIbl1BKCe5OnanGe3cB4FVB",
}
POOLS = {
    "USDT_EFHC": "EQB2iz4-oG50xuXjbRYc-h-TR-Siow7ynH0XGNsor_lgg8D2",
    "GRAM_EFHC": "EQDMCqRzSnMtKjltr6jf4Fqah1o14Gdyq6sU5-XsNGkuIY9F",
    "RBTC_EFHC": "EQAlrp2dgYMHbtp1X0_KujyZvpTHkjjEvic4kBa1FlNRZa8s",
}
MAX_PAGES = int(os.environ.get("DYOR_MAX_PAGES", "2500"))
DEADLINE = time.monotonic() + int(os.environ.get("DYOR_SECONDS", "3000"))
ROOT = Path("archive/dyor") / dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
ROOT.mkdir(parents=True, exist_ok=True)

def request(token, cursor):
    params = {"limit": 100, "exchangeId": "stonfi"}
    if cursor:
        params["cursor"] = cursor
    url = f"https://api.dyor.io/v1/jettons/{urllib.parse.quote(token)}/transactions?{urllib.parse.urlencode(params)}"
    for attempt in range(7):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "EFHC-Strategies-Research/1.0"})
            with urllib.request.urlopen(req, timeout=45) as resp:
                raw = resp.read(8_000_000)
                obj = json.loads(raw)
                if not isinstance(obj, dict) or not isinstance(obj.get("transactions"), list):
                    raise ValueError("Unexpected DYOR API response schema")
                return obj
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            if isinstance(exc, urllib.error.HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                raise
            if attempt == 6:
                raise
            time.sleep(min(60, 2 ** attempt) + random.random())
    raise RuntimeError("Retries exhausted")

def main():
    summary = {"schema": "dyor-cursor-archive-v1", "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "source": "https://api.dyor.io/v1/jettons/{address}/transactions",
               "parameters": {"limit": 100, "exchangeId": "stonfi"}, "tokens": {}, "pool_addresses": POOLS,
               "caveat": "DYOR transaction feed, not independent TON BOC verification. A token feed may include other pools."}
    for symbol, address in TOKENS.items():
        path = ROOT / (symbol + ".jsonl.gz")
        cursor = None
        seen_cursors = set()
        seen_events = set()
        pages = 0
        records = 0
        duplicates = 0
        complete = False
        error = None
        pool_counts = {}
        min_time = None
        max_time = None
        # One compact compressed file per token, preserving raw transaction fields.
        with gzip.open(path, "wt", encoding="utf-8", compresslevel=6) as out:
            while pages < MAX_PAGES and time.monotonic() < DEADLINE:
                try:
                    response = request(address, cursor)
                except Exception as exc:
                    error = f"{type(exc).__name__}: {str(exc)[:350]}"
                    break
                batch = response["transactions"]
                next_cursor = response.get("next")
                if next_cursor and (not isinstance(next_cursor, str) or next_cursor in seen_cursors):
                    error = "Repeated/invalid cursor"
                    break
                for item in batch:
                    if not isinstance(item, dict):
                        error = "Non-object transaction"
                        break
                    event_key = (str(item.get("hash")), str(item.get("timeLt")), str(item.get("pool")), str(item.get("type")))
                    if event_key in seen_events:
                        duplicates += 1
                        continue
                    seen_events.add(event_key)
                    out.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")
                    records += 1
                    p = str(item.get("pool", "UNKNOWN"))
                    pool_counts[p] = pool_counts.get(p, 0) + 1
                    t = item.get("time")
                    if isinstance(t, str):
                        min_time = min(min_time, t) if min_time else t
                        max_time = max(max_time, t) if max_time else t
                if error:
                    break
                pages += 1
                if pages % 20 == 0:
                    print(f"{symbol}: pages={pages}, unique={records}, duplicates={duplicates}", flush=True)
                    out.flush()
                if not next_cursor:
                    complete = True
                    break
                seen_cursors.add(next_cursor)
                cursor = next_cursor
                if not batch:
                    error = "Empty page with next cursor"
                    break
                time.sleep(0.12)
            if not complete and not error:
                error = "Pagination limit or time budget reached"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        summary["tokens"][symbol] = {"address": address, "pages": pages, "unique_records": records,
            "duplicates_skipped": duplicates, "reached_end_of_feed": complete, "error": error,
            "last_cursor": cursor if not complete else None, "first_time_utc": min_time,
            "last_time_utc": max_time, "pool_counts_raw": pool_counts,
            "file": path.name, "sha256": digest}
        print(json.dumps({symbol: summary["tokens"][symbol]}, ensure_ascii=False), flush=True)
        if time.monotonic() >= DEADLINE:
            break
    summary["completed_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    (ROOT / "manifest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    if not all(summary["tokens"].get(s, {}).get("reached_end_of_feed") for s in TOKENS):
        print("INCOMPLETE: inspect manifest.json", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
