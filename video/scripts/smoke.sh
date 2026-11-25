#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
npx remotion render src/index.ts Smoke out/smoke.mp4 --log=error
ffprobe -v error -select_streams v:0 -show_entries stream=width,height:format=duration -of csv=p=0 out/smoke.mp4
