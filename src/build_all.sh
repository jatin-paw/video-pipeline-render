#!/usr/bin/env bash
# Render + upload every script file passed as an argument.
set -euo pipefail
for f in "$@"; do
  name=$(basename "$f" .json)
  out="build/$name"; mkdir -p "$out"
  python src/render_voice.py "$f" "$out/audio"
  python src/render_video.py "$f" "$out/audio" "$out/$name.mp4"
  python src/upload_drive.py "$out/$name.mp4" "$name.mp4"
done
