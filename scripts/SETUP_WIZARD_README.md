# Project Catalyst Setup Wizard

Production-grade interactive onboarding script for Project Catalyst plugins.

## Overview

`setup-wizard.sh` provides a comprehensive, user-friendly setup experience for initializing Project Catalyst in new projects. It automates project detection, configuration, and analysis workflow.

**Version:** 1.0.0
**Status:** Production-ready
**Platforms:** Linux, macOS, Windows (Git Bash)

---

## Features

### ✅ Project Detection

- **Automatic Language Detection:**
  - Node.js/JavaScript (package.json, yarn.lock, pnpm-lock.yaml)
  - Python (setup.py, pyproject.toml, requirements.txt, Pipfile)
  - Java (pom.xml, build.gradle)
  - Rust (Cargo.toml)
  - Go (go.mod, go.sum)
  - Ruby (Gemfile, Rakefile)
  - PHP (composer.json)
  - C#/.NET (*.csproj, *.sln)

- **Existing Setup Detection:**
  - Checks for existing `.catalyst/` directory
  - Prompts for reconfiguration if already initialized

### 🎯 Interactive Setup Flow

1. **Welcome Banner** - ASCII art Project Catalyst logo
2. **Project Detection** - Identifies project type with clear feedback
3. **Full Analysis Option** - User choice to run project analyzer
4. **Priority Recommendations** - Language-specific action items
5. **Preference Collection:**
   - Auto-run analyzer on startup
   - Automatic template suggestions
   - Validation strictness level
6. **Configuration Saving** - Stores preferences to `.catalyst/config.json`
7. **Completion** - Creates setup-complete flag and displays next steps

### 📁 Directory Structure

Creates the following structure:

```
.catalyst/
├── setup.log              # Setup operation log
├── config.json            # User preferences
├── analyzed               # Timestamp flag after analysis
├── setup-complete         # Completion flag
└── templates/             # Applied templates tracking
```

### 🛡️ Defensive Bash Patterns

**Error Handling:**
- `set -euo pipefail` for strict error handling
- Proper `ERR` trap with line number reporting
- Exit code tracking and cleanup on abnormal termination
- Graceful degradation when optional tools unavailable

**Input Validation:**
- All variable expansions properly quoted
- User input validated with pattern matching
- File and directory operations safely gated
- Cross-platform `stat` compatibility

**Process Safety:**
- Temporary file operations with cleanup traps
- Binary-safe array handling with `readarray`
- Proper signal handling via trap
- Resource cleanup on EXIT

### 🎨 Output Features

**Visual Indicators:**
- ✅ Success
- ❌ Errors
- ⚠️ Warnings
- 💡 Information
- 🔍 Search/Analysis

**Formatting:**
- ANSI color codes (auto-detected, can be disabled)
- Bold headings for clarity
- Structured section layout
- Terminal detection for safe output

**Logging:**
- Timestamped log entries
- Multiple log levels (INFO, WARN, ERROR, DEBUG)
- All operations logged to `.catalyst/setup.log`
- Verbose mode for detailed diagnostics

---

## Usage

### Basic Interactive Setup

```bash
./scripts/setup-wizard.sh
```

### With Verbose Logging

```bash
./scripts/setup-wizard.sh --verbose
```

### Dry-Run Mode (No Changes)

```bash
./scripts/setup-wizard.sh --dry-run
```

### Disable Colors (for scripting)

```bash
./scripts/setup-wizard.sh --no-color
```

### View Help

```bash
./scripts/setup-wizard.sh --help
```

---

## Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Display help message and exit |
| `--verbose` | `-v` | Enable verbose debug logging |
| `--no-color` | `-n` | Disable ANSI color output |
| `--dry-run` | | Show operations without applying changes |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Setup completed successfully |
| `1` | General error (missing requirements, I/O error) |
| `2` | Invalid command-line arguments |

---

## Configuration File Format

Generated `.catalyst/config.json`:

```json
{
  "version": "1.0",
  "timestamp": "2025-11-27T03:02:22Z",
  "project_type": "nodejs",
  "preferences": {
    "auto_analyzer": true,
    "suggest_templates": true,
    "strictness": "moderate"
  },
  "directories": {
    "catalyst": "/path/to/project/.catalyst",
    "templates": "/path/to/project/.catalyst/templates"
  }
}
```

---

## Analyzer Integration

The wizard automatically detects and runs the project analyzer if available:

- **Path:** `../skills/project-analyzer/scripts/analyze.sh`
- **Behavior:** Gracefully degrades if analyzer not found
- **Output:** Displays summary of findings
- **Logging:** Records analysis timestamp to `.catalyst/analyzed`

---

## Project Type Recommendations

### Node.js
1. Optimize package.json and dependencies
2. Set up build and test automation
3. Configure linting and code formatting

### Python
1. Organize project structure (src/ layout)
2. Set up virtual environment and requirements
3. Configure testing and CI/CD

### Java
1. Review Maven/Gradle build configuration
2. Verify dependency management
3. Set up test coverage and reporting

### Rust
1. Optimize Cargo.toml manifest
2. Review dependency versions
3. Configure clippy and fmt checks

### Ruby, Go, PHP, C#
- Generic recommendations: documentation, testing, guidelines

---

## Cross-Platform Compatibility

### Linux
✅ Full support with GNU tools

### macOS
✅ Full support (uses BSD stat/date)

### Windows (Git Bash)
✅ Tested compatibility with MSYS2/Git Bash
- ANSI colors may need configuration
- Path handling works with forward slashes

---

## Implementation Details

### Robust Directory Creation

```bash
safe_mkdir() {
  local dir="$1"
  [[ -d "${dir}" ]] && return 0
  [[ ${DRY_RUN} -eq 1 ]] && log_info "[DRY-RUN] Would create: ${dir}" && return 0
  mkdir -p "${dir}" 2>/dev/null || return 1
}
```

### Safe File Operations

- Always validate directory existence before writing
- Capture and report file operation errors
- Support dry-run mode for all modifications
- Proper quoting in all path expansions

### Error Handling Pattern

```bash
trap cleanup EXIT
trap 'trap_error ${LINENO}' ERR

cleanup() {
  local exit_code=$?
  [[ ${exit_code} -ne 0 ]] && log_error "Exit code: ${exit_code}"
  return ${exit_code}
}
```

### Logging Pattern

```bash
log_info "Message"          # Logged + displayed
log_warn "Warning"          # Logged + displayed with indicator
log_debug "Debug info"      # Only in verbose mode
echo "User message"         # Direct output
```

---

## Requirements

- **Bash:** 4.4 or later (checked at runtime)
- **Standard Tools:**
  - `date` (for timestamps)
  - `mkdir` (for directory creation)
  - `touch` (for flag files)
  - `stat` or `ls` (for file operations)
- **Optional:**
  - Project analyzer script (graceful degradation if missing)

---

## Troubleshooting

### Script Won't Run

**Problem:** `Permission denied`
**Solution:** Make script executable
```bash
chmod +x scripts/setup-wizard.sh
```

### Bash Version Error

**Problem:** "Bash 4.4 or later required"
**Solution:** Update Bash (macOS: `brew install bash`)

### Colors Not Working

**Problem:** ANSI codes show as garbage
**Solution:** Use `--no-color` flag
```bash
./scripts/setup-wizard.sh --no-color
```

### Cannot Find Analyzer

**Problem:** "Analyzer script not available"
**Solution:** This is expected if analyzer not installed; setup continues

### Permission Issues

**Problem:** Cannot write to `.catalyst/`
**Solution:** Check directory permissions
```bash
ls -la .catalyst/
chmod 755 .catalyst/
```

---

## Testing

### Syntax Validation

```bash
bash -n scripts/setup-wizard.sh
```

### ShellCheck Analysis

```bash
shellcheck scripts/setup-wizard.sh
```

### Dry-Run Test

```bash
scripts/setup-wizard.sh --dry-run --no-color
```

### Verbose Test

```bash
scripts/setup-wizard.sh --verbose --no-color
```

---

## Security Considerations

- **No Credential Handling:** Script avoids storing or logging credentials
- **Input Sanitization:** All user input validated before use
- **Safe Paths:** All file operations use proper quoting
- **No Eval:** Never uses `eval` on user input
- **Logging:** Sensitive operations logged with appropriate detail level

---

## Performance

- **Setup Time:** < 2 seconds (typical)
- **Analysis Time:** Depends on project analyzer
- **Memory Usage:** < 10MB
- **Disk Usage:** < 1KB (.catalyst/ structure)

---

## Contributing

To extend the setup wizard:

1. **Add Project Type Detection:**
   - Add check to `detect_project_type()`
   - Add label to `get_project_type_label()`
   - Add recommendations to `get_priority_recommendations()`

2. **Add Custom Checks:**
   - Extend `run_project_analysis()`
   - Parse analyzer output for specific patterns

3. **New Preferences:**
   - Add prompt to `collect_user_preferences()`
   - Update `.catalyst/config.json` schema

---

## Related Documentation

- [Project Catalyst Architecture](../README.md)
- [Project Analyzer Integration](../skills/project-analyzer/README.md)
- [Configuration Guide](../docs/CONFIG.md)

---

## License

Part of Project Catalyst ecosystem.

## Support

For issues or questions, check `.catalyst/setup.log` for detailed diagnostics.

---

**Last Updated:** November 27, 2025
**Maintained By:** Project Catalyst Team
