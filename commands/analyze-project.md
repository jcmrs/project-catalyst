# Analyze Project

Analyze the current project structure to detect missing utilities, configuration files, and best practices. Provides intelligent recommendations for templates and improvements.

## What This Command Does

1. **Scans project structure** for common files and patterns
2. **Detects missing utilities** (gitignore, CI/CD, documentation, etc.)
3. **Assigns confidence scores** to each detection
4. **Recommends templates** from Project Catalyst library
5. **Prioritizes recommendations** by severity and impact

## Usage

Simply invoke this command:

```
/analyze-project
```

## What Gets Analyzed

**Git Configuration:**
- .gitignore presence and quality
- Git hooks setup
- GitHub Actions workflows

**Documentation:**
- README.md existence and completeness
- CONTRIBUTING.md
- LICENSE file

**CI/CD:**
- GitHub Actions workflows
- Docker configuration
- Build scripts

**Code Quality:**
- Linter configuration (ESLint, Pylint, etc.)
- Formatter configuration (Prettier, Black, etc.)
- Test setup

**Setup Files:**
- .editorconfig
- Package manager files
- Environment configuration

## Output

The analysis provides:

- **Detection results** with confidence scores (high/medium/low)
- **Recommended templates** to address gaps
- **Priority order** for implementation
- **One-command application** for each recommended template

## Example Output

```
🔍 Project Analysis Results

Git Configuration:
  ❌ Missing .gitignore (confidence: high)
     → Recommended: /apply-template git/gitignore/node

  ✅ Git hooks configured

Documentation:
  ⚠️  README.md exists but minimal (confidence: medium)
     → Recommended: /apply-template documentation/README-comprehensive

CI/CD:
  ❌ No CI/CD configuration (confidence: high)
     → Recommended: /apply-template ci-cd/github-actions/ci-test

Priority Actions:
  1. Add .gitignore
  2. Setup CI/CD workflow
  3. Enhance README documentation
```

## Related Commands

- `/apply-template` - Apply recommended templates
- `/optimize-setup` - Optimize existing configuration
- `/health-check` - Quick project health assessment
