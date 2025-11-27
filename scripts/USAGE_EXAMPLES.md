# Health Check Script - Usage Examples

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Output Modes](#output-modes)
3. [CI/CD Integration](#cicd-integration)
4. [Shell Automation](#shell-automation)
5. [Advanced Scenarios](#advanced-scenarios)
6. [Troubleshooting](#troubleshooting)

## Basic Usage

### Run with Default Output

```bash
$ ./scripts/health-check.sh

🏥 Project Catalyst Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Git Health:              20/25 ✅ 80%
Documentation Health:    15/20 ⚠️  75%
Code Quality Health:     20/25 ✅ 80%
Setup Health:            15/15 ✅ 100%
Security Health:         10/15 ⚠️  67%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Score: 80/100  ✅ Good

Top Recommendations:
  1. Enhance README.md (currently 45 lines, needs 100+)
  2. Add code formatter configuration
  3. Improve test coverage

```

### Check Help

```bash
$ ./scripts/health-check.sh --help

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
```

## Output Modes

### 1. Standard Mode (Default)

Shows complete health report with color-coded scores and recommendations.

```bash
$ ./scripts/health-check.sh
```

**Best for**: Manual review, team meetings, documentation

---

### 2. Verbose Mode

Shows detailed breakdown of each check being performed.

```bash
$ ./scripts/health-check.sh --verbose

[DEBUG] Project Root: /path/to/project-catalyst
[DEBUG] Running health checks...

[DEBUG]
[DEBUG] === Git Health Checks ===
[DEBUG] Checking .gitignore...
  ✓ .gitignore present with 92 patterns
[DEBUG] Checking Git hooks...
  ✓ Git hooks configured (5 hooks)
[DEBUG] Checking CI/CD configuration...
  ✓ CI/CD configured (.github/workflows)

[DEBUG]
[DEBUG] === Documentation Health Checks ===
[DEBUG] Checking README.md...
  ✓ README.md present (250 lines)
[DEBUG] Checking CONTRIBUTING.md...
  ✓ CONTRIBUTING.md present
[DEBUG] Checking LICENSE file...
  ✓ LICENSE file present

...

🏥 Project Catalyst Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Git Health:              25/25 ✅ 100%
...
```

**Best for**: Debugging issues, understanding check details

---

### 3. Quiet Mode

Outputs only the numeric score (0-100).

```bash
$ ./scripts/health-check.sh --quiet
80
```

**Best for**: Shell scripts, CI/CD integration, automated processing

---

### 4. JSON Mode

Outputs detailed JSON report suitable for machine processing.

```bash
$ ./scripts/health-check.sh --json

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

**Best for**: Automation, reporting, data analysis

---

## CI/CD Integration

### GitHub Actions Workflow

Add to `.github/workflows/health-check.yml`:

```yaml
name: Project Health Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    # Run daily at 9 AM UTC
    - cron: '0 9 * * *'

jobs:
  health-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run Health Check
        id: health
        run: |
          RESULT=$(./scripts/health-check.sh --json)
          echo "$RESULT" > health-report.json
          SCORE=$(echo "$RESULT" | jq '.scores.overall.score')
          echo "score=$SCORE" >> $GITHUB_OUTPUT

      - name: Check Score Threshold
        run: |
          SCORE=${{ steps.health.outputs.score }}
          if [ "$SCORE" -lt 70 ]; then
            echo "❌ Health score $SCORE is below threshold (70)"
            exit 1
          else
            echo "✅ Health score $SCORE is acceptable"
          fi

      - name: Upload Report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: health-report
          path: health-report.json

      - name: Comment PR with Results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('health-report.json'));

            let comment = '## 🏥 Project Health Check\n\n';
            comment += `**Overall Score:** ${report.scores.overall.score}/100 (${report.scores.overall.status})\n\n`;
            comment += '### Breakdown\n';
            comment += `- Git Health: ${report.scores.git_health.score}/${report.scores.git_health.max}\n`;
            comment += `- Documentation: ${report.scores.documentation_health.score}/${report.scores.documentation_health.max}\n`;
            comment += `- Code Quality: ${report.scores.code_quality_health.score}/${report.scores.code_quality_health.max}\n`;
            comment += `- Setup: ${report.scores.setup_health.score}/${report.scores.setup_health.max}\n`;
            comment += `- Security: ${report.scores.security_health.score}/${report.scores.security_health.max}\n`;

            if (report.recommendations.length > 0) {
              comment += '\n### Recommendations\n';
              report.recommendations.forEach((rec, idx) => {
                comment += `${idx + 1}. ${rec}\n`;
              });
            }

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### GitLab CI/CD

Add to `.gitlab-ci.yml`:

```yaml
health-check:
  stage: test
  script:
    - ./scripts/health-check.sh --json | tee health-report.json
    - |
      SCORE=$(cat health-report.json | jq '.scores.overall.score')
      if [ "$SCORE" -lt 70 ]; then
        echo "Health score $SCORE is below threshold (70)"
        exit 1
      fi
  artifacts:
    reports:
      dotenv: health-score.env
    paths:
      - health-report.json
  only:
    - main
    - develop
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Health Check') {
            steps {
                script {
                    sh '''
                        ./scripts/health-check.sh --json > health-report.json
                        SCORE=$(jq '.scores.overall.score' health-report.json)
                        echo "Project Health Score: $SCORE/100"

                        if [ "$SCORE" -lt 70 ]; then
                            error("Health score $SCORE is below threshold")
                        fi
                    '''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'health-report.json'
        }
    }
}
```

## Shell Automation

### Conditional Exit Based on Score

```bash
#!/bin/bash
set -euo pipefail

SCORE=$(./scripts/health-check.sh --quiet)

case $SCORE in
    [0-4]*)
        echo "❌ CRITICAL: Score $SCORE - immediate action required"
        exit 3
        ;;
    [5-6]*)
        echo "⚠️  POOR: Score $SCORE - improvements needed"
        exit 1
        ;;
    [7-8]*)
        echo "✅ GOOD: Score $SCORE - acceptable health"
        exit 0
        ;;
    [9-9]*)
        echo "✅ EXCELLENT: Score $SCORE - outstanding"
        exit 0
        ;;
    100)
        echo "✅ PERFECT: Score $SCORE - perfect health"
        exit 0
        ;;
    *)
        echo "⚠️  UNKNOWN: Score $SCORE"
        exit 2
        ;;
esac
```

### JSON Processing with jq

```bash
#!/bin/bash

# Extract all category scores
echo "=== Category Scores ==="
./scripts/health-check.sh --json | jq '.scores | to_entries[] | "\(.key): \(.value.score)/\(.value.max) (\(.value.percentage)%)"'

# Get recommendations count
echo ""
echo "=== Recommendations ==="
RECS=$(./scripts/health-check.sh --json | jq '.recommendations | length')
echo "Total recommendations: $RECS"

# Show first 3 recommendations
echo ""
echo "Top recommendations:"
./scripts/health-check.sh --json | jq '.recommendations[:3][] | "  - \(.)"'

# Export to environment variables
REPORT=$(./scripts/health-check.sh --json)
export HEALTH_SCORE=$(echo "$REPORT" | jq '.scores.overall.score')
export HEALTH_STATUS=$(echo "$REPORT" | jq -r '.scores.overall.status')
export GIT_SCORE=$(echo "$REPORT" | jq '.scores.git_health.percentage')
export DOCS_SCORE=$(echo "$REPORT" | jq '.scores.documentation_health.percentage')
export QUALITY_SCORE=$(echo "$REPORT" | jq '.scores.code_quality_health.percentage')

echo "Exported variables:"
echo "  HEALTH_SCORE=$HEALTH_SCORE ($HEALTH_STATUS)"
echo "  GIT_SCORE=$GIT_SCORE%"
echo "  DOCS_SCORE=$DOCS_SCORE%"
echo "  QUALITY_SCORE=$QUALITY_SCORE%"
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
set -euo pipefail

echo "Running project health check..."

SCORE=$(./scripts/health-check.sh --quiet)

# Fail if score is critical
if [ "$SCORE" -lt 30 ]; then
    echo "❌ Project health is CRITICAL ($SCORE/100)"
    echo "Run './scripts/health-check.sh' for details"
    exit 1
fi

# Warn if score is poor but allow commit
if [ "$SCORE" -lt 50 ]; then
    echo "⚠️  Project health is POOR ($SCORE/100)"
    echo "Consider: ./scripts/health-check.sh --verbose"
fi

exit 0
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Advanced Scenarios

### Daily Health Check Report

```bash
#!/bin/bash
# health-check-daily-report.sh
# Run as: 0 9 * * * /path/to/health-check-daily-report.sh

PROJECT_DIR="/path/to/project-catalyst"
REPORT_DIR="${PROJECT_DIR}/reports/health"
DATE=$(date +%Y-%m-%d)
REPORT_FILE="${REPORT_DIR}/health-${DATE}.json"

mkdir -p "$REPORT_DIR"

cd "$PROJECT_DIR"

# Generate report
./scripts/health-check.sh --json > "$REPORT_FILE"

# Extract metrics
SCORE=$(jq '.scores.overall.score' "$REPORT_FILE")
STATUS=$(jq -r '.scores.overall.status' "$REPORT_FILE")

# Log to central system
logger -t health-check "Score: $SCORE/100 Status: $STATUS"

# Email if score drops
if [ -f "${REPORT_DIR}/health-$(date -d yesterday +%Y-%m-%d).json" ]; then
    PREV_SCORE=$(jq '.scores.overall.score' "${REPORT_DIR}/health-$(date -d yesterday +%Y-%m-%d).json")

    if [ "$SCORE" -lt "$PREV_SCORE" ]; then
        mail -s "⚠️  Project Health Degradation Alert" admin@example.com <<EOF
Project health score has decreased.

Previous: $PREV_SCORE/100
Current:  $SCORE/100

See: $REPORT_FILE
EOF
    fi
fi

echo "Health check report saved: $REPORT_FILE"
```

### Health Trend Analysis

```bash
#!/bin/bash
# analyze-health-trend.sh
# Analyze health check trends over time

REPORT_DIR="./reports/health"

echo "Health Check Trend Analysis"
echo "============================"
echo ""

# Find all reports
for report in $(ls -1 "$REPORT_DIR"/*.json | sort -r | head -10); do
    DATE=$(basename "$report" .json | sed 's/health-//')
    SCORE=$(jq '.scores.overall.score' "$report")
    STATUS=$(jq -r '.scores.overall.status' "$report")

    printf "%-12s Score: %3d/100  Status: %-20s\n" "$DATE" "$SCORE" "$STATUS"
done

echo ""
echo "Detailed Analysis:"
echo "=================="

# Get latest report
LATEST=$(ls -1t "$REPORT_DIR"/*.json | head -1)
OLDEST=$(ls -1t "$REPORT_DIR"/*.json | tail -1)

LATEST_SCORE=$(jq '.scores.overall.score' "$LATEST")
OLDEST_SCORE=$(jq '.scores.overall.score' "$OLDEST")
TREND=$((LATEST_SCORE - OLDEST_SCORE))

echo "Latest Score:  $LATEST_SCORE/100"
echo "Oldest Score:  $OLDEST_SCORE/100"
echo "Trend:         $([ "$TREND" -gt 0 ] && echo "📈 +$TREND" || echo "📉 $TREND")"

# Category analysis
echo ""
echo "Category Breakdown (Latest):"
jq '.scores | to_entries[] | select(.key != "overall") | "\(.key): \(.value.percentage)%"' "$LATEST" | sort
```

## Troubleshooting

### Script Hangs

**Symptom**: Script appears to freeze during execution

**Solution**:
```bash
# Run with timeout
timeout 60 ./scripts/health-check.sh --quiet

# Or check if Git is slow
time git status

# Or use verbose mode to see progress
./scripts/health-check.sh --verbose
```

### Invalid Score Output

**Symptom**: Weird characters or empty output in quiet mode

**Solution**:
```bash
# Check for stderr pollution
./scripts/health-check.sh --quiet 2>/dev/null

# Verify syntax
bash -n ./scripts/health-check.sh

# Run verbose to see issues
./scripts/health-check.sh --verbose 2>&1
```

### JSON Parsing Fails

**Symptom**: `jq: parse error`

**Solution**:
```bash
# Validate JSON output
./scripts/health-check.sh --json | jq '.' > /dev/null

# Check for non-JSON characters
./scripts/health-check.sh --json | head -c 100

# Ensure no stderr pollution
./scripts/health-check.sh --json 2>/dev/null | jq '.'
```

### Git Operations Slow

**Symptom**: `check_security_env_in_git` or other Git checks are slow

**Solution**:
```bash
# Optimize Git config
git gc --aggressive

# Or use different check mode
GIT_OPTIONAL_LOCKS=0 ./scripts/health-check.sh

# Monitor with time
time ./scripts/health-check.sh --json > /dev/null
```

## See Also

- [Health Check README](./HEALTH_CHECK_README.md)
- [Main Project README](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
