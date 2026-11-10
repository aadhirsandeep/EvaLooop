# Run a command inside the evaloop-sandbox container (Windows host, Docker Desktop).
# Only the repository and the Google ADC file (read-only) are mounted.
#   .\scripts\sandbox.ps1 python -m evaloop evaluate --model vertex/google/gemini-3.1-flash-lite ...
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Cmd)
$repo = (Resolve-Path "$PSScriptRoot\..").Path
$adc = "$env:APPDATA\gcloud\application_default_credentials.json"
docker run --rm `
  -v "${repo}:/work" `
  -v "${adc}:/creds/adc.json:ro" `
  -e GOOGLE_APPLICATION_CREDENTIALS=/creds/adc.json `
  -e GOOGLE_CLOUD_PROJECT=$env:GOOGLE_CLOUD_PROJECT `
  -e GOOGLE_CLOUD_QUOTA_PROJECT=$env:GOOGLE_CLOUD_PROJECT `
  -e XDG_CACHE_HOME=/work/.cache `
  --memory 6g --cpus 4 --pids-limit 512 `
  evaloop-sandbox @Cmd
