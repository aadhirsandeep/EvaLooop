#!/usr/bin/env bash
# Linux/macOS equivalent of sandbox.ps1.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ADC="${GOOGLE_APPLICATION_CREDENTIALS:-$HOME/.config/gcloud/application_default_credentials.json}"
exec docker run --rm -v "$REPO:/work" -v "$ADC:/creds/adc.json:ro" \
  -e GOOGLE_APPLICATION_CREDENTIALS=/creds/adc.json -e GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT:-}" \
  -e GOOGLE_CLOUD_QUOTA_PROJECT="${GOOGLE_CLOUD_PROJECT:-}" \
  -e XDG_CACHE_HOME=/work/.cache --memory 6g --cpus 4 --pids-limit 512 \
  evaloop-sandbox "$@"
