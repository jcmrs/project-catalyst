#!/bin/bash
# validate-template-format.sh - Validate template file format
#
# Purpose: Ensure all templates follow the standard format with YAML frontmatter
# Usage: ./scripts/validate-template-format.sh [template-file]

set -e

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(readlink -f "$0")")")}"
TEMPLATE_FILE="${1:-}"

# Validate single template or all templates
if [ -z "${TEMPLATE_FILE}" ]; then
  echo "🔍 Validating all templates..."
  TEMPLATES=$(find "${PLUGIN_ROOT}/templates" -type f)
else
  TEMPLATES="${TEMPLATE_FILE}"
fi

violations=0

for template in ${TEMPLATES}; do
  # Skip if not a file
  [ -f "${template}" ] || continue

  echo "  → Checking $(basename "${template}")..."

  # Check for YAML frontmatter
  if ! head -n 1 "${template}" | grep -q '^---$'; then
    echo "    ❌ Missing YAML frontmatter opening (---)"
    violations=$((violations + 1))
    continue
  fi

  # Check for required fields in frontmatter
  required_fields=("id" "version" "category" "description" "language")

  for field in "${required_fields[@]}"; do
    if ! grep -q "^${field}:" "${template}"; then
      echo "    ❌ Missing required field: ${field}"
      violations=$((violations + 1))
    fi
  done

  # Check for frontmatter closing (within first 50 lines)
  if ! sed -n '2,50p' "${template}" | grep -q '^---$'; then
    echo "    ❌ Missing YAML frontmatter closing (---)"
    violations=$((violations + 1))
    continue
  fi

  echo "    ✅ Format valid"
done

# Report results
if [ ${violations} -eq 0 ]; then
  echo ""
  echo "✅ All templates pass format validation"
  exit 0
else
  echo ""
  echo "🚨 Template format validation failed"
  echo "   ${violations} violation(s) found"
  echo ""
  echo "   Required format:"
  echo "   ---"
  echo "   id: template-id"
  echo "   version: 1.0.0"
  echo "   category: git|documentation|ci-cd|setup|quality"
  echo "   description: Clear description"
  echo "   language: markdown|yaml|bash|etc"
  echo "   dependencies: []"
  echo "   variables: []"
  echo "   ---"
  echo "   "
  echo "   Template content here"
  exit 1
fi
