"""Aggregate EvaLoop runs: metrics, summary.csv, paired loop comparison, compliance checks.

Usage (host or sandbox; needs only the standard library + evaloop.analysis.metrics):

    python scripts/analyze_runs.py --runs experiments/runs.json --out experiments/analysis

``runs.json`` lists the runs to aggregate::

    [{"model": "gemini-3.1-flash-lite", "configuration": "standard-mbpp-plus",
      "results": "results/main/flashlite_standard_code_generation_summarization_results.json",
      "calls": "results/main/flashlite_standard_calls.jsonl"}, ...]

Outputs (in --out):
    summary.csv            one row per run (assignment format)
    metrics.json           all metrics, histograms, compliance and call-log statistics per run
    paired.json / .md      per-model paired comparison standard vs. cross-lingual loop
"""

import argparse
import csv
import json
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaloop.analysis.metrics import (  # noqa: E402
    asl_bias, asl_pow, cycle_histogram, pass_at_k, pass_drop,
)

ERROR_PREFIX = "Error generating response"
SCRIPT_RANGES = {
    "zh": [(0x4E00, 0x9FFF), (0x3400, 0x4DBF)],          # CJK unified ideographs
    "ja": [(0x3040, 0x30FF), (0x4E00, 0x9FFF)],
    "hi": [(0x0900, 0x097F)],                             # Devanagari
    "bn": [(0x0980, 0x09FF)],
    "ru": [(0x0400, 0x04FF)],
    "ar": [(0x0600, 0x06FF)],
}


def load_run(path: str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data[0] if isinstance(data, list) else data


def summary_text(cycle: Dict[str, Any]) -> str:
    """The model's raw summary (without docstring wrapper / assert line)."""
    return cycle.get("task_2_raw_output") or ""


def target_script_share(text: str, lang: str) -> float:
    """Share of alphabetic characters (outside code spans) written in the target script."""
    ranges = SCRIPT_RANGES.get(lang)
    if not ranges:
        return float("nan")
    text = re.sub(r"`[^`]*`", " ", text)  # inline code / identifiers are expected in Latin
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return 0.0
    hits = sum(1 for ch in letters if any(lo <= ord(ch) <= hi for lo, hi in ranges))
    return hits / len(letters)


def run_metrics(entry: Dict[str, Any], subset=None) -> Dict[str, Any]:
    run = load_run(entry["results"])
    cfg = run.get("config", {})
    max_cycles = run.get("max_cycles", 10)
    results = run["prompt_results"]
    if subset is not None:
        results = [r for r in results if r["task_id"] in subset]
    sustained = [r["successful_cycles"] for r in results]
    lang = cfg.get("summary_language") if run.get("loop") == "crosslingual" else None

    infra_tasks, n_summaries, compliant, code_in_summary, shares = [], 0, 0, 0, []
    for r in results:
        for c in r["cycles"]:
            if any(str(c.get(k, "")).startswith(ERROR_PREFIX)
                   for k in ("task_1_raw_output", "task_2_raw_output")) or \
                    any(k.endswith("_error") for k in c):
                infra_tasks.append(r["task_id"])
            if c.get("success") and summary_text(c):
                n_summaries += 1
                s = summary_text(c)
                if "```" in s or re.search(r"\bdef \w+\(", s):
                    code_in_summary += 1
                if lang:
                    share = target_script_share(s, lang)
                    shares.append(share)
                    compliant += share >= 0.5

    calls = {"n": 0, "errors": 0, "length_truncated": 0, "prompt_tokens": 0,
             "completion_tokens": 0, "latency_s": 0.0}
    if entry.get("calls") and Path(entry["calls"]).exists():
        for line in Path(entry["calls"]).read_text(encoding="utf-8").splitlines():
            c = json.loads(line)
            calls["n"] += 1
            if c.get("error"):
                calls["errors"] += 1
                continue
            calls["length_truncated"] += c.get("finish_reason") == "length"
            calls["prompt_tokens"] += c.get("prompt_tokens") or 0
            calls["completion_tokens"] += c.get("completion_tokens") or 0
            calls["latency_s"] += c.get("latency_s") or 0.0

    return {
        "model": entry["model"],
        "configuration": entry["configuration"],
        "loop": run.get("loop", "standard"),
        "prompt_set": cfg.get("prompt_set"),
        "summary_language": lang,
        "n_tasks": len(results),
        "max_cycles": max_cycles,
        "pass@1": pass_at_k(sustained, 1),
        "success_rate": pass_at_k(sustained, 1) / len(results),
        "asl_pow": asl_pow(sustained, max_cycles),
        "asl_bias": asl_bias(sustained, max_cycles),
        "pass_drop": pass_drop(sustained, max_cycles),
        "pass@k": [pass_at_k(sustained, k) for k in range(1, max_cycles + 1)],
        "histogram": cycle_histogram(sustained, max_cycles),
        "mean_sustained": sum(sustained) / len(sustained),
        "infra_error_tasks": sorted(set(infra_tasks)),
        "summaries_after_pass": n_summaries,
        "summaries_with_code": code_in_summary,
        "language_compliant": compliant if lang else None,
        "mean_target_script_share": (sum(shares) / len(shares)) if shares else None,
        "calls": calls,
        "sustained_by_task": {r["task_id"]: r["successful_cycles"] for r in results},
        "cycle1_code_by_task": {r["task_id"]: (r["cycles"][0].get("task_1_output") if r["cycles"] else None)
                                for r in results},
    }


def bootstrap_ci(diffs: List[float], n_boot: int = 10000, seed: int = 0):
    rng = random.Random(seed)
    n = len(diffs)
    means = sorted(sum(rng.choice(diffs) for _ in range(n)) / n for _ in range(n_boot))
    return means[int(0.025 * n_boot)], means[int(0.975 * n_boot)]


def paired(std: Dict[str, Any], ext: Dict[str, Any]) -> Dict[str, Any]:
    """Task-level comparison of two runs of the same model on the same tasks."""
    tasks = sorted(set(std["sustained_by_task"]) & set(ext["sustained_by_task"]),
                   key=lambda t: int(t.split("/")[1]))
    m = std["max_cycles"]
    a = [std["sustained_by_task"][t] for t in tasks]
    b = [ext["sustained_by_task"][t] for t in tasks]
    # Per-task contribution to ASL_pow is i^2 / M, so the ASL difference is the mean of these.
    contrib = [(y * y - x * x) / m for x, y in zip(a, b)]
    lo, hi = bootstrap_ci(contrib)
    both_pass1 = [t for t, x, y in zip(tasks, a, b) if x >= 1 and y >= 1]
    same_code1 = sum(1 for t in tasks if std["cycle1_code_by_task"][t] == ext["cycle1_code_by_task"][t])
    return {
        "model": std["model"],
        "baseline": std["configuration"],
        "extension": ext["configuration"],
        "n_tasks": len(tasks),
        "asl_pow_standard": asl_pow(a, m),
        "asl_pow_extension": asl_pow(b, m),
        "asl_pow_diff": asl_pow(b, m) - asl_pow(a, m),
        "asl_pow_diff_95ci_bootstrap": [lo, hi],
        "mean_sustained_standard": sum(a) / len(a),
        "mean_sustained_extension": sum(b) / len(b),
        "tasks_extension_shorter": sum(y < x for x, y in zip(a, b)),
        "tasks_extension_longer": sum(y > x for x, y in zip(a, b)),
        "tasks_equal": sum(y == x for x, y in zip(a, b)),
        "tasks_pass1_both": len(both_pass1),
        "survive10_standard_among_pass1_both": sum(std["sustained_by_task"][t] == m for t in both_pass1),
        "survive10_extension_among_pass1_both": sum(ext["sustained_by_task"][t] == m for t in both_pass1),
        "cycle1_identical_code": same_code1,
        "cycle1_pass_agreement": sum((x >= 1) == (y >= 1) for x, y in zip(a, b)),
        "broken_by_extension": [t for t, x, y in zip(tasks, a, b) if x == m and y < m],
        "rescued_by_extension": [t for t, x, y in zip(tasks, a, b) if y == m and x < m],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--subset", help="task-id file; restrict every run to these tasks")
    args = parser.parse_args()

    entries = json.loads(Path(args.runs).read_text(encoding="utf-8"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    subset = None
    if args.subset:
        subset = {line.split("#")[0].strip() for line in Path(args.subset).read_text().splitlines()}
        subset.discard("")
    metrics = [run_metrics(e, subset) for e in entries]

    with open(out / "summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["model", "configuration", "n_tasks", "success_rate", "asl_score"])
        for m in metrics:
            writer.writerow([m["model"], m["configuration"], m["n_tasks"],
                             f"{m['success_rate']:.3f}", f"{m['asl_pow']:.3f}"])

    slim = [{k: v for k, v in m.items() if k not in ("sustained_by_task", "cycle1_code_by_task")}
            for m in metrics]
    (out / "metrics.json").write_text(json.dumps(slim, indent=2), encoding="utf-8")

    pairs = []
    for m in metrics:
        if m["loop"] != "standard":
            std = next((s for s in metrics if s["model"] == m["model"] and s["loop"] == "standard"
                        and s["prompt_set"] == m["prompt_set"]), None)
            if std:
                pairs.append(paired(std, m))
    (out / "paired.json").write_text(json.dumps(pairs, indent=2), encoding="utf-8")

    lines = ["| model | configuration | T | pass@1 | ASL_pow | ASL_bias | pass_drop | pass@10 | "
             "lang-compliant | summaries w/ code | truncated calls | API errors |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in metrics:
        comp = "-" if m["language_compliant"] is None else \
            f"{m['language_compliant']}/{m['summaries_after_pass']}"
        lines.append(
            f"| {m['model']} | {m['configuration']} | {m['n_tasks']} | {m['success_rate']:.3f} | "
            f"{m['asl_pow']:.3f} | {m['asl_bias']:.3f} | {m['pass_drop']:.3f} | {m['pass@k'][-1]} | "
            f"{comp} | {m['summaries_with_code']}/{m['summaries_after_pass']} | "
            f"{m['calls']['length_truncated']} | {m['calls']['errors']} |")
    lines += ["", "| model | extension | ΔASL_pow | 95% CI | shorter | longer | equal | "
              "cycle-1 pass agreement | broken (10→<10) | rescued (<10→10) |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for p in pairs:
        lines.append(
            f"| {p['model']} | {p['extension']} | {p['asl_pow_diff']:+.3f} | "
            f"[{p['asl_pow_diff_95ci_bootstrap'][0]:+.3f}, {p['asl_pow_diff_95ci_bootstrap'][1]:+.3f}] | "
            f"{p['tasks_extension_shorter']} | {p['tasks_extension_longer']} | {p['tasks_equal']} | "
            f"{p['cycle1_pass_agreement']}/{p['n_tasks']} | {len(p['broken_by_extension'])} | "
            f"{len(p['rescued_by_extension'])} |")
    (out / "tables.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
