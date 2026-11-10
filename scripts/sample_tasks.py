"""Draw a reproducible random subset of MBPP+ task ids.

Usage (inside the sandbox):
    python scripts/sample_tasks.py --n 150 --seed 20261110 --out experiments/task_subset_150.txt

Tasks are sampled uniformly without replacement from the 378 MBPP+ v0.2.0 tasks with
Python's ``random.Random(seed).sample`` and written in ascending numeric order.
"""
import argparse
import random

from evalplus.data import get_mbpp_plus


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--seed", type=int, default=20261110)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    task_ids = sorted(get_mbpp_plus(), key=lambda t: int(t.split("/")[1]))
    subset = sorted(random.Random(args.seed).sample(task_ids, args.n),
                    key=lambda t: int(t.split("/")[1]))
    with open(args.out, "w") as f:
        f.write(f"# {args.n} of {len(task_ids)} MBPP+ tasks, random.Random({args.seed}).sample\n")
        f.write("\n".join(subset) + "\n")
    print(f"wrote {len(subset)} task ids to {args.out}")


if __name__ == "__main__":
    main()
