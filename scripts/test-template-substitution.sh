#!/bin/bash
# test-template-substitution.sh - Test template variable substitution
#
# Purpose: Verify that template variables can be properly substituted
# Usage: ./scripts/test-template-substitution.sh

set -e

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(readlink -f "$0")")")}"

echo "🧪 Testing template variable substitution..."

# Test function
test_substitution() {
  local template=$1
  local test_name=$2

  echo "  → Testing $(basename "${template}")..."

  # Extract variables from template
  variables=$(grep -A 100 "^variables:" "${template}" | sed -n '/^  - name:/p' | sed 's/.*name: //' || true)

  if [ -z "${variables}" ]; then
    echo "    ✅ No variables (static template)"
    return 0
  fi

  # Create test substitution
  local content=$(cat "${template}")

  for var in ${variables}; do
    # Substitute with test value
    content=$(echo "${content}" | sed "s/\${${var}}/TEST_${var}/g")
  done

  # Check if any variables remain unsubstituted
  if echo "${content}" | grep -q '\${[A-Z_][A-Z0-9_]*}'; then
    echo "    ❌ Failed: Some variables not substituted"
    echo "${content}" | grep -o '\${[A-Z_][A-Z0-9_]*}' | sort -u | sed 's/^/       Remaining: /'
    return 1
  else
    echo "    ✅ All variables substituted successfully"
    return 0
  fi
}

# Test all templates
failures=0

for template in $(find "${PLUGIN_ROOT}/templates" -type f); do
  if ! test_substitution "${template}" "$(basename "${template}")"; then
    failures=$((failures + 1))
  fi
done

# Report results
echo ""
if [ ${failures} -eq 0 ]; then
  echo "✅ All template substitution tests passed"
  exit 0
else
  echo "🚨 ${failures} template substitution test(s) failed"
  exit 1
fi
