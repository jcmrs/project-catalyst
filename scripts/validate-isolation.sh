#!/bin/bash
# validate-isolation.sh - Verify isolation enforcement
#
# Hook: PreCommit
# Triggered: Before git commits
# Purpose: Ensure all local-memory operations include mandatory isolation parameters
#
# CRITICAL: 100% isolation coverage is non-negotiable

set -e

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(readlink -f "$0")")")}"

echo "🔍 Validating isolation enforcement..."

# Check Skills for proper isolation
check_skills_isolation() {
  local violations=0

  if [ -d "${PLUGIN_ROOT}/skills" ]; then
    # Check for store_memory calls without session_filter_mode
    while IFS= read -r file; do
      if grep -q "store_memory" "${file}" && ! grep -q "session_filter_mode.*session_only" "${file}"; then
        echo "❌ ISOLATION VIOLATION in ${file}"
        echo "   store_memory call missing session_filter_mode: 'session_only'"
        violations=$((violations + 1))
      fi

      # Check for search calls without session_filter_mode
      if grep -q "mcp__local-memory__search" "${file}" && ! grep -q "session_filter_mode.*session_only" "${file}"; then
        echo "❌ ISOLATION VIOLATION in ${file}"
        echo "   search call missing session_filter_mode: 'session_only'"
        violations=$((violations + 1))
      fi
    done < <(find "${PLUGIN_ROOT}/skills" -type f -name "*.md" -o -name "*.js" -o -name "*.py")
  fi

  return ${violations}
}

# Check scripts for proper isolation
check_scripts_isolation() {
  local violations=0

  if [ -d "${PLUGIN_ROOT}/scripts" ]; then
    while IFS= read -r file; do
      if grep -q "store_memory\|mcp__local-memory__search" "${file}" && ! grep -q "session_filter_mode" "${file}"; then
        echo "❌ ISOLATION VIOLATION in ${file}"
        echo "   local-memory operation missing isolation parameters"
        violations=$((violations + 1))
      fi
    done < <(find "${PLUGIN_ROOT}/scripts" -type f \( -name "*.js" -o -name "*.py" -o -name "*.sh" \))
  fi

  return ${violations}
}

# Run checks
violations=0

check_skills_isolation || violations=$((violations + $?))
check_scripts_isolation || violations=$((violations + $?))

# Report results
if [ ${violations} -eq 0 ]; then
  echo "✅ All local-memory operations properly isolated (${violations} violations)"
  exit 0
else
  echo ""
  echo "🚨 ISOLATION VALIDATION FAILED"
  echo "   ${violations} violation(s) found"
  echo ""
  echo "   CRITICAL: All local-memory operations MUST include:"
  echo "   - session_filter_mode: 'session_only'"
  echo "   - session_id: getProjectSessionId()"
  echo ""
  echo "   See: scripts/lib/session-utils.js for helper functions"
  exit 1
fi
