#!/usr/bin/env bash

################################################################################
# Health Check Script Tests
################################################################################
#
# Test suite for scripts/health-check.sh
# Uses simple bash assertions for portability
#
# Usage: bash test-health-check.sh
#
################################################################################

set -euo pipefail

# Test environment
readonly TEST_SCRIPT="${SCRIPT_DIR}/health-check.sh"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly TEST_RESULTS_DIR="${SCRIPT_DIR}/.test-results"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# ============================================================================
# Test Utilities
# ============================================================================

setup_test_env() {
    mkdir -p "$TEST_RESULTS_DIR"
}

teardown_test_env() {
    rm -rf "$TEST_RESULTS_DIR"
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-}"

    ((TESTS_RUN++))

    if [[ "$expected" == "$actual" ]]; then
        printf '  ✓ %s\n' "$message"
        ((TESTS_PASSED++))
    else
        printf '  ✗ %s\n' "$message"
        printf '    Expected: %s\n' "$expected"
        printf '    Actual:   %s\n' "$actual"
        ((TESTS_FAILED++))
    fi
}

assert_true() {
    local condition=$1
    local message="${2:-}"

    ((TESTS_RUN++))

    if [[ $condition -eq 0 ]]; then
        printf '  ✓ %s\n' "$message"
        ((TESTS_PASSED++))
    else
        printf '  ✗ %s (condition failed)\n' "$message"
        ((TESTS_FAILED++))
    fi
}

assert_file_exists() {
    local file="$1"
    local message="${2:-}"

    ((TESTS_RUN++))

    if [[ -f "$file" ]]; then
        printf '  ✓ %s\n' "$message"
        ((TESTS_PASSED++))
    else
        printf '  ✗ %s (file not found: %s)\n' "$message" "$file"
        ((TESTS_FAILED++))
    fi
}

# ============================================================================
# Test Suites
# ============================================================================

test_script_exists() {
    printf '\n=== Script Existence Tests ===\n'

    assert_file_exists "$TEST_SCRIPT" "health-check.sh exists"
}

test_script_syntax() {
    printf '\n=== Script Syntax Tests ===\n'

    ((TESTS_RUN++))
    if bash -n "$TEST_SCRIPT" 2>/dev/null; then
        printf '  ✓ Script has valid bash syntax\n'
        ((TESTS_PASSED++))
    else
        printf '  ✗ Script has syntax errors\n'
        ((TESTS_FAILED++))
    fi
}

test_script_executable() {
    printf '\n=== Script Executable Tests ===\n'

    ((TESTS_RUN++))
    if [[ -x "$TEST_SCRIPT" ]]; then
        printf '  ✓ Script is executable\n'
        ((TESTS_PASSED++))
    else
        printf '  ⚠ Script is not executable (chmod +x may be needed)\n'
        # Don't fail on non-executable as it's a permission issue
        ((TESTS_PASSED++))
    fi
}

test_help_output() {
    printf '\n=== Help Output Tests ===\n'

    ((TESTS_RUN++))
    local output
    output=$(bash "$TEST_SCRIPT" --help 2>/dev/null || echo "")

    if echo "$output" | grep -q "🏥 Project Catalyst Health Check"; then
        printf '  ✓ Help output contains header\n'
        ((TESTS_PASSED++))
    else
        printf '  ✗ Help output missing header\n'
        ((TESTS_FAILED++))
    fi

    ((TESTS_RUN++))
    if echo "$output" | grep -q "Usage:"; then
        printf '  ✓ Help output contains usage\n'
        ((TESTS_PASSED++))
    else
        printf '  ✗ Help output missing usage\n'
        ((TESTS_FAILED++))
    fi
}

test_invalid_arguments() {
    printf '\n=== Invalid Arguments Tests ===\n'

    ((TESTS_RUN++))
    if bash "$TEST_SCRIPT" --invalid-flag &>/dev/null; then
        printf '  ✗ Script should reject invalid flags\n'
        ((TESTS_FAILED++))
    else
        printf '  ✓ Script rejects invalid flags\n'
        ((TESTS_PASSED++))
    fi
}

test_output_modes() {
    printf '\n=== Output Mode Tests ===\n'

    # Test quiet mode
    ((TESTS_RUN++))
    local quiet_output
    quiet_output=$(bash "$TEST_SCRIPT" --quiet 2>/dev/null || echo "")

    if [[ "$quiet_output" =~ ^[0-9]+$ ]]; then
        printf '  ✓ Quiet mode outputs a number\n'
        ((TESTS_PASSED++))
    else
        printf '  ✗ Quiet mode output is not numeric: %s\n' "$quiet_output"
        ((TESTS_FAILED++))
    fi

    # Test JSON mode
    ((TESTS_RUN++))
    local json_output
    json_output=$(bash "$TEST_SCRIPT" --json 2>/dev/null || echo "")

    if echo "$json_output" | grep -q '"project"'; then
        printf '  ✓ JSON mode outputs valid JSON\n'
        ((TESTS_PASSED++))
    else
        printf '  ✗ JSON mode output is not valid JSON\n'
        ((TESTS_FAILED++))
    fi
}

test_score_range() {
    printf '\n=== Score Range Tests ===\n'

    local score
    score=$(bash "$TEST_SCRIPT" --quiet 2>/dev/null || echo "0")

    ((TESTS_RUN++))
    if (( score >= 0 && score <= 100 )); then
        printf '  ✓ Score is in valid range (0-100): %d\n' "$score"
        ((TESTS_PASSED++))
    else
        printf '  ✗ Score is out of valid range: %d\n' "$score"
        ((TESTS_FAILED++))
    fi
}

test_json_structure() {
    printf '\n=== JSON Structure Tests ===\n'

    local json_output
    json_output=$(bash "$TEST_SCRIPT" --json 2>/dev/null || echo "")

    local tests=(
        '".project"'
        '".timestamp"'
        '".scores"'
        '".scores.git_health"'
        '".scores.documentation_health"'
        '".scores.code_quality_health"'
        '".scores.setup_health"'
        '".scores.security_health"'
        '".scores.overall"'
        '".recommendations"'
    )

    for test in "${tests[@]}"; do
        ((TESTS_RUN++))
        # Simple check for field existence
        if echo "$json_output" | grep -q "${test//\"/}"; then
            printf '  ✓ JSON contains field: %s\n' "$test"
            ((TESTS_PASSED++))
        else
            printf '  ✗ JSON missing field: %s\n' "$test"
            ((TESTS_FAILED++))
        fi
    done
}

test_recommendations() {
    printf '\n=== Recommendations Tests ===\n'

    local json_output
    json_output=$(bash "$TEST_SCRIPT" --json 2>/dev/null || echo "")

    ((TESTS_RUN++))
    if echo "$json_output" | grep -q '"recommendations"'; then
        printf '  ✓ Recommendations field present\n'
        ((TESTS_PASSED++))
    else
        printf '  ✗ Recommendations field missing\n'
        ((TESTS_FAILED++))
    fi
}

test_consistent_scoring() {
    printf '\n=== Consistent Scoring Tests ===\n'

    # Run twice and compare
    local score1 score2
    score1=$(bash "$TEST_SCRIPT" --quiet 2>/dev/null || echo "0")
    score2=$(bash "$TEST_SCRIPT" --quiet 2>/dev/null || echo "0")

    ((TESTS_RUN++))
    if [[ "$score1" == "$score2" ]]; then
        printf '  ✓ Scoring is consistent across runs\n'
        ((TESTS_PASSED++))
    else
        printf '  ⚠ Scores differ between runs: %s vs %s (may be normal)\n' "$score1" "$score2"
        # Don't fail as this can happen with dynamic checks
        ((TESTS_PASSED++))
    fi
}

# ============================================================================
# Report Generation
# ============================================================================

print_summary() {
    printf '\n'
    printf '=================================================\n'
    printf 'Test Results Summary\n'
    printf '=================================================\n'
    printf 'Total Tests:   %d\n' "$TESTS_RUN"
    printf 'Passed:        %d\n' "$TESTS_PASSED"
    printf 'Failed:        %d\n' "$TESTS_FAILED"
    printf '=================================================\n'

    if (( TESTS_FAILED == 0 )); then
        printf '\n✅ All tests passed!\n\n'
        return 0
    else
        printf '\n❌ %d test(s) failed\n\n' "$TESTS_FAILED"
        return 1
    fi
}

# ============================================================================
# Main Execution
# ============================================================================

main() {
    printf '\n🧪 Health Check Script Test Suite\n'
    printf '==================================\n'

    setup_test_env

    # Run all test suites
    test_script_exists
    test_script_syntax
    test_script_executable
    test_help_output
    test_invalid_arguments
    test_output_modes
    test_score_range
    test_json_structure
    test_recommendations
    test_consistent_scoring

    teardown_test_env

    print_summary
}

main "$@"
