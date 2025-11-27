#!/bin/bash
# validate-template.sh - Validate template files after writing
#
# Hook: PostToolUse (Write)
# Triggered: After files are written
# Purpose: Ensure template variables are properly substituted

set -e

FILE_PATH="${1:-}"

if [ -z "${FILE_PATH}" ]; then
  echo "⚠️  No file path provided to validate-template.sh"
  exit 0
fi

# Only validate files in known template target locations
case "${FILE_PATH}" in
  *.md|*.json|*.yaml|*.yml|*.toml|*.ini|*.conf|*.config)
    # Check for unsubstituted template variables
    if grep -q '\${[A-Z_][A-Z0-9_]*}' "${FILE_PATH}" 2>/dev/null; then
      echo "⚠️  Warning: Unsubstituted template variables found in ${FILE_PATH}"
      echo "   Run /apply-template to properly substitute variables"
    fi
    ;;
  *)
    # Not a template file type, skip validation
    exit 0
    ;;
esac

exit 0
