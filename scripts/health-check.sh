#!/usr/bin/env bash

################################################################################
# Project Catalyst Health Check Script
################################################################################
#
# Purpose:  Quick project health assessment (30-60 seconds max)
# Location: scripts/health-check.sh
# Compat:   Windows Git Bash, macOS, Linux
#
# Usage:    ./scripts/health-check.sh [OPTIONS]
# Options:  --json       Output in JSON format
#           --verbose    Show detailed breakdown
#           --quiet      Only output score
#           --help       Display help message
#
# Exit Codes:
#   0   Success
#   1   General error
#   2   Invalid arguments
#   3   Critical errors detected
#
################################################################################

set -euo pipefail

# Bash version check for modern features
if (( BASH_VERSINFO[0] < 4 )) || (( BASH_VERSINFO[0] == 4 && BASH_VERSINFO[1] < 4 )); then
    printf 'Error: Bash 4.4+ required (found %s.%s)\n' \
        "${BASH_VERSINFO[0]}" "${BASH_VERSINFO[1]}" >&2
    exit 1
fi

shopt -s inherit_errexit 2>/dev/null || true

# ============================================================================
# Constants & Configuration
# ============================================================================

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"

# Score thresholds
readonly SCORE_EXCELLENT=90
readonly SCORE_GOOD=70
readonly SCORE_NEEDS_IMPROVEMENT=50
readonly SCORE_POOR=30

# Max points per category
declare -r MAX_GIT=25
declare -r MAX_DOCS=20
declare -r MAX_QUALITY=25
declare -r MAX_SETUP=15
declare -r MAX_SECURITY=15
declare -r TOTAL_MAX=$((MAX_GIT + MAX_DOCS + MAX_QUALITY + MAX_SETUP + MAX_SECURITY))

# Output formatting
readonly COLOR_RED='\033[0;31m'
readonly COLOR_YELLOW='\033[1;33m'
readonly COLOR_GREEN='\033[0;32m'
readonly COLOR_BLUE='\033[0;34m'
readonly COLOR_RESET='\033[0m'

# Platform detection
readonly UNAME_S="$(uname -s 2>/dev/null || echo 'UNKNOWN')"

# ============================================================================
# Mode flags (set via command line)
# ============================================================================

MODE_JSON=0
MODE_VERBOSE=0
MODE_QUIET=0

# ============================================================================
# Scoring variables
# ============================================================================

GIT_SCORE=0
DOCS_SCORE=0
QUALITY_SCORE=0
SETUP_SCORE=0
SECURITY_SCORE=0
OVERALL_SCORE=0

# Recommendation buffer
declare -a RECOMMENDATIONS=()
declare -i RECOMMENDATION_COUNT=0

# ============================================================================
# Utility Functions
# ============================================================================

# Print to stderr (for logging, doesn't affect JSON output)
log_debug() {
    (( MODE_VERBOSE )) && printf '[DEBUG] %s\n' "$*" >&2
}

log_error() {
    printf '[ERROR] %s\n' "$*" >&2
}

# Color output (disabled for JSON mode)
colorize() {
    local color="$1"
    local text="$2"

    if (( MODE_JSON )); then
        printf '%s' "$text"
    else
        printf '%s%s%s' "$color" "$text" "$COLOR_RESET"
    fi
}

# Safe file check
file_exists() {
    [[ -f "$1" ]] && return 0 || return 1
}

# Safe directory check
dir_exists() {
    [[ -d "$1" ]] && return 0 || return 1
}

# Count lines in file (safely)
count_file_lines() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        echo "0"
        return 0
    fi

    # Use POSIX-compatible line counting
    local line_count
    line_count=$(wc -l < "$file" 2>/dev/null || echo "0")

    # Remove leading/trailing whitespace
    echo "${line_count##*( )}"
}

# Check if file has content (not empty)
file_not_empty() {
    [[ -s "$1" ]] && return 0 || return 1
}

# Safe grep check (returns true if pattern found)
grep_exists() {
    local pattern="$1"
    local file="$2"

    grep -q "$pattern" "$file" 2>/dev/null && return 0 || return 1
}

# Safe find (handles special characters)
find_files() {
    local pattern="$1"
    local path="${2:-.}"
    local depth="${3:--1}"

    if [[ "$depth" -eq -1 ]]; then
        find "$path" -name "$pattern" -type f 2>/dev/null | head -5
    else
        find "$path" -maxdepth "$depth" -name "$pattern" -type f 2>/dev/null | head -5
    fi
}

# Add recommendation (deduplicated)
add_recommendation() {
    local rec="$1"
    local i

    # Check if already added
    for i in "${RECOMMENDATIONS[@]}"; do
        [[ "$i" == "$rec" ]] && return 0
    done

    RECOMMENDATIONS+=("$rec")
    ((RECOMMENDATION_COUNT++))
}

# Display help
show_help() {
    cat <<'HELP_TEXT'
🏥 Project Catalyst Health Check

Usage: ./scripts/health-check.sh [OPTIONS]

Options:
  --json      Output results in JSON format (for automation)
  --verbose   Show detailed breakdown of each check
  --quiet     Only output final score
  --help      Display this help message

Examples:
  # Standard output with detailed report
  ./scripts/health-check.sh

  # JSON output for CI/CD integration
  ./scripts/health-check.sh --json

  # Verbose mode with all checks detailed
  ./scripts/health-check.sh --verbose

  # Minimal output (just the score)
  ./scripts/health-check.sh --quiet

Exit Codes:
  0   Success
  1   General error
  2   Invalid arguments
  3   Critical errors detected

HELP_TEXT
}

# Parse command line arguments
parse_arguments() {
    while (( $# > 0 )); do
        case "$1" in
            --json)
                MODE_JSON=1
                ;;
            --verbose)
                MODE_VERBOSE=1
                ;;
            --quiet)
                MODE_QUIET=1
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                printf 'Error: Unknown option: %s\n' "$1" >&2
                printf 'Use --help for usage information\n' >&2
                exit 2
                ;;
        esac
        shift
    done
}

# ============================================================================
# Check Functions (organized by category)
# ============================================================================

# GIT HEALTH CHECKS
check_git_gitignore() {
    local gitignore_file="${PROJECT_ROOT}/.gitignore"
    local points=0

    log_debug "Checking .gitignore..."

    if file_exists "$gitignore_file" && file_not_empty "$gitignore_file"; then
        local line_count
        line_count=$(count_file_lines "$gitignore_file")

        if (( line_count > 0 )); then
            points=10
            (( MODE_VERBOSE )) && printf '  ✓ .gitignore present with %d patterns\n' "$line_count" >&2
        else
            add_recommendation "Populate .gitignore with common patterns"
        fi
    else
        add_recommendation "Create and populate .gitignore file"
    fi

    echo "$points"
}

check_git_hooks() {
    local hooks_dir="${PROJECT_ROOT}/.git/hooks"
    local points=0

    log_debug "Checking Git hooks..."

    if dir_exists "$hooks_dir"; then
        # Count hook files (exclude *.sample files)
        local hook_count
        hook_count=$(find_files '[!.]*' "$hooks_dir" 1 | wc -l 2>/dev/null || echo 0)

        if (( hook_count > 0 )); then
            points=5
            (( MODE_VERBOSE )) && printf '  ✓ Git hooks configured (%d hooks)\n' "$hook_count" >&2
        else
            add_recommendation "Configure pre-commit/pre-push Git hooks"
        fi
    else
        add_recommendation "Set up Git hooks for code quality checks"
    fi

    echo "$points"
}

check_git_cicd() {
    local ci_files=(
        "${PROJECT_ROOT}/.github/workflows"
        "${PROJECT_ROOT}/.gitlab-ci.yml"
        "${PROJECT_ROOT}/.circleci/config.yml"
        "${PROJECT_ROOT}/.travis.yml"
        "${PROJECT_ROOT}/.github/workflows/test.yml"
        "${PROJECT_ROOT}/.github/workflows/ci.yml"
    )

    local points=0

    log_debug "Checking CI/CD configuration..."

    for file in "${ci_files[@]}"; do
        if [[ -d "$file" ]] || [[ -f "$file" ]]; then
            points=10
            local basename
            basename=$(basename "${file%/*}" 2>/dev/null || basename "$file" 2>/dev/null)
            (( MODE_VERBOSE )) && printf '  ✓ CI/CD configured (%s)\n' "$basename" >&2
            break
        fi
    done

    if (( points == 0 )); then
        add_recommendation "Configure GitHub Actions or other CI/CD pipeline"
    fi

    echo "$points"
}

# DOCUMENTATION HEALTH CHECKS
check_docs_readme() {
    local readme_file="${PROJECT_ROOT}/README.md"
    local points=0

    log_debug "Checking README.md..."

    if file_exists "$readme_file"; then
        local line_count
        line_count=$(count_file_lines "$readme_file")

        if (( line_count >= 100 )); then
            points=10
            (( MODE_VERBOSE )) && printf '  ✓ README.md present (%d lines)\n' "$line_count" >&2
        else
            (( MODE_VERBOSE )) && printf '  ⚠ README.md exists but is short (%d lines)\n' "$line_count" >&2
            add_recommendation "Enhance README.md (currently $line_count lines, needs 100+)"
        fi
    else
        add_recommendation "Create comprehensive README.md documentation"
    fi

    echo "$points"
}

check_docs_contributing() {
    local contrib_file="${PROJECT_ROOT}/CONTRIBUTING.md"
    local points=0

    log_debug "Checking CONTRIBUTING.md..."

    if file_exists "$contrib_file"; then
        points=5
        (( MODE_VERBOSE )) && printf '  ✓ CONTRIBUTING.md present\n' >&2
    else
        add_recommendation "Create CONTRIBUTING.md for contributor guidelines"
    fi

    echo "$points"
}

check_docs_license() {
    local license_file="${PROJECT_ROOT}/LICENSE"
    local license_files=(
        "${PROJECT_ROOT}/LICENSE"
        "${PROJECT_ROOT}/LICENSE.txt"
        "${PROJECT_ROOT}/LICENSE.md"
    )

    local points=0

    log_debug "Checking LICENSE file..."

    for lfile in "${license_files[@]}"; do
        if file_exists "$lfile"; then
            points=5
            (( MODE_VERBOSE )) && printf '  ✓ LICENSE file present\n' >&2
            break
        fi
    done

    if (( points == 0 )); then
        add_recommendation "Add LICENSE file to the repository"
    fi

    echo "$points"
}

# CODE QUALITY CHECKS
check_quality_linter() {
    local linter_configs=(
        "${PROJECT_ROOT}/.eslintrc"
        "${PROJECT_ROOT}/.eslintrc.json"
        "${PROJECT_ROOT}/.eslintrc.js"
        "${PROJECT_ROOT}/.pylintrc"
        "${PROJECT_ROOT}/pylintrc"
        "${PROJECT_ROOT}/.flake8"
        "${PROJECT_ROOT}/setup.cfg"
        "${PROJECT_ROOT}/.shellcheckrc"
    )

    local points=0

    log_debug "Checking linter configuration..."

    for config in "${linter_configs[@]}"; do
        if file_exists "$config"; then
            points=10
            local basename
            basename=$(basename "$config")
            (( MODE_VERBOSE )) && printf '  ✓ Linter config found (%s)\n' "$basename" >&2
            break
        fi
    done

    if (( points == 0 )); then
        add_recommendation "Configure linter (ESLint, Pylint, Flake8, etc.)"
    fi

    echo "$points"
}

check_quality_formatter() {
    local formatter_configs=(
        "${PROJECT_ROOT}/.prettierrc"
        "${PROJECT_ROOT}/.prettierrc.json"
        "${PROJECT_ROOT}/prettier.config.js"
        "${PROJECT_ROOT}/.black"
        "${PROJECT_ROOT}/pyproject.toml"
    )

    local points=0

    log_debug "Checking formatter configuration..."

    for config in "${formatter_configs[@]}"; do
        if file_exists "$config"; then
            # Check if pyproject.toml actually has formatter config
            if [[ "$config" == *"pyproject.toml" ]]; then
                if grep_exists "tool\\.black\\|tool\\.autopep8" "$config"; then
                    points=5
                    (( MODE_VERBOSE )) && printf '  ✓ Formatter config found (%s)\n' "$(basename "$config")" >&2
                    break
                fi
            else
                points=5
                (( MODE_VERBOSE )) && printf '  ✓ Formatter config found (%s)\n' "$(basename "$config")" >&2
                break
            fi
        fi
    done

    if (( points == 0 )); then
        add_recommendation "Configure code formatter (Prettier, Black, etc.)"
    fi

    echo "$points"
}

check_quality_tests() {
    local test_dirs=(
        "${PROJECT_ROOT}/tests"
        "${PROJECT_ROOT}/test"
        "${PROJECT_ROOT}/__tests__"
        "${PROJECT_ROOT}/spec"
    )

    local points=0

    log_debug "Checking test directory..."

    for test_dir in "${test_dirs[@]}"; do
        if dir_exists "$test_dir"; then
            # Count test files
            local test_count
            test_count=$(find_files '*.py\|*.js\|*.ts\|*.sh\|*_test.*\|*test.*' "$test_dir" 1 | wc -l 2>/dev/null || echo 0)

            if (( test_count > 0 )); then
                points=10
                (( MODE_VERBOSE )) && printf '  ✓ Test directory with %d test files\n' "$test_count" >&2
                break
            else
                (( MODE_VERBOSE )) && printf '  ⚠ Test directory exists but appears empty\n' >&2
            fi
        fi
    done

    if (( points == 0 )); then
        add_recommendation "Create test directory with test cases"
    fi

    echo "$points"
}

# SETUP HEALTH CHECKS
check_setup_editorconfig() {
    local editorconfig_file="${PROJECT_ROOT}/.editorconfig"
    local points=0

    log_debug "Checking .editorconfig..."

    if file_exists "$editorconfig_file"; then
        points=5
        (( MODE_VERBOSE )) && printf '  ✓ .editorconfig present\n' >&2
    else
        add_recommendation "Add .editorconfig for consistent code style"
    fi

    echo "$points"
}

check_setup_package_files() {
    local pkg_files=(
        "${PROJECT_ROOT}/package.json"
        "${PROJECT_ROOT}/requirements.txt"
        "${PROJECT_ROOT}/setup.py"
        "${PROJECT_ROOT}/Gemfile"
        "${PROJECT_ROOT}/Cargo.toml"
        "${PROJECT_ROOT}/go.mod"
    )

    local points=0

    log_debug "Checking package manager files..."

    for pkg_file in "${pkg_files[@]}"; do
        if file_exists "$pkg_file" && file_not_empty "$pkg_file"; then
            # Basic validation - check for key patterns
            local basename
            basename=$(basename "$pkg_file")

            case "$basename" in
                package.json)
                    if grep_exists '"name"' "$pkg_file"; then
                        points=10
                        (( MODE_VERBOSE )) && printf '  ✓ package.json valid\n' >&2
                        break
                    fi
                    ;;
                requirements.txt)
                    points=10
                    (( MODE_VERBOSE )) && printf '  ✓ requirements.txt present\n' >&2
                    break
                    ;;
                *)
                    points=10
                    (( MODE_VERBOSE )) && printf '  ✓ Package file found (%s)\n' "$basename" >&2
                    break
                    ;;
            esac
        fi
    done

    if (( points == 0 )); then
        add_recommendation "Set up package manager files (package.json, requirements.txt, etc.)"
    fi

    echo "$points"
}

# SECURITY HEALTH CHECKS
check_security_env_in_git() {
    local env_files="${PROJECT_ROOT}/.env"
    local points=10

    log_debug "Checking for .env files in Git..."

    if file_exists "$env_files"; then
        # Check if .env is in git using git check-ignore (safer, no cd needed)
        if (cd "$PROJECT_ROOT" && git check-ignore "$env_files" &>/dev/null); then
            (( MODE_VERBOSE )) && printf '  ✓ .env properly ignored\n' >&2
        else
            # If not ignored, it might be tracked - give warning
            points=5
            add_recommendation "Ensure .env is in .gitignore"
            (( MODE_VERBOSE )) && printf '  ⚠ .env file exists but may not be properly ignored\n' >&2
        fi
    else
        (( MODE_VERBOSE )) && printf '  ✓ No .env files detected\n' >&2
    fi

    echo "$points"
}

check_security_hardcoded_secrets() {
    local secret_patterns=(
        'PRIVATE_KEY='
        'api_key='
        'password='
        'secret='
        'token='
        'AWS_ACCESS_KEY'
        'firebase_key'
    )

    local points=10
    local found_secrets=0

    log_debug "Checking for hardcoded secrets..."

    # Only scan common config files (not entire project)
    local config_files=(
        "${PROJECT_ROOT}/.env.example"
        "${PROJECT_ROOT}/config.js"
        "${PROJECT_ROOT}/config.py"
        "${PROJECT_ROOT}/settings.json"
    )

    for config_file in "${config_files[@]}"; do
        [[ ! -f "$config_file" ]] && continue

        for pattern in "${secret_patterns[@]}"; do
            if grep_exists "$pattern" "$config_file"; then
                if ! grep_exists "example\|placeholder\|XXXX\|changeme" "$config_file"; then
                    found_secrets=1
                    break
                fi
            fi
        done

        [[ $found_secrets -eq 1 ]] && break
    done

    if (( found_secrets == 1 )); then
        points=0
        add_recommendation "Remove hardcoded secrets from source files"
        (( MODE_VERBOSE )) && printf '  ❌ Potential hardcoded secrets detected\n' >&2
    else
        (( MODE_VERBOSE )) && printf '  ✓ No obvious hardcoded secrets found\n' >&2
    fi

    echo "$points"
}

# ============================================================================
# Score Assessment Functions
# ============================================================================

get_status_symbol() {
    local score=$1

    if (( score >= SCORE_EXCELLENT )); then
        echo "✅"
    elif (( score >= SCORE_GOOD )); then
        echo "✅"
    elif (( score >= SCORE_NEEDS_IMPROVEMENT )); then
        echo "⚠️"
    else
        echo "❌"
    fi
}

get_status_label() {
    local score=$1

    if (( score >= SCORE_EXCELLENT )); then
        echo "Excellent"
    elif (( score >= SCORE_GOOD )); then
        echo "Good"
    elif (( score >= SCORE_NEEDS_IMPROVEMENT )); then
        echo "Needs Improvement"
    elif (( score >= SCORE_POOR )); then
        echo "Poor"
    else
        echo "Critical"
    fi
}

calculate_overall_score() {
    local total=$((GIT_SCORE + DOCS_SCORE + QUALITY_SCORE + SETUP_SCORE + SECURITY_SCORE))
    OVERALL_SCORE=$((total * 100 / TOTAL_MAX))
}

# ============================================================================
# Output Functions
# ============================================================================

output_json() {
    local status_label
    status_label=$(get_status_label "$OVERALL_SCORE")

    cat <<EOF
{
  "project": "Project Catalyst",
  "timestamp": "$(date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || echo 'N/A')",
  "scores": {
    "git_health": {
      "score": $GIT_SCORE,
      "max": $MAX_GIT,
      "percentage": $((GIT_SCORE * 100 / MAX_GIT))
    },
    "documentation_health": {
      "score": $DOCS_SCORE,
      "max": $MAX_DOCS,
      "percentage": $((DOCS_SCORE * 100 / MAX_DOCS))
    },
    "code_quality_health": {
      "score": $QUALITY_SCORE,
      "max": $MAX_QUALITY,
      "percentage": $((QUALITY_SCORE * 100 / MAX_QUALITY))
    },
    "setup_health": {
      "score": $SETUP_SCORE,
      "max": $MAX_SETUP,
      "percentage": $((SETUP_SCORE * 100 / MAX_SETUP))
    },
    "security_health": {
      "score": $SECURITY_SCORE,
      "max": $MAX_SECURITY,
      "percentage": $((SECURITY_SCORE * 100 / MAX_SECURITY))
    },
    "overall": {
      "score": $OVERALL_SCORE,
      "max": 100,
      "status": "$status_label"
    }
  },
  "recommendations": [
$(printf '    "%s",\n' "${RECOMMENDATIONS[@]}" | sed '$ s/,$//')
  ]
}
EOF
}

output_standard() {
    local git_pct=$((GIT_SCORE * 100 / MAX_GIT))
    local docs_pct=$((DOCS_SCORE * 100 / MAX_DOCS))
    local quality_pct=$((QUALITY_SCORE * 100 / MAX_QUALITY))
    local setup_pct=$((SETUP_SCORE * 100 / MAX_SETUP))
    local security_pct=$((SECURITY_SCORE * 100 / MAX_SECURITY))
    local status_label
    status_label=$(get_status_label "$OVERALL_SCORE")

    # Header
    printf '\n'
    printf '%s\n' "$(colorize "$COLOR_BLUE" '🏥 Project Catalyst Health Check')"
    printf '%s\n' "$(colorize "$COLOR_BLUE" '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')"
    printf '\n'

    # Scores
    printf 'Git Health:              %2d/%2d %s\n' \
        "$GIT_SCORE" "$MAX_GIT" \
        "$(colorize "$([[ $git_pct -ge 70 ]] && echo "$COLOR_GREEN" || echo "$COLOR_RED")" "$git_pct%")"

    printf 'Documentation Health:    %2d/%2d %s\n' \
        "$DOCS_SCORE" "$MAX_DOCS" \
        "$(colorize "$([[ $docs_pct -ge 70 ]] && echo "$COLOR_GREEN" || echo "$COLOR_RED")" "$docs_pct%")"

    printf 'Code Quality Health:     %2d/%2d %s\n' \
        "$QUALITY_SCORE" "$MAX_QUALITY" \
        "$(colorize "$([[ $quality_pct -ge 70 ]] && echo "$COLOR_GREEN" || echo "$COLOR_RED")" "$quality_pct%")"

    printf 'Setup Health:            %2d/%2d %s\n' \
        "$SETUP_SCORE" "$MAX_SETUP" \
        "$(colorize "$([[ $setup_pct -ge 70 ]] && echo "$COLOR_GREEN" || echo "$COLOR_RED")" "$setup_pct%")"

    printf 'Security Health:         %2d/%2d %s\n' \
        "$SECURITY_SCORE" "$MAX_SECURITY" \
        "$(colorize "$([[ $security_pct -ge 70 ]] && echo "$COLOR_GREEN" || echo "$COLOR_RED")" "$security_pct%")"

    printf '\n%s\n' "$(colorize "$COLOR_BLUE" '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')"

    printf 'Overall Score: %3d/100  %s %s\n\n' \
        "$OVERALL_SCORE" \
        "$(colorize "$(
            if (( OVERALL_SCORE >= SCORE_EXCELLENT )); then
                echo "$COLOR_GREEN"
            elif (( OVERALL_SCORE >= SCORE_GOOD )); then
                echo "$COLOR_GREEN"
            elif (( OVERALL_SCORE >= SCORE_NEEDS_IMPROVEMENT )); then
                echo "$COLOR_YELLOW"
            else
                echo "$COLOR_RED"
            fi
        )" "$(get_status_symbol "$OVERALL_SCORE")")" \
        "$(colorize "$(
            if (( OVERALL_SCORE >= SCORE_EXCELLENT )); then
                echo "$COLOR_GREEN"
            elif (( OVERALL_SCORE >= SCORE_GOOD )); then
                echo "$COLOR_GREEN"
            elif (( OVERALL_SCORE >= SCORE_NEEDS_IMPROVEMENT )); then
                echo "$COLOR_YELLOW"
            else
                echo "$COLOR_RED"
            fi
        )" "$status_label")"

    # Recommendations
    if (( RECOMMENDATION_COUNT > 0 )); then
        printf '%s\n' "$(colorize "$COLOR_YELLOW" 'Top Recommendations:')"

        local i=1
        for rec in "${RECOMMENDATIONS[@]}"; do
            printf '  %d. %s\n' "$i" "$rec"
            ((i++))
            if (( i > 5 )); then
                printf '  ... and %d more\n' "$((RECOMMENDATION_COUNT - i + 1))"
                break
            fi
        done
        printf '\n'
    fi
}

output_quiet() {
    printf '%d\n' "$OVERALL_SCORE"
}

# ============================================================================
# Main Execution
# ============================================================================

main() {
    # Parse arguments
    parse_arguments "$@"

    # Change to project root
    cd "$PROJECT_ROOT" || exit 1

    if (( ! MODE_QUIET )); then
        log_debug "Project Root: $PROJECT_ROOT"
        log_debug "Running health checks..."
    fi

    # Run all checks
    (( ! MODE_QUIET )) && log_debug ""
    (( ! MODE_QUIET )) && log_debug "=== Git Health Checks ==="
    local git1 git2 git3
    git1=$(check_git_gitignore)
    git2=$(check_git_hooks)
    git3=$(check_git_cicd)
    GIT_SCORE=$((git1 + git2 + git3))

    (( ! MODE_QUIET )) && log_debug ""
    (( ! MODE_QUIET )) && log_debug "=== Documentation Health Checks ==="
    local doc1 doc2 doc3
    doc1=$(check_docs_readme)
    doc2=$(check_docs_contributing)
    doc3=$(check_docs_license)
    DOCS_SCORE=$((doc1 + doc2 + doc3))

    (( ! MODE_QUIET )) && log_debug ""
    (( ! MODE_QUIET )) && log_debug "=== Code Quality Checks ==="
    local qual1 qual2 qual3
    qual1=$(check_quality_linter)
    qual2=$(check_quality_formatter)
    qual3=$(check_quality_tests)
    QUALITY_SCORE=$((qual1 + qual2 + qual3))

    (( ! MODE_QUIET )) && log_debug ""
    (( ! MODE_QUIET )) && log_debug "=== Setup Health Checks ==="
    local setup1 setup2
    setup1=$(check_setup_editorconfig)
    setup2=$(check_setup_package_files)
    SETUP_SCORE=$((setup1 + setup2))

    (( ! MODE_QUIET )) && log_debug ""
    (( ! MODE_QUIET )) && log_debug "=== Security Health Checks ==="
    local sec1 sec2
    sec1=$(check_security_env_in_git)
    sec2=$(check_security_hardcoded_secrets)
    SECURITY_SCORE=$((sec1 + sec2))

    # Calculate overall score
    calculate_overall_score

    # Output results
    if (( MODE_JSON )); then
        output_json
    elif (( MODE_QUIET )); then
        output_quiet
    else
        output_standard
    fi

    # Exit with appropriate code
    if (( OVERALL_SCORE >= SCORE_GOOD )); then
        return 0
    elif (( OVERALL_SCORE >= SCORE_NEEDS_IMPROVEMENT )); then
        return 0
    elif (( OVERALL_SCORE >= SCORE_POOR )); then
        return 0
    else
        return 3
    fi
}

# Run main function
main "$@"
