# Health Check

Perform a quick health assessment of your project setup. Provides a scorecard of essential project utilities and configuration quality.

Execute the health check script and display the results:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/health-check.sh"
```

## What This Command Does

1. **Quick scan** of essential project files (< 5 seconds)
2. **Scores each category** (Git, Documentation, CI/CD, Quality)
3. **Calculates overall health score** (0-100)
4. **Identifies critical issues** vs nice-to-haves
5. **Provides actionable next steps**

## Usage

```
/health-check
```

### Detailed Report

```
/health-check --detailed
```

## Health Categories

Each category is scored 0-100:

**Git Health (25%):**
- .gitignore present and comprehensive
- Git hooks configured
- Clean commit history

**Documentation Health (20%):**
- README.md present and complete
- CONTRIBUTING.md exists
- LICENSE file present
- API documentation

**CI/CD Health (25%):**
- Automated testing setup
- Build automation
- Deployment pipeline

**Code Quality Health (20%):**
- Linter configured
- Formatter configured
- Test coverage > 80%

**Setup Health (10%):**
- .editorconfig present
- Package manager configured
- Environment setup documented

## Example Output

```
🏥 Project Health Check

Overall Score: 72/100 (Good)

Git Health: 85/100 ✅
  ✅ .gitignore present (comprehensive)
  ✅ Git hooks configured
  ⚠️  Large files in history (warning)

Documentation Health: 60/100 ⚠️
  ✅ README.md present
  ❌ CONTRIBUTING.md missing
  ✅ LICENSE file present
  ⚠️  README incomplete (missing Usage section)

CI/CD Health: 70/100 ⚠️
  ✅ GitHub Actions configured
  ⚠️  No deployment automation
  ⚠️  Test job could be optimized

Code Quality Health: 75/100 ✅
  ✅ ESLint configured
  ✅ Prettier configured
  ⚠️  Test coverage at 65% (target: 80%)

Setup Health: 80/100 ✅
  ✅ .editorconfig present
  ✅ package.json configured
  ⚠️  No .nvmrc for Node version

Priority Actions:
  1. 🔴 Add CONTRIBUTING.md (critical for open source)
  2. 🟡 Improve test coverage to 80%
  3. 🟡 Complete README Usage section
  4. 🟢 Add .nvmrc for Node version consistency
```

## Health Score Interpretation

**90-100 (Excellent) 🌟:**
- Production-ready setup
- Follows best practices
- Minimal improvements needed

**75-89 (Good) ✅:**
- Solid foundation
- Minor improvements recommended
- Ready for collaboration

**60-74 (Fair) ⚠️:**
- Basic setup complete
- Several improvements needed
- Consider optimizations

**0-59 (Needs Attention) 🔴:**
- Critical gaps exist
- Priority improvements required
- Run `/analyze-project` for details

## Trend Tracking

Track health over time:

```
📈 Health Trend (Last 7 Days)

Day 1: 58/100
Day 3: 65/100  (+7)
Day 5: 72/100  (+7)
Today: 72/100  (+0)

Improvements:
  ✅ Added .gitignore
  ✅ Setup CI/CD
  ✅ Configured linting

Next Goals:
  → Add CONTRIBUTING.md
  → Improve test coverage
```

## Quick Fix Mode

Apply recommended quick fixes:

```
/health-check --quick-fix
```

Automatically applies:
- Missing .editorconfig
- Basic .gitignore (if missing)
- MIT License (with prompt)
- Minimal README (if missing)

## Related Commands

- `/analyze-project` - Detailed analysis
- `/optimize-setup` - Improve existing files
- `/apply-template` - Add missing files
