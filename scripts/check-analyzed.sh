#!/bin/bash
# check-analyzed.sh - Check if project has been analyzed
#
# Hook: SessionStart
# Triggered: When Claude Code session starts
# Purpose: Suggest running analyzer for new projects

set -e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CATALYST_DIR="${PROJECT_DIR}/.catalyst"
ANALYZED_FLAG="${CATALYST_DIR}/analyzed"

# Check if .catalyst directory exists
if [ ! -d "${CATALYST_DIR}" ]; then
  echo "💡 New project detected. Run /analyze-project to get recommendations"
  exit 0
fi

# Check if analysis has been run
if [ ! -f "${ANALYZED_FLAG}" ]; then
  echo "💡 Project not yet analyzed. Run /analyze-project for recommendations"
  exit 0
fi

# Check if analysis is stale (older than 7 days)
if [ -f "${ANALYZED_FLAG}" ]; then
  LAST_ANALYZED=$(stat -c %Y "${ANALYZED_FLAG}" 2>/dev/null || stat -f %m "${ANALYZED_FLAG}" 2>/dev/null || echo 0)
  NOW=$(date +%s)
  DAYS_AGO=$(( (NOW - LAST_ANALYZED) / 86400 ))

  if [ "${DAYS_AGO}" -gt 7 ]; then
    echo "💡 Project analysis is ${DAYS_AGO} days old. Consider re-analyzing: /analyze-project"
  fi
fi

exit 0
