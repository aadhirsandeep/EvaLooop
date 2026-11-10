"""Quick statistics of a Vertex call log: python scripts/call_stats.py LOG.jsonl [...]"""
import json
import sys

for f in sys.argv[1:]:
    cs = []
    for line in open(f, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                cs.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    ok = [c for c in cs if not c.get("error")]
    lat = sorted(c["latency_s"] for c in ok)
    span = (max(c["time"] for c in cs) - min(c["time"] for c in cs)) / 60 if cs else 0
    print(f"{f}: calls={len(cs)} errors={len(cs) - len(ok)} "
          f"length={sum(c.get('finish_reason') == 'length' for c in ok)} "
          f"p50_latency={lat[len(lat) // 2] if lat else None}s "
          f"in={sum(c.get('prompt_tokens') or 0 for c in ok)} out={sum(c.get('completion_tokens') or 0 for c in ok)} "
          f"reasoning={sum(c.get('reasoning_tokens') or 0 for c in ok)} span={span:.1f}min")
    for c in [c for c in cs if c.get("error")][:3]:
        print("   ", c["error"][:120])
