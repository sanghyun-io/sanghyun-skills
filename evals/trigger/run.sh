#!/bin/bash
# Run trigger evals with Harbor (Linux / WSL). Usage:
#   evals/trigger/run.sh <model> <attempts> <job-name> [extra harbor args...]
#   e.g. evals/trigger/run.sh anthropic/claude-sonnet-5-5 1 trig-sonnet-dev
#   baseline: SKILLS_REF=<commit> evals/trigger/run.sh ...
# Needs: harbor, docker, and an Anthropic key in $HARBOR_ANTHROPIC_API_KEY (or set KEY_VAR).
set -euo pipefail
MODEL=$1; ATTEMPTS=$2; JOB=$3; shift 3
REPO=$(cd "$(dirname "$0")/../.." && pwd)
WORK=${WORK:-$HOME/sh-skills-eval}
KEY_VAR=${KEY_VAR:-HARBOR_ANTHROPIC_API_KEY}
[ -n "${!KEY_VAR:-}" ] || { echo "missing \$$KEY_VAR" >&2; exit 3; }

rm -rf "$WORK/skills" "$WORK/tasks" "$WORK/src"; mkdir -p "$WORK/skills" "$WORK/src"
# SKILLS_REF=<git ref> measures the skills as they were at that commit (baseline comparison).
if [ -n "${SKILLS_REF:-}" ]; then git -c safe.directory="$REPO" -C "$REPO" archive "$SKILLS_REF" plugins | tar -x -C "$WORK/src"; SRC="$WORK/src"; else SRC="$REPO"; fi
for d in "$SRC"/plugins/*/skills/*/; do cp -r "$d" "$WORK/skills/"; done   # all skills compete
python3 "$REPO/evals/trigger/build_tasks.py" "$WORK/tasks"

harbor run -p "$WORK/tasks" --skill "$WORK/skills" \
  -a claude-code -m "$MODEL" --api-key-name "$KEY_VAR" \
  --ak max_turns=3 --disable-verification \
  -k "$ATTEMPTS" -n "${N_CONCURRENT:-6}" \
  --jobs-dir "$WORK/jobs" --job-name "$JOB" --no-stream --yes "$@"
python3 "$REPO/evals/trigger/score.py" "$WORK/jobs/$JOB"
