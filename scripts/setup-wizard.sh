#!/usr/bin/env bash
# Project Catalyst Setup Wizard
# Interactive onboarding script for new projects using Project Catalyst
#
# Usage: ./scripts/setup-wizard.sh [OPTIONS]
# Options:
#   -h, --help        Display this help message
#   -v, --verbose     Enable verbose logging
#   -n, --no-color    Disable colored output
#   --dry-run         Show what would be done without making changes
#
# Supported platforms: Linux, macOS, Windows (Git Bash)
# Requires: Bash 4.4+

set -euo pipefail
shopt -s inherit_errexit 2>/dev/null || true

# Script metadata
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"

# Catalyst configuration
readonly CATALYST_DIR="${PROJECT_ROOT}/.catalyst"
readonly CATALYST_LOG="${CATALYST_DIR}/setup.log"
readonly CATALYST_CONFIG="${CATALYST_DIR}/config.json"
readonly CATALYST_ANALYZED="${CATALYST_DIR}/analyzed"
readonly CATALYST_COMPLETE="${CATALYST_DIR}/setup-complete"
readonly TEMPLATES_DIR="${CATALYST_DIR}/templates"

# Analyzer script
readonly ANALYZER_SCRIPT="${PROJECT_ROOT}/../skills/project-analyzer/scripts/analyze.sh"

# Global options
VERBOSE=0
USE_COLOR=1
DRY_RUN=0

# Color codes (disable on Windows or if not supported)
if [[ ${USE_COLOR} -eq 1 ]] && [[ -t 1 ]]; then
  readonly COLOR_RESET='\033[0m'
  readonly COLOR_BOLD='\033[1m'
  readonly COLOR_RED='\033[31m'
  readonly COLOR_GREEN='\033[32m'
  readonly COLOR_YELLOW='\033[33m'
  readonly COLOR_BLUE='\033[34m'
  readonly COLOR_CYAN='\033[36m'
else
  readonly COLOR_RESET=''
  readonly COLOR_BOLD=''
  readonly COLOR_RED=''
  readonly COLOR_GREEN=''
  readonly COLOR_YELLOW=''
  readonly COLOR_BLUE=''
  readonly COLOR_CYAN=''
fi

# Indicators
readonly INDICATOR_SUCCESS="✅"
readonly INDICATOR_ERROR="❌"
readonly INDICATOR_WARN="⚠️ "
readonly INDICATOR_INFO="💡"
readonly INDICATOR_SEARCH="🔍"

# ============================================================================
# Logging and Output Functions
# ============================================================================

#@description Log a message with timestamp and level
#@arg $1 level (info|warn|error|debug)
#@arg $@ message
log_message() {
  local level="$1"
  shift
  local message="$*"
  local timestamp

  timestamp=$(date '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo 'N/A')

  case "${level}" in
    info)
      echo -e "${COLOR_CYAN}${timestamp}${COLOR_RESET} [INFO] ${message}" >&2
      [[ -d "${CATALYST_DIR}" ]] && echo "${timestamp} [INFO] ${message}" >> "${CATALYST_LOG}" 2>/dev/null || true
      ;;
    warn)
      echo -e "${COLOR_YELLOW}${timestamp}${COLOR_RESET} [WARN] ${INDICATOR_WARN} ${message}" >&2
      [[ -d "${CATALYST_DIR}" ]] && echo "${timestamp} [WARN] ${message}" >> "${CATALYST_LOG}" 2>/dev/null || true
      ;;
    error)
      echo -e "${COLOR_RED}${timestamp}${COLOR_RESET} [ERROR] ${INDICATOR_ERROR} ${message}" >&2
      [[ -d "${CATALYST_DIR}" ]] && echo "${timestamp} [ERROR] ${message}" >> "${CATALYST_LOG}" 2>/dev/null || true
      ;;
    debug)
      if [[ ${VERBOSE} -eq 1 ]]; then
        echo -e "${COLOR_BLUE}${timestamp}${COLOR_RESET} [DEBUG] ${message}" >&2
        [[ -d "${CATALYST_DIR}" ]] && echo "${timestamp} [DEBUG] ${message}" >> "${CATALYST_LOG}" 2>/dev/null || true
      fi
      ;;
  esac
}

#@description Log info message
log_info() {
  log_message info "$@"
}

#@description Log warning message
log_warn() {
  log_message warn "$@"
}

#@description Log error message
log_error() {
  log_message error "$@"
}

#@description Log debug message (only in verbose mode)
log_debug() {
  log_message debug "$@"
}

#@description Print success message with indicator
print_success() {
  echo -e "${COLOR_GREEN}${INDICATOR_SUCCESS} $*${COLOR_RESET}"
}

#@description Print error message with indicator
print_error() {
  echo -e "${COLOR_RED}${INDICATOR_ERROR} $*${COLOR_RESET}"
}

#@description Print warning message with indicator
print_warn() {
  echo -e "${COLOR_YELLOW}${INDICATOR_WARN}$*${COLOR_RESET}"
}

#@description Print info message with indicator
print_info() {
  echo -e "${COLOR_CYAN}${INDICATOR_INFO} $*${COLOR_RESET}"
}

#@description Print search indicator
print_search() {
  echo -e "${COLOR_CYAN}${INDICATOR_SEARCH} $*${COLOR_RESET}"
}

# ============================================================================
# Utility Functions
# ============================================================================

#@description Display usage information
show_usage() {
  cat <<EOF
${COLOR_BOLD}Project Catalyst Setup Wizard${COLOR_RESET}
${COLOR_CYAN}v${SCRIPT_VERSION}${COLOR_RESET}

${COLOR_BOLD}Usage:${COLOR_RESET}
  ${SCRIPT_NAME} [OPTIONS]

${COLOR_BOLD}Options:${COLOR_RESET}
  -h, --help        Display this help message
  -v, --verbose     Enable verbose logging
  -n, --no-color    Disable colored output
  --dry-run         Show what would be done without making changes

${COLOR_BOLD}Examples:${COLOR_RESET}
  # Run interactive setup
  ${SCRIPT_NAME}

  # Run with verbose logging
  ${SCRIPT_NAME} --verbose

  # Preview changes without applying
  ${SCRIPT_NAME} --dry-run

${COLOR_BOLD}Supported Platforms:${COLOR_RESET}
  Linux, macOS, Windows (Git Bash)

${COLOR_BOLD}Requirements:${COLOR_RESET}
  Bash 4.4 or later

${COLOR_BOLD}Exit Codes:${COLOR_RESET}
  0   - Setup completed successfully
  1   - General error occurred
  2   - Invalid arguments provided

${COLOR_BOLD}Output:${COLOR_RESET}
  Setup logs are written to: ${CATALYST_LOG}

${COLOR_RESET}
EOF
}

#@description Validate bash version
validate_bash_version() {
  log_debug "Checking Bash version"

  if [[ ${BASH_VERSINFO[0]} -lt 4 ]] || \
     ([[ ${BASH_VERSINFO[0]} -eq 4 ]] && [[ ${BASH_VERSINFO[1]} -lt 4 ]]); then
    print_error "Bash 4.4 or later required (current: ${BASH_VERSION})"
    log_error "Bash version check failed: ${BASH_VERSION}"
    return 1
  fi

  log_debug "Bash version OK: ${BASH_VERSION}"
  return 0
}

#@description Check if command exists
command_exists() {
  command -v "$1" &>/dev/null
}

#@description Safely create directory
safe_mkdir() {
  local dir="$1"

  if [[ -d "${dir}" ]]; then
    log_debug "Directory already exists: ${dir}"
    return 0
  fi

  if [[ ${DRY_RUN} -eq 1 ]]; then
    log_info "[DRY-RUN] Would create directory: ${dir}"
    return 0
  fi

  if mkdir -p "${dir}" 2>/dev/null; then
    log_debug "Created directory: ${dir}"
    return 0
  else
    log_error "Failed to create directory: ${dir}"
    return 1
  fi
}

#@description Safely write file
safe_write_file() {
  local file="$1"
  local content="$2"

  if [[ ${DRY_RUN} -eq 1 ]]; then
    log_info "[DRY-RUN] Would write file: ${file}"
    return 0
  fi

  if echo "${content}" > "${file}" 2>/dev/null; then
    log_debug "Wrote file: ${file}"
    return 0
  else
    log_error "Failed to write file: ${file}"
    return 1
  fi
}

#@description Safely touch file
safe_touch_file() {
  local file="$1"

  if [[ ${DRY_RUN} -eq 1 ]]; then
    log_info "[DRY-RUN] Would create file: ${file}"
    return 0
  fi

  if touch "${file}" 2>/dev/null; then
    log_debug "Created file: ${file}"
    return 0
  else
    log_error "Failed to create file: ${file}"
    return 1
  fi
}

#@description Get current timestamp in ISO format
get_timestamp() {
  date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || echo "N/A"
}

#@description Cross-platform stat for file mtime
get_file_mtime() {
  local file="$1"

  if command_exists stat; then
    if [[ "$(uname -s)" == "Darwin" ]]; then
      # macOS BSD stat
      stat -f '%m' "${file}" 2>/dev/null || echo "0"
    else
      # GNU stat
      stat -c '%Y' "${file}" 2>/dev/null || echo "0"
    fi
  else
    # Fallback: try ls -l parsing
    if [[ -f "${file}" ]]; then
      ls -la "${file}" | awk '{print NF}' | head -1 || echo "0"
    fi
  fi
}

# ============================================================================
# Project Detection Functions
# ============================================================================

#@description Display ASCII banner
display_banner() {
  cat <<'EOF'

    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          🚀  PROJECT CATALYST - Setup Wizard  🚀            ║
    ║                                                              ║
    ║            Interactive Onboarding for Smart Projects         ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝

EOF
}

#@description Detect project type based on file signatures
#@stdout Project type (nodejs|python|java|rust|go|ruby|php|csharp|unknown)
detect_project_type() {
  log_debug "Detecting project type in: ${PROJECT_ROOT}"

  # Check for Node.js
  if [[ -f "${PROJECT_ROOT}/package.json" ]] || \
     [[ -f "${PROJECT_ROOT}/yarn.lock" ]] || \
     [[ -f "${PROJECT_ROOT}/pnpm-lock.yaml" ]]; then
    echo "nodejs"
    return
  fi

  # Check for Python
  if [[ -f "${PROJECT_ROOT}/setup.py" ]] || \
     [[ -f "${PROJECT_ROOT}/setup.cfg" ]] || \
     [[ -f "${PROJECT_ROOT}/pyproject.toml" ]] || \
     [[ -f "${PROJECT_ROOT}/requirements.txt" ]] || \
     [[ -f "${PROJECT_ROOT}/Pipfile" ]]; then
    echo "python"
    return
  fi

  # Check for Java
  if [[ -f "${PROJECT_ROOT}/pom.xml" ]] || \
     [[ -f "${PROJECT_ROOT}/build.gradle" ]] || \
     [[ -f "${PROJECT_ROOT}/build.gradle.kts" ]]; then
    echo "java"
    return
  fi

  # Check for Rust
  if [[ -f "${PROJECT_ROOT}/Cargo.toml" ]]; then
    echo "rust"
    return
  fi

  # Check for Go
  if [[ -f "${PROJECT_ROOT}/go.mod" ]] || \
     [[ -f "${PROJECT_ROOT}/go.sum" ]]; then
    echo "go"
    return
  fi

  # Check for Ruby
  if [[ -f "${PROJECT_ROOT}/Gemfile" ]] || \
     [[ -f "${PROJECT_ROOT}/Rakefile" ]] || \
     [[ -f "${PROJECT_ROOT}/.ruby-version" ]]; then
    echo "ruby"
    return
  fi

  # Check for PHP
  if [[ -f "${PROJECT_ROOT}/composer.json" ]] || \
     [[ -f "${PROJECT_ROOT}/composer.lock" ]]; then
    echo "php"
    return
  fi

  # Check for C#
  if [[ -f "${PROJECT_ROOT}/"*.csproj ]] || \
     [[ -f "${PROJECT_ROOT}/"*.sln ]] || \
     [[ -f "${PROJECT_ROOT}/project.json" ]]; then
    echo "csharp"
    return
  fi

  echo "unknown"
}

#@description Get human-readable project type name
get_project_type_label() {
  local type="$1"

  case "${type}" in
    nodejs) echo "Node.js/JavaScript" ;;
    python) echo "Python" ;;
    java) echo "Java" ;;
    rust) echo "Rust" ;;
    go) echo "Go" ;;
    ruby) echo "Ruby" ;;
    php) echo "PHP" ;;
    csharp) echo "C#/.NET" ;;
    *) echo "Unknown" ;;
  esac
}

#@description Detect if project has existing catalyst setup
is_catalyst_initialized() {
  [[ -d "${CATALYST_DIR}" ]]
}

# ============================================================================
# Interactive Prompts
# ============================================================================

#@description Prompt user for yes/no response
#@arg $1 prompt message
#@arg $2 default answer (Y/n or y/N), defaults to Y
#@stdout "y" or "n"
prompt_yes_no() {
  local prompt="$1"
  local default="${2:-Y}"
  local response

  while true; do
    echo -en "${COLOR_BOLD}${prompt} [${default}]:${COLOR_RESET} "
    read -r response || response=""

    # Use default if empty response
    if [[ -z "${response}" ]]; then
      response="${default}"
    fi

    case "${response}" in
      [Yy]) return 0 ;;
      [Nn]) return 1 ;;
      *)
        print_warn "Please answer 'y' or 'n'"
        continue
        ;;
    esac
  done
}

#@description Prompt user to select from options
#@arg $1 prompt message
#@arg $2... options (space-separated)
#@stdout selected option
prompt_choice() {
  local prompt="$1"
  shift
  local options=("$@")
  local choice
  local i

  echo ""
  echo -e "${COLOR_BOLD}${prompt}${COLOR_RESET}"

  for i in "${!options[@]}"; do
    echo "  $((i+1))) ${options[$i]}"
  done

  while true; do
    echo -en "${COLOR_BOLD}Select option [1-${#options[@]}]:${COLOR_RESET} "
    read -r choice || choice=""

    if [[ -z "${choice}" ]]; then
      print_warn "Please enter a valid option number"
      continue
    fi

    if [[ ! "${choice}" =~ ^[0-9]+$ ]] || \
       [[ ${choice} -lt 1 ]] || \
       [[ ${choice} -gt ${#options[@]} ]]; then
      print_warn "Please enter a number between 1 and ${#options[@]}"
      continue
    fi

    echo "${options[$((choice-1))]}"
    return 0
  done
}

# ============================================================================
# Catalyst Directory Setup
# ============================================================================

#@description Create catalyst directory structure
setup_catalyst_directories() {
  print_info "Setting up Catalyst directory structure..."
  log_info "Creating catalyst directories"

  local dirs=(
    "${CATALYST_DIR}"
    "${TEMPLATES_DIR}"
  )

  local dir
  for dir in "${dirs[@]}"; do
    if ! safe_mkdir "${dir}"; then
      log_error "Failed to create directory: ${dir}"
      return 1
    fi
    print_success "Created: ${dir}"
  done

  return 0
}

# ============================================================================
# Project Analysis
# ============================================================================

#@description Run project analyzer if available
run_project_analysis() {
  print_search "Analyzing project structure..."
  log_info "Starting project analysis"

  if [[ ! -f "${ANALYZER_SCRIPT}" ]]; then
    log_warn "Analyzer script not found: ${ANALYZER_SCRIPT}"
    print_warn "Project analyzer not available"
    return 0
  fi

  if [[ ! -x "${ANALYZER_SCRIPT}" ]]; then
    log_warn "Analyzer script not executable: ${ANALYZER_SCRIPT}"
    print_warn "Cannot execute analyzer (permission denied)"
    return 0
  fi

  # Run analyzer and capture output
  local analysis_output
  if analysis_output=$("${ANALYZER_SCRIPT}" 2>&1); then
    log_info "Analysis completed successfully"

    # Display findings summary
    echo ""
    echo -e "${COLOR_BOLD}Analysis Results:${COLOR_RESET}"
    echo "${analysis_output}" | head -20

    if [[ $(echo "${analysis_output}" | wc -l) -gt 20 ]]; then
      echo "... (truncated)"
    fi

    # Record analysis timestamp
    if ! safe_touch_file "${CATALYST_ANALYZED}"; then
      log_warn "Failed to record analysis timestamp"
    fi

    return 0
  else
    log_error "Project analysis failed: ${analysis_output}"
    print_warn "Project analysis encountered an error"
    return 0
  fi
}

#@description Get priority recommendations (stub)
get_priority_recommendations() {
  local project_type="$1"

  print_info "Top priority recommendations for ${COLOR_BOLD}${project_type}${COLOR_RESET}:"

  case "${project_type}" in
    nodejs)
      echo "  1. Optimize package.json and dependencies"
      echo "  2. Set up build and test automation"
      echo "  3. Configure linting and code formatting"
      ;;
    python)
      echo "  1. Organize project structure (src/ layout)"
      echo "  2. Set up virtual environment and requirements"
      echo "  3. Configure testing and CI/CD"
      ;;
    java)
      echo "  1. Review Maven/Gradle build configuration"
      echo "  2. Verify dependency management"
      echo "  3. Set up test coverage and reporting"
      ;;
    rust)
      echo "  1. Optimize Cargo.toml manifest"
      echo "  2. Review dependency versions"
      echo "  3. Configure clippy and fmt checks"
      ;;
    *)
      echo "  1. Document project structure"
      echo "  2. Set up automated testing"
      echo "  3. Configure development guidelines"
      ;;
  esac
}

# ============================================================================
# Configuration Management
# ============================================================================

#@description Prompt for user preferences
collect_user_preferences() {
  print_info "Configuring Catalyst preferences..."
  log_info "Collecting user preferences"

  echo ""

  local auto_analyzer
  if prompt_yes_no "Auto-run analyzer on session start?" "Y"; then
    auto_analyzer="true"
  else
    auto_analyzer="false"
  fi

  local suggest_templates
  if prompt_yes_no "Suggest templates automatically?" "Y"; then
    suggest_templates="true"
  else
    suggest_templates="false"
  fi

  local strictness
  strictness=$(prompt_choice "Validation strictness level:" \
    "strict (fail on any issues)" \
    "moderate (fail on critical issues)" \
    "relaxed (log issues, don't fail)")

  # Simplify strictness value
  case "${strictness}" in
    *strict*) strictness="strict" ;;
    *moderate*) strictness="moderate" ;;
    *) strictness="relaxed" ;;
  esac

  log_debug "Collected preferences: auto_analyzer=${auto_analyzer}, suggest_templates=${suggest_templates}, strictness=${strictness}"

  echo "${auto_analyzer}" "${suggest_templates}" "${strictness}"
}

#@description Save configuration to config.json
save_configuration() {
  local auto_analyzer="$1"
  local suggest_templates="$2"
  local strictness="$3"
  local project_type="$4"

  log_info "Saving configuration to ${CATALYST_CONFIG}"

  local config_content
  config_content=$(cat <<EOF
{
  "version": "1.0",
  "timestamp": "$(get_timestamp)",
  "project_type": "${project_type}",
  "preferences": {
    "auto_analyzer": ${auto_analyzer},
    "suggest_templates": ${suggest_templates},
    "strictness": "${strictness}"
  },
  "directories": {
    "catalyst": "${CATALYST_DIR}",
    "templates": "${TEMPLATES_DIR}"
  }
}
EOF
)

  if ! safe_write_file "${CATALYST_CONFIG}" "${config_content}"; then
    log_error "Failed to save configuration"
    return 1
  fi

  print_success "Configuration saved"
  return 0
}

# ============================================================================
# Setup Completion
# ============================================================================

#@description Display setup summary
display_summary() {
  local project_type="$1"

  echo ""
  echo -e "${COLOR_BOLD}═══════════════════════════════════════════════════════════════${COLOR_RESET}"
  echo -e "${COLOR_BOLD}Setup Summary${COLOR_RESET}"
  echo -e "${COLOR_BOLD}═══════════════════════════════════════════════════════════════${COLOR_RESET}"
  echo ""
  echo -e "  ${COLOR_GREEN}✓${COLOR_RESET} Project Type:     ${COLOR_BOLD}$(get_project_type_label "${project_type}")${COLOR_RESET}"
  echo -e "  ${COLOR_GREEN}✓${COLOR_RESET} Catalyst Dir:     ${COLOR_BOLD}.catalyst/${COLOR_RESET}"
  echo -e "  ${COLOR_GREEN}✓${COLOR_RESET} Config File:      ${COLOR_BOLD}.catalyst/config.json${COLOR_RESET}"
  echo -e "  ${COLOR_GREEN}✓${COLOR_RESET} Setup Log:        ${COLOR_BOLD}.catalyst/setup.log${COLOR_RESET}"
  echo ""
}

#@description Display next steps
display_next_steps() {
  echo -e "${COLOR_BOLD}Next Steps:${COLOR_RESET}"
  echo ""
  echo "  1. Review .catalyst/config.json for preferences"
  echo "  2. Explore .catalyst/templates/ for available templates"
  echo "  3. Run project analyzer to generate detailed insights"
  echo "  4. Apply recommended templates to your project"
  echo ""
}

#@description Mark setup as complete
mark_setup_complete() {
  log_info "Marking setup as complete"

  if ! safe_touch_file "${CATALYST_COMPLETE}"; then
    log_warn "Failed to create setup-complete flag"
    return 1
  fi

  print_success "Setup completed successfully!"
  return 0
}

# ============================================================================
# Error Handling and Cleanup
# ============================================================================

#@description Cleanup function called on exit/error
cleanup() {
  local exit_code=$?

  if [[ ${exit_code} -ne 0 ]]; then
    log_error "Setup wizard exited with code ${exit_code}"
  fi

  return ${exit_code}
}

#@description Trap errors and display helpful message
trap_error() {
  local line_num=$1
  print_error "An error occurred at line ${line_num}"
  log_error "Script error at line ${line_num}"
  return 1
}

# Set up error handling
trap cleanup EXIT
trap 'trap_error ${LINENO}' ERR

# ============================================================================
# Main Setup Flow
# ============================================================================

#@description Parse command-line arguments
parse_arguments() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--help)
        show_usage
        exit 0
        ;;
      -v|--verbose)
        VERBOSE=1
        log_debug "Verbose mode enabled"
        shift
        ;;
      -n|--no-color)
        USE_COLOR=0
        shift
        ;;
      --dry-run)
        DRY_RUN=1
        log_info "Dry-run mode enabled"
        shift
        ;;
      -*)
        print_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 2
        ;;
      *)
        print_error "Unexpected argument: $1"
        echo "Use --help for usage information"
        exit 2
        ;;
    esac
  done
}

#@description Main setup workflow
main() {
  # Parse arguments
  parse_arguments "$@"

  # Validate environment
  if ! validate_bash_version; then
    exit 1
  fi

  # Initialize logging
  if ! safe_mkdir "${CATALYST_DIR}"; then
    print_error "Failed to initialize Catalyst directory"
    exit 1
  fi

  log_info "========== Project Catalyst Setup Wizard Started =========="
  log_info "Script version: ${SCRIPT_VERSION}"
  log_info "Project root: ${PROJECT_ROOT}"
  log_info "Platform: $(uname -s)"
  log_info "Bash version: ${BASH_VERSION}"

  # Display banner
  display_banner

  # Detect project type
  print_search "Detecting project type..."
  local project_type
  project_type=$(detect_project_type)
  print_success "Detected: $(get_project_type_label "${project_type}")"
  log_info "Detected project type: ${project_type}"

  # Check for existing setup
  if is_catalyst_initialized; then
    print_warn "Catalyst is already initialized in this project"
    if ! prompt_yes_no "Continue with reconfiguration?" "n"; then
      log_info "Setup cancelled by user"
      echo "Setup cancelled."
      exit 0
    fi
    log_info "User opted to reconfigure"
  fi

  # Ask about full analysis
  echo ""
  if prompt_yes_no "Run full project analysis?" "Y"; then
    log_info "User requested full analysis"

    # Setup directories first
    if ! setup_catalyst_directories; then
      print_error "Failed to setup Catalyst directories"
      exit 1
    fi

    # Run analysis
    if ! run_project_analysis; then
      log_warn "Project analysis did not complete successfully"
    fi

    # Show recommendations
    echo ""
    get_priority_recommendations "${project_type}"
  else
    log_info "User skipped full analysis"

    # Still create directories
    if ! setup_catalyst_directories; then
      print_error "Failed to setup Catalyst directories"
      exit 1
    fi
  fi

  # Collect preferences
  echo ""
  read -r auto_analyzer suggest_templates strictness < <(collect_user_preferences)

  # Save configuration
  if ! save_configuration "${auto_analyzer}" "${suggest_templates}" "${strictness}" "${project_type}"; then
    print_error "Failed to save configuration"
    exit 1
  fi

  # Mark setup complete
  if ! mark_setup_complete; then
    log_warn "Failed to mark setup as complete"
  fi

  # Display summary and next steps
  display_summary "${project_type}"
  display_next_steps

  log_info "========== Project Catalyst Setup Wizard Completed =========="
  return 0
}

# Execute main function if script is being run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
