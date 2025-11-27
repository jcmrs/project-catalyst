# Project Catalyst Health Check Script

## Overview

`health-check.sh` is a production-grade bash script that quickly assesses the overall health of the Project Catalyst plugin project (30-60 seconds max).

## Location

```
scripts/health-check.sh
```

## Features

- **Cross-platform compatibility**: Windows Git Bash, macOS, Linux
- **Fast execution**: Completes in <60 seconds for typical projects
- **Defensive programming**: Full error handling with `set -euo pipefail`
- **Multiple output formats**: Standard, JSON, verbose, and quiet modes
- **Comprehensive scoring**: 100-point scale across 5 categories
- **Actionable recommendations**: Prioritized suggestions for improvements

## Quick Start

```bash
# Standard output with detailed report
./scripts/health-check.sh

# JSON output for CI/CD integration
./scripts/health-check.sh --json

# Verbose mode with all checks detailed
./scripts/health-check.sh --verbose

# Minimal output (just the score)
./scripts/health-check.sh --quiet

# Display help
./scripts/health-check.sh --help
```

## Output Format

### Standard Output

```
🏥 Project Catalyst Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Git Health:              20/25 ✅ 80%
Documentation Health:    15/20 ⚠️ 75%
Code Quality Health:     20/25 ✅ 80%
Setup Health:            15/15 ✅ 100%
Security Health:         10/15 ⚠️ 67%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Score: 80/100  ✅ Good

Top Recommendations:
  1. Enhance README.md (currently 45 lines, needs 100+)
  2. Add code formatter configuration
  3. Improve test coverage

```

### JSON Output

```json
{
  "project": "Project Catalyst",
  "timestamp": "2025-11-27T12:34:56Z",
  "scores": {
    "git_health": {
      "score": 20,
      "max": 25,
      "percentage": 80
    },
    "documentation_health": {
      "score": 15,
      "max": 20,
      "percentage": 75
    },
    "code_quality_health": {
      "score": 20,
      "max": 25,
      "percentage": 80
    },
    "setup_health": {
      "score": 15,
      "max": 15,
      "percentage": 100
    },
    "security_health": {
      "score": 10,
      "max": 15,
      "percentage": 67
    },
    "overall": {
      "score": 80,
      "max": 100,
      "status": "Good"
    }
  },
  "recommendations": [
    "Enhance README.md (currently 45 lines, needs 100+)",
    "Add code formatter configuration",
    "Improve test coverage"
  ]
}
```

### Quiet Output

```
80
```

## Scoring System

### Score Bands

| Score Range | Status | Symbol |
|-------------|--------|--------|
| 90-100 | Excellent | ✅ |
| 70-89 | Good | ✅ |
| 50-69 | Needs Improvement | ⚠️ |
| 30-49 | Poor | ❌ |
| 0-29 | Critical | ❌ |

### Scoring Categories (100 points total)

#### 1. Git Health (25 points)
- `.gitignore` present and populated: **10 pts**
- Git hooks configured: **5 pts**
- GitHub Actions or CI/CD present: **10 pts**

#### 2. Documentation Health (20 points)
- `README.md` present and > 100 lines: **10 pts**
- `CONTRIBUTING.md` present: **5 pts**
- `LICENSE` file present: **5 pts**

#### 3. Code Quality Health (25 points)
- Linter config present (ESLint, Pylint, etc.): **10 pts**
- Formatter config present (Prettier, Black, etc.): **5 pts**
- Test directory exists with tests: **10 pts**

#### 4. Setup Health (15 points)
- `.editorconfig` present: **5 pts**
- Package manager files valid (package.json, requirements.txt, etc.): **10 pts**

#### 5. Security Health (15 points)
- `.env` file properly configured/ignored: **10 pts**
- No obvious hardcoded secrets: **5 pts**

### Total: 100 points

## Command-line Options

```
--json        Output results in JSON format (for automation)
--verbose     Show detailed breakdown of each check
--quiet       Only output final score
--help        Display help message
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Critical errors detected (score < 30) |

## Defensive Programming Features

The script implements multiple defensive programming patterns:

### Error Handling
```bash
set -euo pipefail        # Exit on error, undefined vars, pipe failures
shopt -s inherit_errexit # Better error propagation in functions
```

### Safe Variable Expansion
- All variables quoted: `"${VAR}"`
- Safe arithmetic with local variables
- Proper array handling

### Safe File Operations
- Check file existence: `file_exists()`
- Safe line counting: `count_file_lines()`
- Empty file checks: `file_not_empty()`
- Grep with proper error handling: `grep_exists()`

### Safe Process Management
- Command existence checking: `command -v`
- Proper subshell usage
- Safe find operations with `-print0` support

## Performance Characteristics

**Expected Execution Time:**
- Small projects (<10 files): 2-5 seconds
- Medium projects (<100 files): 5-15 seconds
- Large projects (>1000 files): 15-45 seconds

**Resource Usage:**
- Memory: ~1-2 MB
- CPU: Minimal (no deep analysis)
- I/O: Fast sequential file checks only

## Platform Support

### Tested Platforms
- ✅ Windows Git Bash (Git for Windows 2.30+)
- ✅ macOS (10.14+)
- ✅ Linux (CentOS 7+, Ubuntu 18.04+)

### Bash Requirements
- Minimum: Bash 4.4
- Recommended: Bash 5.0+

## Checks Don't Include

The script deliberately avoids expensive operations:
- ❌ No deep file system scanning
- ❌ No external API calls
- ❌ No complex code analysis
- ❌ No full test execution
- ❌ No dependency tree analysis

## Integration Examples

### CI/CD Pipeline (GitHub Actions)

```yaml
- name: Project Health Check
  run: |
    ./scripts/health-check.sh --json > health-report.json
    SCORE=$(cat health-report.json | jq '.scores.overall.score')
    if (( SCORE < 70 )); then
      echo "Project health score below threshold: $SCORE"
      exit 1
    fi
```

### Pre-commit Hook

```bash
#!/bin/bash
./scripts/health-check.sh --quiet
if (( $? == 3 )); then
    echo "Project health is critical - commit aborted"
    exit 1
fi
```

### Monitoring Script

```bash
#!/bin/bash
# Run hourly health checks and log results
while true; do
    ./scripts/health-check.sh --json >> health-checks.log
    sleep 3600
done
```

## Troubleshooting

### Script won't execute

**Problem**: `Permission denied`

**Solution**:
```bash
chmod +x scripts/health-check.sh
```

### Bash version error

**Problem**: `Bash 4.4+ required`

**Solution**: Upgrade Bash or run with explicit interpreter:
```bash
bash scripts/health-check.sh
```

### Git operations slow

**Problem**: Script takes too long on large repos

**Solution**: Script caches Git checks, but if git is slow, the script will be slow. Consider optimizing your Git config.

### Color codes in JSON output

**Problem**: JSON contains ANSI color codes

**Solution**: Always use `--json` flag for automation to disable colors.

## Development

### Running Tests

```bash
# Syntax check
bash -n scripts/health-check.sh

# Run with verbose output
./scripts/health-check.sh --verbose

# Check JSON output validity
./scripts/health-check.sh --json | jq '.'
```

### Adding New Checks

1. Create check function: `check_category_name()`
2. Add to appropriate category in `main()`
3. Update scoring variables
4. Add to README documentation

Example:
```bash
check_example_feature() {
    local points=0

    log_debug "Checking example feature..."

    if some_condition; then
        points=5
        (( MODE_VERBOSE )) && printf '  ✓ Feature present\n' >&2
    else
        add_recommendation "Configure example feature"
    fi

    echo "$points"
}
```

## License

Project Catalyst - See LICENSE file

## Contributing

See CONTRIBUTING.md for guidelines

## Recommendations Algorithm

The script prioritizes recommendations by:
1. Impact on project health
2. Ease of implementation
3. Best practices alignment
4. Security implications

Recommendations are deduplicated and limited to top 5 for clarity.

## Advanced Usage

### Quiet Mode for Scripts

```bash
SCORE=$(./scripts/health-check.sh --quiet)
if (( SCORE < 70 )); then
    echo "Health check failed with score: $SCORE"
    exit 1
fi
```

### JSON Processing with jq

```bash
# Extract specific score
./scripts/health-check.sh --json | jq '.scores.git_health.percentage'

# Check if any recommendations exist
./scripts/health-check.sh --json | jq '.recommendations | length'

# Format for reporting
./scripts/health-check.sh --json | jq '.scores | to_entries | .[] | "\(.key): \(.value.percentage)%"'
```

### Continuous Monitoring

```bash
# Daily health check report
0 9 * * * cd /path/to/project && ./scripts/health-check.sh >> logs/health-check-$(date +%Y%m%d).log
```

## See Also

- [Project Catalyst README](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Installation Instructions](../docs/installation.md)
