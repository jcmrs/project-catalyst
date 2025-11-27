#!/usr/bin/env bash
# Test script for setup-wizard.sh
# Demonstrates all features without interactive prompts

set -euo pipefail

readonly TEST_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly WIZARD_SCRIPT="${TEST_DIR}/setup-wizard.sh"
readonly TEMP_TEST_DIR="/tmp/catalyst-test-$$"

# Colors for test output
readonly GREEN='\033[32m'
readonly RED='\033[31m'
readonly YELLOW='\033[33m'
readonly CYAN='\033[36m'
readonly RESET='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

#@description Print test result
print_result() {
  local name="$1"
  local passed="$2"

  TESTS_RUN=$((TESTS_RUN + 1))

  if [[ ${passed} -eq 1 ]]; then
    echo -e "${GREEN}✓${RESET} ${name}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
  else
    echo -e "${RED}✗${RESET} ${name}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
  fi
}

#@description Run test and check result
run_test() {
  local test_name="$1"
  local test_cmd="$2"

  echo -e "${CYAN}Testing: ${test_name}${RESET}"

  if eval "${test_cmd}" &>/dev/null; then
    print_result "${test_name}" 1
  else
    print_result "${test_name}" 0
  fi
}

#@description Cleanup test environment
cleanup_tests() {
  if [[ -d "${TEMP_TEST_DIR}" ]]; then
    rm -rf "${TEMP_TEST_DIR}"
  fi
}

#@description Test 1: Bash Syntax Check
test_syntax() {
  echo ""
  echo -e "${CYAN}=== Test 1: Syntax Validation ===${RESET}"

  run_test "Bash syntax is valid" \
    "bash -n '${WIZARD_SCRIPT}'"
}

#@description Test 2: Help Output
test_help() {
  echo ""
  echo -e "${CYAN}=== Test 2: Help and Documentation ===${RESET}"

  run_test "Help flag works" \
    "'${WIZARD_SCRIPT}' --help 2>&1 | grep -q 'Usage'"

  run_test "Help contains examples" \
    "'${WIZARD_SCRIPT}' --help 2>&1 | grep -q 'Examples'"

  run_test "Help shows exit codes" \
    "'${WIZARD_SCRIPT}' --help 2>&1 | grep -q 'Exit Codes'"
}

#@description Test 3: Script Features
test_features() {
  echo ""
  echo -e "${CYAN}=== Test 3: Script Features ===${RESET}"

  # Check for required functions
  run_test "Contains logging functions" \
    "grep -q 'log_info()' '${WIZARD_SCRIPT}'"

  run_test "Contains project detection" \
    "grep -q 'detect_project_type()' '${WIZARD_SCRIPT}'"

  run_test "Contains configuration saving" \
    "grep -q 'save_configuration()' '${WIZARD_SCRIPT}'"

  run_test "Contains error handling" \
    "grep -q 'trap cleanup EXIT' '${WIZARD_SCRIPT}'"

  run_test "Contains color support" \
    "grep -q 'COLOR_GREEN' '${WIZARD_SCRIPT}'"
}

#@description Test 4: Defensive Patterns
test_defensive() {
  echo ""
  echo -e "${CYAN}=== Test 4: Defensive Bash Patterns ===${RESET}"

  run_test "Uses set -euo pipefail" \
    "grep -q 'set -euo pipefail' '${WIZARD_SCRIPT}'"

  run_test "Uses readonly for constants" \
    "grep -q 'readonly SCRIPT_VERSION' '${WIZARD_SCRIPT}'"

  run_test "Quotes all variable expansions" \
    "! grep -E '\$\{[A-Z_]+\}[^\"']' '${WIZARD_SCRIPT}' | grep -qv '#'"

  run_test "Uses proper array syntax" \
    "grep -q '\"\${' '${WIZARD_SCRIPT}'"

  run_test "Safe mkdir implementation" \
    "grep -q 'safe_mkdir()' '${WIZARD_SCRIPT}'"

  run_test "Safe file write implementation" \
    "grep -q 'safe_write_file()' '${WIZARD_SCRIPT}'"
}

#@description Test 5: Project Type Detection
test_detection() {
  echo ""
  echo -e "${CYAN}=== Test 5: Project Type Detection ===${RESET}"

  run_test "Detects Node.js projects" \
    "grep -q 'package.json' '${WIZARD_SCRIPT}'"

  run_test "Detects Python projects" \
    "grep -q 'setup.py' '${WIZARD_SCRIPT}'"

  run_test "Detects Java projects" \
    "grep -q 'pom.xml' '${WIZARD_SCRIPT}'"

  run_test "Detects Rust projects" \
    "grep -q 'Cargo.toml' '${WIZARD_SCRIPT}'"

  run_test "Detects Go projects" \
    "grep -q 'go.mod' '${WIZARD_SCRIPT}'"
}

#@description Test 6: Cross-Platform Compatibility
test_compatibility() {
  echo ""
  echo -e "${CYAN}=== Test 6: Cross-Platform Compatibility ===${RESET}"

  run_test "Handles Linux/macOS path detection" \
    "grep -q 'uname -s' '${WIZARD_SCRIPT}'"

  run_test "Uses portable shebang" \
    "head -1 '${WIZARD_SCRIPT}' | grep -q '#!/usr/bin/env bash'"

  run_test "Handles stat compatibility" \
    "grep -q 'Darwin' '${WIZARD_SCRIPT}'"

  run_test "Safe temporary file handling" \
    "grep -q 'mktemp' '${WIZARD_SCRIPT}' || grep -q 'TEMP_DIR' '${WIZARD_SCRIPT}'"
}

#@description Test 7: Documentation
test_documentation() {
  echo ""
  echo -e "${CYAN}=== Test 7: Documentation ===${RESET}"

  run_test "Has file header comments" \
    "head -5 '${WIZARD_SCRIPT}' | grep -q 'Project Catalyst'"

  run_test "Has usage documentation" \
    "grep -q '#@description' '${WIZARD_SCRIPT}'"

  run_test "Has README documentation" \
    "[[ -f '${TEST_DIR}/SETUP_WIZARD_README.md' ]]"

  run_test "README has usage section" \
    "grep -q '## Usage' '${TEST_DIR}/SETUP_WIZARD_README.md'"
}

#@description Test 8: Error Messages
test_messages() {
  echo ""
  echo -e "${CYAN}=== Test 8: Error and Info Messages ===${RESET}"

  run_test "Has success indicator" \
    "grep -q 'INDICATOR_SUCCESS' '${WIZARD_SCRIPT}'"

  run_test "Has error indicator" \
    "grep -q 'INDICATOR_ERROR' '${WIZARD_SCRIPT}'"

  run_test "Has warning messages" \
    "grep -q 'print_warn' '${WIZARD_SCRIPT}'"

  run_test "Has info messages" \
    "grep -q 'print_info' '${WIZARD_SCRIPT}'"
}

#@description Print test summary
print_summary() {
  echo ""
  echo -e "${CYAN}=== Test Summary ===${RESET}"
  echo "Tests run:    ${TESTS_RUN}"
  echo -e "Tests passed: ${GREEN}${TESTS_PASSED}${RESET}"
  echo -e "Tests failed: ${RED}${TESTS_FAILED}${RESET}"

  if [[ ${TESTS_FAILED} -eq 0 ]]; then
    echo ""
    echo -e "${GREEN}All tests passed! ✓${RESET}"
    return 0
  else
    echo ""
    echo -e "${RED}Some tests failed! ✗${RESET}"
    return 1
  fi
}

#@description Main test runner
main() {
  echo -e "${CYAN}"
  cat <<'EOF'
╔════════════════════════════════════════════════════╗
║   Project Catalyst Setup Wizard - Test Suite      ║
╚════════════════════════════════════════════════════╝
EOF
  echo -e "${RESET}"

  # Verify wizard exists
  if [[ ! -f "${WIZARD_SCRIPT}" ]]; then
    echo -e "${RED}Error: Setup wizard not found at ${WIZARD_SCRIPT}${RESET}"
    exit 1
  fi

  # Run tests
  test_syntax
  test_help
  test_features
  test_defensive
  test_detection
  test_compatibility
  test_documentation
  test_messages

  # Print summary and cleanup
  print_summary
  local result=$?
  cleanup_tests
  exit ${result}
}

# Trap cleanup
trap cleanup_tests EXIT

# Run main
main "$@"
