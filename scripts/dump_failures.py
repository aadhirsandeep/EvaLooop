"""Write every failed loop of a run to a Markdown file for manual inspection.

Run inside the sandbox (needs evalplus for the test inputs / expected outputs):

    python scripts/dump_failures.py RESULTS_JSON OUT_MD [--min_cycle 2]

For each task whose loop ended before max_cycles at cycle >= --min_cycle (i.e. a failure
*induced by the loop*, not a plain cycle-1 failure), the dump shows:
  * the original MBPP+ prompt,
  * the description that fed the failing cycle (the model's own last summary),
  * the last passing code and the failing code,
  * which suite failed (base / plus) and the first failing test input with its expected output.
"""

import argparse
import json
import pickle
from pathlib import Path


def first_fail(details, inputs, expected):
    if details is None:
        return None
    flags = [int(ch) for ch in details] if isinstance(details, str) else list(details)
    for i, ok in enumerate(flags):
        if not ok and i < len(inputs):
            exp = expected[i] if expected is not None and i < len(expected) else "?"
            return f"input={inputs[i]!r}\nexpected={exp!r}"
    if len(flags) < len(inputs):  # evalplus stops at first failure/timeout
        i = len(flags)
        exp = expected[i] if expected is not None and i < len(expected) else "?"
        return f"input={inputs[i]!r}\nexpected={exp!r}  (stopped here: crash/timeout)"
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("out")
    ap.add_argument("--min_cycle", type=int, default=2)
    args = ap.parse_args()

    from evalplus.data import get_mbpp_plus, get_mbpp_plus_hash
    from evalplus.data.utils import CACHE_DIR
    problems = get_mbpp_plus()
    gt_file = Path(CACHE_DIR) / f"{get_mbpp_plus_hash()}.pkl"
    ground_truth = pickle.loads(gt_file.read_bytes()) if gt_file.exists() else {}

    data = json.loads(Path(args.results).read_text(encoding="utf-8"))
    run = data[0] if isinstance(data, list) else data
    m = run["max_cycles"]
    lines = [f"# Failed loops — {run['model']} — loop={run.get('loop', 'standard')}", ""]
    n = 0
    for r in run["prompt_results"]:
        fail_cycle = r["successful_cycles"] + 1
        if r["successful_cycles"] >= m or fail_cycle < args.min_cycle:
            continue
        n += 1
        cycles = {c["cycle"]: c for c in r["cycles"]}
        failing, passing = cycles.get(fail_cycle, {}), cycles.get(fail_cycle - 1, {})
        tr = failing.get("test_results", {})
        prob, gt = problems[r["task_id"]], ground_truth.get(r["task_id"], {})
        where = []
        if not tr.get("base_success", True):
            where.append("BASE: " + str(first_fail(tr.get("base_details"), prob["base_input"], gt.get("base"))))
        if not tr.get("plus_success", True):
            where.append("PLUS: " + str(first_fail(tr.get("plus_details"), prob["plus_input"], gt.get("plus"))))
        lines += [
            f"## {r['task_id']} — sustained {r['successful_cycles']}, failed at cycle {fail_cycle}",
            "", "**Original prompt**", "```", r["initial_prompt"].strip(), "```",
            "", f"**Description that fed cycle {fail_cycle}** (model's own summary from cycle {fail_cycle - 1})",
            "```", passing.get("task_2_output", "").strip(), "```",
            "", f"**Last passing code (cycle {fail_cycle - 1})**", "```python",
            passing.get("task_1_output", "").strip(), "```",
            "", f"**Failing code (cycle {fail_cycle})**", "```python",
            failing.get("task_1_output", "").strip(), "```",
            "", "**Test outcome**", "```", tr.get("error", "") or "\n".join(where) or "(no detail)", "```", "",
        ]
    lines.insert(1, f"\n{n} loop-induced failures (failed at cycle >= {args.min_cycle}).\n")
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {n} failures to {args.out}")


if __name__ == "__main__":
    main()
