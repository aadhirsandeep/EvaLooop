"""Run several EvaLoop configurations in one process (dataset loaded once, runs in parallel).

    python scripts/run_matrix.py experiments/matrix_main.json

The matrix file is a list of objects with EvaluationConfig fields, e.g.::

    [{"experiment_name": "flashlite_standard", "model": "vertex/google/gemini-3.1-flash-lite",
      "loop": "standard", "prompt_set": "data_package", "output_dir": "results/main",
      "max_new_tokens": 1024, "concurrency": 16}]

Runs whose results file already exists are skipped, so an interrupted matrix can be resumed.
Each run is identical to ``python -m evaloop evaluate`` with the same arguments.
"""
import json
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaloop.core.config import EvaluationConfig  # noqa: E402
from evaloop.core.evaluator import EvaLoopEvaluator, _cached_mbpp_dataset  # noqa: E402


def run_one(spec: dict) -> str:
    cfg = EvaluationConfig(**spec)
    out = Path(cfg.output_dir) / f"{cfg.experiment_name}_{cfg.get_loop_task_type()}_results.json"
    if out.exists():
        return f"{cfg.experiment_name}: exists, skipped"
    start = time.time()
    try:
        EvaLoopEvaluator(cfg).run_loop()
    except Exception as exc:  # keep the other runs going
        logging.exception(f"{cfg.experiment_name} failed")
        return f"{cfg.experiment_name}: FAILED {exc!r}"
    return f"{cfg.experiment_name}: done in {time.time() - start:.0f}s"


def main() -> None:
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    specs = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
    _cached_mbpp_dataset()  # load the ~1.8 GB ground truth once, before the threads start
    with ThreadPoolExecutor(max_workers=len(specs)) as pool:
        for line in pool.map(run_one, specs):
            print(line, flush=True)


if __name__ == "__main__":
    main()
