# Sandbox image for running EvaLoop experiments with API models.
#
# Generated code is executed by EvalPlus inside this container, never on the host:
#   * only the repository is mounted (read-write, for results) plus the Google
#     credentials file (read-only); no other host files are visible;
#   * the container runs as an unprivileged user;
#   * EvalPlus additionally runs each candidate in a subprocess with a time limit,
#     a memory limit and reliability_guard() (os.remove, subprocess, ... disabled).
# torch/vllm are deliberately not installed: API-only runs do not need them.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

RUN pip install \
        "evalplus==0.3.1" \
        "openai>=1.40,<2" \
        "google-auth>=2.30" \
        "requests>=2.31" \
        "fire>=0.5" \
        "tqdm>=4.60" \
        "pyyaml>=6.0" \
        "pandas>=2.0" \
        "matplotlib>=3.7" \
        "seaborn>=0.12" \
        "pytest>=7.0" \
        "ruff>=0.4"

RUN useradd --create-home --uid 1000 runner
USER runner
WORKDIR /work
ENV PYTHONPATH=/work
