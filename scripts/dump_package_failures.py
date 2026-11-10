"""Dump loop-induced failures (failed at cycle >= 2) from the assignment data package.

    python scripts/dump_package_failures.py PATH/TO/loops/gemini-2.5-flash-lite.json OUT_MD

Used only as the *reference* for what failures look like in the standard loop; the package
itself is not redistributed (records are referenced by model_id, task_id and cycle).
"""
import json
import sys
from pathlib import Path


def main() -> None:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    d = json.loads(src.read_text(encoding="utf-8"))
    m = 10
    lines = [f"# Data-package loop-induced failures — {d['model_id']}", ""]
    n = 0
    for t in d["tasks"]:
        i = t["successful_cycles"]
        if not 1 <= i < m:
            continue
        n += 1
        cyc = {c["cycle"]: c for c in t["cycles"]}
        failing, passing = cyc.get(i + 1, {}), cyc.get(i, {})
        lines += [
            f"## {t['task_id']} — sustained {i}, failed at cycle {i + 1} "
            f"(judge similarity {t.get('boundary_similarity')})", "",
            "**Original prompt**", "```", t["initial_prompt"].strip(), "```", "",
            f"**Description that fed cycle {i + 1}**", "```", (passing.get("summary") or "").strip(), "```", "",
            f"**Last passing code (cycle {i})**", "```python", (passing.get("code") or "").strip(), "```", "",
            f"**Failing code (cycle {i + 1})** base_passed={failing.get('base_passed')} "
            f"plus_passed={failing.get('plus_passed')}", "```python", (failing.get("code") or "").strip(), "```", "",
        ]
    lines.insert(1, f"\n{n} loop-induced failures.\n")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {n} failures to {out}")


if __name__ == "__main__":
    main()
