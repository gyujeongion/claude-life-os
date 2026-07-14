#!/usr/bin/env bash
# First-run setup: create your private live data files from the tracked *.example seeds.
#
# The template ships every personal file as `<name>.example` (tracked, updatable). This
# copies each to `<name>` (git-ignored, yours) — but only if the live file doesn't exist
# yet, so re-running it never clobbers your data. Safe to run any time.
#
#   bash tools/bootstrap.sh
set -euo pipefail
cd "$(dirname "$0")/.."

created=0
skipped=0
while IFS= read -r seed; do
    live="${seed%.example}"
    if [ -e "$live" ]; then
        skipped=$((skipped + 1))
    else
        cp "$seed" "$live"
        echo "  created  $live"
        created=$((created + 1))
    fi
done < <(find . -name '*.example' -not -path './.git/*')

echo ""
echo "Bootstrap done: $created created, $skipped already existed."
if [ "$created" -gt 0 ]; then
    echo "These live files are git-ignored — your data stays private. Fill them in, or run"
    echo "onboarding: open Claude Code here and say \"Set this up for me\"."
fi
