# Onboard

Interactive onboarding wizard for setting up a new project with Project Catalyst. Asks questions about your project and applies appropriate templates automatically.

Execute the setup wizard:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup-wizard.sh"
```

## What This Command Does

1. **Asks questions** about your project (language, type, goals)
2. **Recommends template bundle** based on answers
3. **Prompts for variables** (project name, author, etc.)
4. **Applies multiple templates** in one session
5. **Verifies setup** and provides next steps

## Usage

```
/onboard
```

## Onboarding Flow

### Step 1: Project Information

```
🚀 Welcome to Project Catalyst Onboarding!

Let's set up your project with best practices.

What is your project name?
> my-awesome-project

What type of project is this?
  1. Web application
  2. CLI tool
  3. Library/Package
  4. API/Backend service
> 1

What is your primary language?
  1. JavaScript/TypeScript
  2. Python
  3. Java
  4. Go
  5. Rust
  6. Other
> 1
```

### Step 2: Project Goals

```
What are your goals for this project? (select multiple)
  [x] Open source (needs LICENSE, CONTRIBUTING.md)
  [x] CI/CD automation
  [x] Code quality tools
  [ ] Docker deployment
> 1,2,3

Do you plan to publish to npm?
> Yes
```

### Step 3: Template Recommendations

```
📦 Recommended Templates

Based on your selections, we recommend:

Git:
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

Quality:
  ✓ ESLint configuration
  ✓ Prettier configuration

Total: 11 templates

Proceed with setup? (y/n): y
```

### Step 4: Variable Collection

```
📝 Please provide some details:

Author name: jcmrs
Author email: jcmrs@example.com
Project description: A tool for awesome things
Node version: 20
Test command: npm test
Build command: npm run build
```

### Step 5: Template Application

```
🔧 Applying templates...

  ✅ .gitignore (Node.js)
  ✅ .github/workflows/ci.yml
  ✅ .github/workflows/release.yml
  ✅ README.md
  ✅ CONTRIBUTING.md
  ✅ LICENSE (MIT)
  ✅ .editorconfig
  ✅ .eslintrc.js
  ✅ .prettierrc
  ✅ .git/hooks/pre-commit

✅ Project setup complete!
```

### Step 6: Next Steps

```
🎉 Your project is ready!

Next steps:
  1. Review generated files
  2. Install dependencies: npm install
  3. Initialize git (if not done): git init
  4. Make first commit: git add . && git commit -m "Initial setup"
  5. Create GitHub repository
  6. Push code: git push -u origin main

Project Health: 95/100 (Excellent)

Run /health-check anytime to verify your setup.
```

## Onboarding Profiles

Quick setup with predefined profiles:

**Open Source Package:**
```
/onboard --profile oss-package
```
Includes: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, comprehensive README, CI/CD

**Internal Tool:**
```
/onboard --profile internal-tool
```
Includes: Minimal README, basic gitignore, CI workflow

**Startup MVP:**
```
/onboard --profile mvp
```
Includes: Essential files only, optimized for speed

**Enterprise Project:**
```
/onboard --profile enterprise
```
Includes: Full documentation, security scanning, compliance tools

## Customization

Skip specific categories:

```
/onboard --skip documentation
/onboard --skip ci-cd
```

Add specific templates:

```
/onboard --add docker --add kubernetes
```

## Save Configuration

Save your choices for future projects:

```
Save this configuration as a profile? (y/n): y
Profile name: my-web-app-setup

✅ Saved as "my-web-app-setup"

Use in future: /onboard --profile my-web-app-setup
```

## Related Commands

- `/analyze-project` - Check existing project
- `/health-check` - Verify setup quality
- `/apply-template` - Add individual templates
