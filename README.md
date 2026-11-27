# claude-video-pipeline

1. Claude (in a Claude Code session) writes a script → `scripts/<name>.json`, commits and pushes.
2. GitHub Actions detects the push, voices each scene (edge-tts), renders the mp4 (ffmpeg), uploads to Google Drive.

No Anthropic API key needed. Script format: see `scripts/example.json`.
Manual run: Actions → *Render and upload videos* → Run workflow → script path.

## Secrets (repo → Settings → Secrets → Actions)
- `GDRIVE_SERVICE_ACCOUNT_JSON` – service-account key JSON (a plain API key can't upload to Drive)
- `GDRIVE_FOLDER_ID` – Drive folder shared with the service account's email as Editor
