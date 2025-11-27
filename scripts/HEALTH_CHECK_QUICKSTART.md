# Health Check Script - Quick Start Guide

## Installation (30 seconds)

The script is ready to use - no installation needed!

```bash
cd project-catalyst
./scripts/health-check.sh --help
```

## Basic Usage

### 1. Get Project Health Score

```bash
./scripts/health-check.sh
```

**Output**: Full report with color-coded categories and recommendations

### 2. Just Get the Number

```bash
./scripts/health-check.sh --quiet
80
```

**Output**: Single number 0-100 (useful for automation)

### 3. Get JSON Report

```bash
./scripts/health-check.sh --json
```

**Output**: Structured data for CI/CD pipelines

### 4. Detailed Debug Info

```bash
./scripts/health-check.sh --verbose
```

**Output**: Shows what each check is doing

## Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | ✅ Excellent | Keep it up! |
| 70-89 | ✅ Good | Minor improvements possible |
| 50-69 | ⚠️ Needs Work | Address top recommendations |
| 30-49 | ❌ Poor | Prioritize improvements |
| 0-29 | ❌ Critical | Fix issues immediately |

## What Gets Checked?

### 1. Git Health (25 points)
- Is `.gitignore` configured?
- Are Git hooks set up?
- Is CI/CD configured?

### 2. Documentation (20 points)
- Does README exist and is substantial?
- Does CONTRIBUTING guide exist?
- Does LICENSE exist?

### 3. Code Quality (25 points)
- Is linter configured?
- Is code formatter configured?
- Do tests exist?

### 4. Setup (15 points)
- Is `.editorconfig` present?
- Are package manager files valid?

### 5. Security (15 points)
- Is `.env` properly ignored?
- Are there obvious hardcoded secrets?

## Common Issues Fixed

### Issue: "Script not executable"
```bash
chmod +x ./scripts/health-check.sh
./scripts/health-check.sh
```

### Issue: "Command not found"
```bash
bash ./scripts/health-check.sh
```

### Issue: "Takes too long"
```bash
timeout 60 ./scripts/health-check.sh --json
# If Git is slow, optimize with: git gc --aggressive
```

## For CI/CD

### GitHub Actions

```yaml
- name: Health Check
  run: |
    SCORE=$(./scripts/health-check.sh --json | jq '.scores.overall.score')
    echo "Health Score: $SCORE/100"
    [ "$SCORE" -ge 70 ] || exit 1
```

### GitLab CI

```yaml
health-check:
  script:
    - SCORE=$(./scripts/health-check.sh --quiet)
    - echo "Health Score: $SCORE/100"
    - [ "$SCORE" -ge 70 ] || exit 1
```

## Pro Tips

### 1. Watch for Changes
```bash
while sleep 60; do
  clear
  ./scripts/health-check.sh --quiet
done
```

### 2. Track History
```bash
./scripts/health-check.sh --quiet >> health-history.log
tail health-history.log
```

### 3. Export Results
```bash
./scripts/health-check.sh --json > health-report-$(date +%Y%m%d).json
```

### 4. Check Before Commit
```bash
./scripts/health-check.sh --quiet | grep -q '^[7-9][0-9]$' || echo "Consider fixing health issues first"
```

## Files

```
scripts/
├── health-check.sh                # The main script
├── test-health-check.sh           # Run tests
├── HEALTH_CHECK_README.md         # Full documentation
├── USAGE_EXAMPLES.md              # 40+ examples
├── HEALTH_CHECK_QUICKSTART.md     # This file
└── IMPLEMENTATION_SUMMARY.md      # Technical details
```

## Next Steps

1. **Run it**: `./scripts/health-check.sh`
2. **Review results**: Look at recommendations
3. **Fix issues**: Address high-priority items
4. **Integrate**: Add to CI/CD pipeline
5. **Monitor**: Run regularly to track progress

## Questions?

- See: `HEALTH_CHECK_README.md` for comprehensive docs
- See: `USAGE_EXAMPLES.md` for 40+ practical examples
- See: `IMPLEMENTATION_SUMMARY.md` for technical details

## One-Liners

```bash
# Score
./scripts/health-check.sh --quiet

# JSON
./scripts/health-check.sh --json | jq '.'

# Just recommendations
./scripts/health-check.sh --json | jq '.recommendations[]'

# Category scores
./scripts/health-check.sh --json | jq '.scores | to_entries[] | "\(.key): \(.value.percentage)%"'

# In CI: Fail if below 70
[ $(./scripts/health-check.sh --quiet) -ge 70 ] || exit 1
```

---

**Happy checking! 🏥**
