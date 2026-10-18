import collections, gzip, hashlib, json, pathlib
root=pathlib.Path("archive/dyor/2026-10-18")
m=json.loads((root/"manifest.json").read_text())
result={"source":str(root/"manifest.json"),"tokens":{}}
hashes={}
for token,meta in m["tokens"].items():
    p=root/meta["file"]
    assert hashlib.sha256(p.read_bytes()).hexdigest()==meta["sha256"]
    fields=collections.Counter(); pools=collections.Counter(); kinds=collections.Counter(); hours=collections.Counter()
    wallets=collections.defaultdict(collections.Counter); ids=set(); count=0; examples={}
    with gzip.open(p,"rt") as stream:
        for line in stream:
            row=json.loads(line); count+=1
            for key,value in row.items():
                fields[key]+=1
                if key not in examples: examples[key]=str(value)[:100]
                if isinstance(value,str) and any(w in key.lower() for w in ("wallet","trader","sender","receiver")):
                    wallets[key][value]+=1
            pools[str(row.get("pool","UNKNOWN"))]+=1
            kinds[str(row.get("type","UNKNOWN"))]+=1
            if isinstance(row.get("time"),str): hours[row["time"][:13]]+=1
            if row.get("hash"): ids.add(str(row["hash"]))
    assert count==meta["unique_records"]
    hashes[token]=ids
    result["tokens"][token]={"records":count,"end_of_feed":meta["reached_end_of_feed"],
       "limit_reached":meta["limit_reached"],"fields":dict(fields),"field_examples":examples,
       "pools":dict(pools),"event_types":dict(kinds),"hourly_counts":dict(sorted(hours.items())),
       "wallet_fields":{k:{"unique":len(v),"top20":v.most_common(20)} for k,v in wallets.items()},
       "distinct_hashes":len(ids)}
result["shared_hashes_EFHC_RBTC"]=len(hashes.get("EFHC",set()) & hashes.get("RBTC",set()))
result["limitations"]=["No price-pressure conclusion from counts alone","Pool ID mapping pending independent verification","Wallet clustering is not identity attribution","TON traces and decimal-adjusted amounts not yet verified"]
out=pathlib.Path("reports/dyor");out.mkdir(parents=True,exist_ok=True)
(out/"analysis.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
lines=["# DYOR transaction analysis","", "Exploratory analysis; no market-manipulation finding.",""]
for token,x in result["tokens"].items():
    lines.extend(["## "+token,"Records: "+str(x["records"]),"Pools: "+str(len(x["pools"])),
      "Event types: "+json.dumps(x["event_types"],ensure_ascii=False),""])
lines.append("Shared hashes: "+str(result["shared_hashes_EFHC_RBTC"]))
lines.extend(["","Next: map TON pool addresses, validate swap direction and reserves, trace material events."])
(out/"analysis.md").write_text("\n".join(lines)+"\n")
print("\n".join(lines))
