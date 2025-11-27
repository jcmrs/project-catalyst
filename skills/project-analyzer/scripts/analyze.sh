#!/bin/bash
# analyze.sh - Main orchestration script for project analysis
#
# Purpose: Orchestrate full project analysis workflow
# Usage: ./analyze.sh [project-path]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_PATH="${1:-$(pwd)}"

# Output files
TEMP_DIR=$(mktemp -d)
STRUCTURE_JSON="${TEMP_DIR}/structure.json"
DETECTION_JSON="${TEMP_DIR}/detection.json"

echo "🔍 Analyzing project: ${PROJECT_PATH}"
echo ""

# Step 1: Analyze project structure
echo "Step 1/3: Scanning project structure..."
python3 "${SCRIPT_DIR}/analyze-structure.py" "${PROJECT_PATH}" > "${STRUCTURE_JSON}"

if [ $? -ne 0 ]; then
  echo "❌ Failed to analyze project structure"
  rm -rf "${TEMP_DIR}"
  exit 1
fi

echo "  ✅ Structure scan complete"
echo ""

# Step 2: Detect patterns
echo "Step 2/3: Detecting patterns..."
PATTERNS_YAML="${SCRIPT_DIR}/../assets/detection-patterns.yaml"
python3 "${SCRIPT_DIR}/detect-patterns.py" "${STRUCTURE_JSON}" "${PATTERNS_YAML}" > "${DETECTION_JSON}"

if [ $? -ne 0 ]; then
  echo "❌ Failed to detect patterns"
  rm -rf "${TEMP_DIR}"
  exit 1
fi

echo "  ✅ Pattern detection complete"
echo ""

# Step 3: Generate report
echo "Step 3/3: Generating report..."
echo ""
python3 "${SCRIPT_DIR}/generate-report.py" "${DETECTION_JSON}"

if [ $? -ne 0 ]; then
  echo "❌ Failed to generate report"
  rm -rf "${TEMP_DIR}"
  exit 1
fi

# Cleanup
rm -rf "${TEMP_DIR}"

echo ""
echo "✅ Analysis complete"

exit 0
