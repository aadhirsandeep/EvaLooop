"""Share of passing summaries that mention an implementation method (report, Section 4).

    python scripts/summary_style.py RESULTS_JSON [...]

A summary "mentions an implementation method" if it matches the keyword pattern for its language
(English: using/via/by iterating/algorithm/regex/heap/zip/...; Chinese: 使用/利用/通过/算法/正则/...).
This is a coarse keyword count, not a semantic judgment.
"""
import json
import re
import statistics
import sys

EN = re.compile(r"\b(using|uses|via|by (iterating|using|converting|checking|applying|leveraging|creating|"
                r"sorting|counting|recursively)|with (a|the) (loop|heap|regular expression|list comprehension|"
                r"dictionary|set)|algorithm|regular expression|regex|list comprehension|heap|zip|lambda|recurs)",
                re.I)
ZH = re.compile(r"(使用|利用|通过|借助|采用|算法|正则|递归|堆|列表推导|zip|lambda|循环)")

for path in sys.argv[1:]:
    data = json.load(open(path, encoding="utf-8"))
    run = data[0] if isinstance(data, list) else data
    pattern = ZH if run.get("loop") == "crosslingual" else EN
    summaries = [c["task_2_raw_output"] for p in run["prompt_results"] for c in p["cycles"]
                 if c.get("success") and c.get("task_2_raw_output")]
    hits = sum(bool(pattern.search(s)) for s in summaries)
    print(f"{path}: n={len(summaries)} median_chars={statistics.median(len(s) for s in summaries):.0f} "
          f"implementation-method mention={hits / len(summaries):.2f}")
