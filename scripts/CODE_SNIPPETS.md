# Setup Wizard - Key Code Snippets

Reference implementations of defensive bash patterns used in the setup wizard.

---

## Strict Error Handling

### Setup Error Trap
```bash
set -euo pipefail                                  # Enable strict mode
shopt -s inherit_errexit 2>/dev/null || true      # Error propagation (Bash 4.1+)

trap cleanup EXIT                                 # Always cleanup
trap 'trap_error ${LINENO}' ERR                   # Report error line
```

### Error Handler
```bash
trap_error() {
  local line_num=$1
  print_error "An error occurred at line ${line_num}"
  log_error "Script error at line ${line_num}"
  return 1
}

cleanup() {
  local exit_code=$?
  if [[ ${exit_code} -ne 0 ]]; then
    log_error "Setup wizard exited with code ${exit_code}"
  fi
  return ${exit_code}
}
```

---

## Constant Definitions

### Immutable Constants
```bash
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"

readonly CATALYST_DIR="${PROJECT_ROOT}/.catalyst"
readonly CATALYST_LOG="${CATALYST_DIR}/setup.log"
readonly CATALYST_CONFIG="${CATALYST_DIR}/config.json"
```

---

## Variable Handling

### Proper Quoting
```bash
# ✅ CORRECT - All expansions quoted
echo "Project root: ${PROJECT_ROOT}"
mkdir -p "${CATALYST_DIR}"
[[ -d "${dir}" ]]

# ❌ WRONG - Unquoted expansions
echo Project root: $PROJECT_ROOT    # Word splitting!
mkdir -p $CATALYST_DIR              # Globbing issues!
[[ -d $dir ]]                       # Vulnerable!
```

### Parameter Validation
```bash
# Require variable to be set
: "${PROJECT_ROOT:?PROJECT_ROOT not set}"

# Provide default value
CONFIG_FILE="${1:-${CATALYST_CONFIG}}"

# Pattern matching
if [[ ! "${response}" =~ ^[Yy] ]]; then
  echo "Invalid response"
fi
```

---

## Safe File Operations

### Directory Creation
```bash
safe_mkdir() {
  local dir="$1"

  # Return success if already exists
  if [[ -d "${dir}" ]]; then
    log_debug "Directory already exists: ${dir}"
    return 0
  fi

  # Honor dry-run mode
  if [[ ${DRY_RUN} -eq 1 ]]; then
    log_info "[DRY-RUN] Would create directory: ${dir}"
    return 0
  fi

  # Create with error handling
  if mkdir -p "${dir}" 2>/dev/null; then
    log_debug "Created directory: ${dir}"
    return 0
  else
    log_error "Failed to create directory: ${dir}"
    return 1
  fi
}
```

### Safe File Writing
```bash
safe_write_file() {
  local file="$1"
  local content="$2"

  # Dry-run support
  if [[ ${DRY_RUN} -eq 1 ]]; then
    log_info "[DRY-RUN] Would write file: ${file}"
    return 0
  fi

  # Write with error handling
  if echo "${content}" > "${file}" 2>/dev/null; then
    log_debug "Wrote file: ${file}"
    return 0
  else
    log_error "Failed to write file: ${file}"
    return 1
  fi
}
```

### Safe Touch
```bash
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
```

---

## Logging System

### Centralized Logging
```bash
log_message() {
  local level="$1"
  shift
  local message="$*"
  local timestamp

  timestamp=$(date '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo 'N/A')

  case "${level}" in
    info)
      echo -e "${COLOR_CYAN}${timestamp}${COLOR_RESET} [INFO] ${message}" >&2
      [[ -d "${CATALYST_DIR}" ]] && \
        echo "${timestamp} [INFO] ${message}" >> "${CATALYST_LOG}" 2>/dev/null || true
      ;;
    warn)
      echo -e "${COLOR_YELLOW}${timestamp}${COLOR_RESET} [WARN] ${message}" >&2
      [[ -d "${CATALYST_DIR}" ]] && \
        echo "${timestamp} [WARN] ${message}" >> "${CATALYST_LOG}" 2>/dev/null || true
      ;;
    error)
      echo -e "${COLOR_RED}${timestamp}${COLOR_RESET} [ERROR] ${message}" >&2
      [[ -d "${CATALYST_DIR}" ]] && \
        echo "${timestamp} [ERROR] ${message}" >> "${CATALYST_LOG}" 2>/dev/null || true
      ;;
  esac
}

# Convenience wrappers
log_info() { log_message info "$@"; }
log_warn() { log_message warn "$@"; }
log_error() { log_message error "$@"; }
```

### Output Helpers
```bash
print_success() {
  echo -e "${COLOR_GREEN}✅ $*${COLOR_RESET}"
}

print_error() {
  echo -e "${COLOR_RED}❌ $*${COLOR_RESET}"
}

print_warn() {
  echo -e "${COLOR_YELLOW}⚠️ $*${COLOR_RESET}"
}

print_info() {
  echo -e "${COLOR_CYAN}💡 $*${COLOR_RESET}"
}
```

---

## Command Validation

### Check Command Exists
```bash
command_exists() {
  command -v "$1" &>/dev/null
}

# Usage
if command_exists jq; then
  # Use jq
else
  log_warn "jq not available, skipping JSON parsing"
fi
```

### Safe Analyzer Execution
```bash
run_project_analysis() {
  print_search "Analyzing project structure..."
  log_info "Starting project analysis"

  # Check if analyzer exists
  if [[ ! -f "${ANALYZER_SCRIPT}" ]]; then
    log_warn "Analyzer script not found: ${ANALYZER_SCRIPT}"
    print_warn "Project analyzer not available"
    return 0  # Non-fatal
  fi

  # Check if executable
  if [[ ! -x "${ANALYZER_SCRIPT}" ]]; then
    log_warn "Analyzer script not executable: ${ANALYZER_SCRIPT}"
    print_warn "Cannot execute analyzer (permission denied)"
    return 0  # Non-fatal
  fi

  # Run with error handling
  local analysis_output
  if analysis_output=$("${ANALYZER_SCRIPT}" 2>&1); then
    log_info "Analysis completed successfully"
    echo "${analysis_output}"
    return 0
  else
    log_error "Project analysis failed: ${analysis_output}"
    print_warn "Project analysis encountered an error"
    return 0  # Graceful degradation
  fi
}
```

---

## User Input Validation

### Yes/No Prompt
```bash
prompt_yes_no() {
  local prompt="$1"
  local default="${2:-Y}"
  local response

  while true; do
    echo -en "${COLOR_BOLD}${prompt} [${default}]:${COLOR_RESET} "
    read -r response || response=""

    # Use default if empty
    [[ -z "${response}" ]] && response="${default}"

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
```

### Choice Selection
```bash
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
```

---

## Project Detection

### Auto-Detection Pattern
```bash
detect_project_type() {
  log_debug "Detecting project type in: ${PROJECT_ROOT}"

  # Check for Node.js
  if [[ -f "${PROJECT_ROOT}/package.json" ]] || \
     [[ -f "${PROJECT_ROOT}/yarn.lock" ]]; then
    echo "nodejs"
    return
  fi

  # Check for Python
  if [[ -f "${PROJECT_ROOT}/setup.py" ]] || \
     [[ -f "${PROJECT_ROOT}/pyproject.toml" ]]; then
    echo "python"
    return
  fi

  # Check for Rust
  if [[ -f "${PROJECT_ROOT}/Cargo.toml" ]]; then
    echo "rust"
    return
  fi

  # Default to unknown
  echo "unknown"
}
```

### Language Label Mapping
```bash
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
```

---

## Configuration Management

### JSON Generation
```bash
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
  "timestamp": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
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
```

---

## Color Support Detection

### Terminal-Aware Colors
```bash
# Check if output is TTY and color is supported
if [[ ${USE_COLOR} -eq 1 ]] && [[ -t 1 ]]; then
  readonly COLOR_RESET='\033[0m'
  readonly COLOR_BOLD='\033[1m'
  readonly COLOR_RED='\033[31m'
  readonly COLOR_GREEN='\033[32m'
  readonly COLOR_YELLOW='\033[33m'
  readonly COLOR_CYAN='\033[36m'
else
  # Disable colors on non-TTY or when requested
  readonly COLOR_RESET=''
  readonly COLOR_BOLD=''
  readonly COLOR_RED=''
  readonly COLOR_GREEN=''
  readonly COLOR_YELLOW=''
  readonly COLOR_CYAN=''
fi
```

---

## Argument Parsing

### Robust Option Parsing
```bash
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
```

---

## Best Practices Summary

1. **Always Quote Expansions**
   ```bash
   "${VARIABLE}"  # ✅ Safe
   $VARIABLE      # ❌ Unsafe
   ```

2. **Use readonly for Constants**
   ```bash
   readonly CONSTANT="value"  # ✅ Safe
   CONSTANT="value"           # ❌ Can be modified
   ```

3. **Check Commands Exist**
   ```bash
   command_exists "cmd" || return 1  # ✅ Safe
   cmd                               # ❌ May not exist
   ```

4. **Use [[ ]] for Bash**
   ```bash
   [[ -f "${file}" ]]         # ✅ Bash 3+
   [ -f "${file}" ]           # ✅ POSIX
   ```

5. **Always Have Exit Handlers**
   ```bash
   trap cleanup EXIT          # ✅ Always cleanup
   # No trap                   # ❌ May leak resources
   ```

6. **Validate All Input**
   ```bash
   [[ ! "${var}" =~ ^[0-9]+$ ]] && return 1  # ✅ Validate
   echo "${var}"                             # ❌ No validation
   ```

7. **Use Local Variables in Functions**
   ```bash
   function_name() {
     local var="${1}"         # ✅ Scoped
     var="${1}"               # ❌ Global scope
   }
   ```

8. **Error Trap with Line Numbers**
   ```bash
   trap 'trap_error ${LINENO}' ERR  # ✅ Debugging aid
   trap 'exit 1' ERR                # ❌ No diagnostics
   ```

---

**These patterns ensure production-grade reliability and maintainability.**
