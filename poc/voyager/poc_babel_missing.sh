#!/usr/bin/env bash
set -eu
src="${VOYAGER_SRC:-/tmp/voyager-audit}"
cd "$src/voyager/env/mineflayer"
if node -e "require('@babel/core')" 2>/dev/null; then
  echo "NOT REPRODUCED: @babel/core present"
  exit 1
fi
echo "REPRODUCED: @babel/core is missing from the bridge package"
node -e "require('@babel/generator')" 2>/dev/null && {
  echo "generator present (unexpected)"; exit 1;
} || echo "REPRODUCED: @babel/generator is also missing"
