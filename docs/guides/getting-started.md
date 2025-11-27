# Getting Started Guide

Ready to set up your first project with Project Catalyst? This guide will walk you through the setup process step-by-step.

---

## What You'll Learn

By the end of this guide, you'll be able to:

- Run the interactive onboarding wizard
- Apply production-ready templates to your project
- Understand health check results
- Establish best practices for your project type
- Use Project Catalyst commands effectively

**Time Estimate:** 10-15 minutes
**Prerequisites:** [Installation](./installation.md) complete

---

## Overview: How Project Catalyst Works

Project Catalyst provides three main ways to set up your project:

1. **Interactive Onboarding** (`/onboard`) - Guided setup for new projects
2. **Project Analysis** (`/analyze-project`) - Detailed scan of existing projects
3. **Health Checks** (`/health-check`) - Quick project assessment anytime

```
Decision Tree:

Start
  └─ New project?
      ├─ Yes → /onboard (interactive wizard)
      └─ No → Existing project?
          ├─ Has some files → /analyze-project (detailed analysis)
          └─ Quick check → /health-check (5-second scan)
```

---

## Method 1: Interactive Onboarding (Recommended for New Projects)

The onboarding wizard is the best starting point. It asks about your project and applies templates automatically.

### Step 1: Start the Wizard

In Claude Code, run:

```
/onboard
```

Or from the command line:

```bash
bash ~/.claude/plugins/project-catalyst/scripts/setup-wizard.sh
```

### Step 2: Answer Project Questions

The wizard will ask about your project:

**Question 1: Project Name**
```
🚀 Welcome to Project Catalyst!

What is your project name?
> my-awesome-app
```

**Question 2: Project Type**
```
What type of project is this?
  1. Web application (React, Vue, etc.)
  2. CLI tool (command-line utility)
  3. Library/Package (reusable code)
  4. API/Backend service (Node.js, Python, etc.)
  5. Mobile app (React Native, Flutter, etc.)
  6. Other
> 1
```

**Question 3: Programming Language**
```
What is your primary language?
  1. JavaScript/TypeScript
  2. Python
  3. Java
  4. Go
  5. Rust
  6. Ruby
  7. PHP
  8. Other
> 1
```

### Step 3: Select Goals

```
What are your project goals? (select multiple)
  [x] Open source (needs LICENSE, CONTRIBUTING.md)
  [x] CI/CD automation
  [x] Code quality tools
  [ ] Docker deployment
  [ ] Kubernetes deployment
> 1,2,3
```

**What Each Goal Adds:**
- **Open Source:** LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md
- **CI/CD:** GitHub Actions workflows, automated testing
- **Code Quality:** Linter, formatter, test setup
- **Docker:** Dockerfile, Docker Compose
- **Kubernetes:** k8s manifests, deployment configs

### Step 4: Review Recommendations

The wizard shows templates it will apply:

```
📦 Recommended Templates

Based on your selections, we recommend:

Git Configuration:
  ✓ .gitignore (Node.js)
  ✓ Pre-commit hook (linting)
  ✓ GitHub Actions CI workflow
  ✓ GitHub Actions release workflow

Documentation:
  ✓ README.md (comprehensive)
  ✓ CONTRIBUTING.md
  ✓ CODE_OF_CONDUCT.md

Setup:
  ✓ LICENSE (MIT)
  ✓ .editorconfig
  ✓ .nvmrc (Node version)

Code Quality:
  ✓ ESLint configuration
  ✓ Prettier configuration

Total: 13 templates
Estimated time: 2-3 minutes

Proceed with setup? (y/n): y
```

### Step 5: Provide Variables

Templates need some information:

```
📝 Please provide details:

Author name: Jane Smith
Author email: jane@example.com
Project description: A powerful web app for managing tasks
Node version: 20
Test command: npm test
Build command: npm run build
License type: MIT
```

**Common Variables:**
- `AUTHOR`: Your name or organization
- `EMAIL`: Contact email
- `DESCRIPTION`: What your project does
- `LICENSE`: Choose MIT, Apache-2.0, GPL-3.0, ISC, or UNLICENSE
- `TEST_COMMAND`: How to run tests
- `BUILD_COMMAND`: How to build the project

### Step 6: Apply Templates

Watch as templates are applied:

```
🔧 Applying templates...

  ✅ .gitignore
  ✅ .github/workflows/ci.yml
  ✅ .github/workflows/release.yml
  ✅ README.md
  ✅ CONTRIBUTING.md
  ✅ CODE_OF_CONDUCT.md
  ✅ LICENSE
  ✅ .editorconfig
  ✅ .eslintrc.js
  ✅ .prettierrc.json
  ✅ .nvmrc
  ✅ .git/hooks/pre-commit

✅ Setup complete in 45 seconds!
```

### Step 7: Next Steps

```
🎉 Your project is ready!

Next steps:
  1. Review generated files
  2. Initialize git: git init
  3. Install dependencies: npm install
  4. Make first commit: git add . && git commit -m "Initial setup"
  5. Create GitHub repository
  6. Push code: git push -u origin main

Project Health: 95/100 (Excellent)

Run /health-check anytime to verify your setup.
```

---

## Method 2: Analyze Existing Project

If you have an existing project, use `/analyze-project` to get detailed recommendations.

### Using Analyze Project

```
/analyze-project
```

### What Gets Analyzed

The analyzer checks for:

- **Git Setup:** .gitignore, hooks, GitHub Actions workflows
- **Documentation:** README, CONTRIBUTING, LICENSE
- **CI/CD:** Testing, build automation, deployment
- **Code Quality:** Linter, formatter, test coverage
- **Project Files:** package.json, pyproject.toml, etc.

### Example Output

```
🔍 Project Analysis Results

Git Configuration:
  ❌ Missing .gitignore (confidence: high)
     → Recommended: /apply-template git/gitignore/node

  ✅ Git initialized

Documentation:
  ✅ README.md exists
  ⚠️  README incomplete (missing "Usage" section)
     → Recommended: /apply-template documentation/README-comprehensive

  ❌ CONTRIBUTING.md missing
     → Recommended: /apply-template documentation/CONTRIBUTING

CI/CD:
  ❌ No CI/CD configuration (confidence: high)
     → Recommended: /apply-template ci-cd/github-actions/ci-test

Code Quality:
  ✅ ESLint configured
  ❌ No test setup (confidence: medium)
     → Recommended: Add test runner (npm install --save-dev jest)

Priority Actions:
  1. 🔴 Add .gitignore (prevents committing secrets/dependencies)
  2. 🟡 Setup CI/CD workflow (catch bugs early)
  3. 🟡 Add CONTRIBUTING.md (attract contributors)
  4. 🟢 Add usage section to README
```

### Applying Recommendations

The analyzer shows exact commands to apply each template:

```
/apply-template git/gitignore/node
/apply-template ci-cd/github-actions/ci-test
/apply-template documentation/CONTRIBUTING
```

---

## Understanding Health Check Results

The health check gives you a snapshot of your project setup.

### Running Health Check

```
/health-check
```

### Interpreting the Score

```
🏥 Project Health Check

Overall Score: 72/100 (Good)

Git Health: 85/100 ✅
Documentation Health: 60/100 ⚠️
CI/CD Health: 70/100 ⚠️
Code Quality Health: 75/100 ✅
Setup Health: 80/100 ✅
```

**Score Ranges:**

| Score | Status | Meaning |
|-------|--------|---------|
| 90-100 | 🌟 Excellent | Production-ready, follows all best practices |
| 75-89 | ✅ Good | Solid foundation, minor improvements recommended |
| 60-74 | ⚠️ Fair | Basic setup complete, improvements needed |
| 0-59 | 🔴 Needs Attention | Critical gaps, run `/analyze-project` |

### Category Breakdown

**Git Health (25% of score):**
- ✅ .gitignore present and comprehensive
- ✅ Git hooks configured properly
- ⚠️ Clean commit history (no large files)

**Documentation Health (20% of score):**
- ✅ README.md exists and complete
- ❌ CONTRIBUTING.md present
- ✅ LICENSE file included
- ⚠️ API documentation (if applicable)

**CI/CD Health (25% of score):**
- ✅ Automated testing configured
- ✅ Build automation present
- ⚠️ Deployment pipeline (if applicable)

**Code Quality Health (20% of score):**
- ✅ Linter configured and passing
- ✅ Formatter configured
- ⚠️ Test coverage above 80%

**Setup Health (10% of score):**
- ✅ .editorconfig present
- ✅ Package manager configured
- ⚠️ Version managers (.nvmrc, .python-version)

---

## Basic Workflow Example

Here's a typical first-time user workflow:

### Scenario: Starting a New JavaScript Web App

**Step 1: Run Onboarding**
```
/onboard
```

**Step 2: Answer Questions**
- Project name: `task-manager`
- Type: Web application
- Language: JavaScript/TypeScript
- Goals: Open source, CI/CD, Code quality

**Step 3: Provide Details**
- Author: Jane Smith
- Email: jane@example.com
- Description: A collaborative task management application
- Node version: 20

**Step 4: Let It Setup**
```
✅ Applied 13 templates in 45 seconds
```

**Step 5: Review Generated Files**
```bash
# Check what was created
git status

# You should see:
# - .gitignore
# - README.md
# - CONTRIBUTING.md
# - LICENSE
# - .github/workflows/ci.yml
# - .editorconfig
# - .eslintrc.js
# - .prettierrc.json
# - and more!
```

**Step 6: Initialize Git**
```bash
git init
git add .
git commit -m "Initial setup with Project Catalyst"
```

**Step 7: Install Dependencies**
```bash
npm install
```

**Step 8: Check Health**
```
/health-check
```

Expected output:
```
Overall Score: 95/100 (Excellent)

Your project is production-ready!
```

---

## Common Customizations

### Change License Type

If you selected the wrong license during onboarding, apply a different one:

```
/apply-template setup/licenses/MIT      # MIT License
/apply-template setup/licenses/Apache-2 # Apache 2.0
/apply-template setup/licenses/GPL-3    # GPL 3.0
```

### Add Docker Support

Didn't select Docker during onboarding? Easy to add:

```
/apply-template ci-cd/docker/Dockerfile
```

### Customize README

Apply a different README template:

```
/apply-template documentation/README-minimal     # Simple version
/apply-template documentation/README-comprehensive # Full version
```

### Use Template Profiles

Quick setup with pre-defined profiles:

```
/onboard --profile open-source-package
/onboard --profile internal-tool
/onboard --profile mvp
/onboard --profile enterprise
```

---

## Files Created by Onboarding

After onboarding, your project will have:

### Essential Files
- `README.md` - Project overview and documentation
- `LICENSE` - License file (you choose the type)
- `.gitignore` - Prevents committing unwanted files
- `.editorconfig` - Consistent editor settings

### Git & CI/CD
- `.github/workflows/ci.yml` - Automated testing
- `.github/workflows/release.yml` - Release automation
- `.git/hooks/pre-commit` - Pre-commit checks

### Documentation
- `CONTRIBUTING.md` - How to contribute
- `CODE_OF_CONDUCT.md` - Community guidelines

### Code Quality
- `.eslintrc.js` - Linting rules
- `.prettierrc.json` - Code formatting

### Configuration
- `.nvmrc` - Node.js version (if Node project)
- `package.json` - Project metadata and dependencies

---

## Next Steps

### Immediate
1. Review files: `git status`
2. Initialize git: `git init`
3. Install dependencies: `npm install` (or equivalent)

### Soon
1. Create GitHub repository
2. Push code: `git push -u origin main`
3. Enable Actions in repository settings
4. Make first commit with message explaining setup

### Later
1. See [Customization Guide](./customization.md) to create custom templates
2. Set up hooks for your workflow
3. Integrate with CI/CD platform

---

## Troubleshooting Getting Started

### "No templates found"

❌ **Error:** Onboarding can't find templates

**Solution:**
1. Verify installation: See [Installation Guide](./installation.md)
2. Check template directory: `ls -la ~/.claude/plugins/project-catalyst/templates/`
3. Re-run setup wizard: `bash scripts/setup-wizard.sh`

### "Template requires variables but skipped"

❌ **Error:** Template applied without asking for variables

**Solution:**
1. Templates require specific variables
2. Re-apply manually: `/apply-template <template-path>`
3. Provide variables when prompted

### "Health check shows low score after onboarding"

❌ **Error:** Setup complete but health is only 50/100

**Possible Causes:**
1. Test setup not complete (run `npm install && npm test`)
2. Dependencies not installed
3. Some optional templates not applied

**Solution:**
Run `/analyze-project` to see exact gaps and apply missing templates

### "Git not initialized"

❌ **Error:** "fatal: not a git repository"

**Solution:**
```bash
git init
git add .
git commit -m "Initial setup with Project Catalyst"
```

---

## Common Questions

**Q: Can I customize templates during onboarding?**
A: Not during onboarding, but you can apply different versions afterward. See [Customization Guide](./customization.md).

**Q: Can I run onboarding twice?**
A: It's better to run `/analyze-project` on existing projects, but `/onboard --skip` is available to skip categories.

**Q: What if my language isn't listed?**
A: Select "Other" and then manually apply templates that fit your language.

**Q: Can I undo template application?**
A: Templates are regular files. Delete or modify them like any other files in your project.

**Q: Do I need git before onboarding?**
A: No, but you should initialize it immediately after with `git init`.

---

## Learn More

- **[Installation Guide](./installation.md)** - Setup instructions for your platform
- **[Customization Guide](./customization.md)** - Create and modify templates
- **[Troubleshooting Guide](./troubleshooting.md)** - Common issues and solutions
- **[Command Reference](../commands/)** - Detailed command documentation

---

**Ready to set up a project?** Start with `/onboard` and follow the prompts!

For questions, visit our [GitHub Discussions](https://github.com/jcmrs/project-catalyst/discussions) or [Issues](https://github.com/jcmrs/project-catalyst/issues).
