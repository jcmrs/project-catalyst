# Customization Guide

Learn how to create custom templates, configure hooks, and extend Project Catalyst for your unique workflow.

---

## Overview

Project Catalyst is highly customizable. You can:

- Create custom templates for your team's standards
- Configure hooks to automate your workflow
- Set up custom commands
- Define advanced isolation rules
- Build template bundles for specific project types

---

## Creating Custom Templates

### Template Structure

Templates are simple text files with variables that get substituted.

**Template Format:**
```
Template files can contain:
- Regular text/code
- Variables: {{VARIABLE_NAME}}
- Comments (language-specific)
- Conditional sections (optional)
```

**Template Location:**
```
~/.claude/plugins/project-catalyst/templates/
├── category/
│   └── subcategory/
│       └── template-file
```

### Example: Create a Custom .gitignore

**Step 1: Create Template File**

```bash
# Create custom templates directory
mkdir -p ~/.claude/plugins/project-catalyst/templates/custom/gitignore

# Create your template
cat > ~/.claude/plugins/project-catalyst/templates/custom/gitignore/monorepo.gitignore << 'EOF'
# Project Catalyst Custom Template for Monorepo
# Project: {{PROJECT_NAME}}
# Author: {{AUTHOR}}

# Dependencies
node_modules/
/.pnp
.pnp.js
venv/
__pycache__/
*.egg-info/

# Testing
coverage/
.nyc_output/
.pytest_cache/

# Build outputs
dist/
build/
.next/
out/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
.DS_Store?

# Workspace
lerna-debug.log
npm-debug.log*
yarn-debug.log*

# Monorepo specific
packages/*/dist
apps/*/build
EOF
```

**Step 2: Use Your Custom Template**

```bash
# Apply the template
/apply-template custom/gitignore/monorepo
```

You'll be prompted for variables:
```
AUTHOR: Your Company
PROJECT_NAME: My Monorepo
```

The template variables will be substituted and the file created.

### Template Variables Reference

Built-in variables automatically available:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{AUTHOR}}` | Project author | John Smith |
| `{{AUTHOR_EMAIL}}` | Author email | john@example.com |
| `{{PROJECT_NAME}}` | Project name | my-app |
| `{{PROJECT_SLUG}}` | URL-safe project name | my-app |
| `{{DESCRIPTION}}` | Project description | A task manager |
| `{{LICENSE}}` | License type | MIT |
| `{{YEAR}}` | Current year | 2025 |
| `{{VERSION}}` | Version number | 1.0.0 |
| `{{LANGUAGE}}` | Primary language | JavaScript |
| `{{LANGUAGE_VERSION}}` | Language version | Node 20 |

### Creating a Template with Multiple Variables

**Example: Custom ESLint Config**

```javascript
// ~/.claude/plugins/project-catalyst/templates/custom/linting/eslint-strict.js
// Custom ESLint config for {{PROJECT_NAME}}
// Created by: {{AUTHOR}} <{{AUTHOR_EMAIL}}>

module.exports = {
  root: true,
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
  },
  env: {
    node: true,
    es2022: true,
    {{#TESTING}}jest: true,{{/TESTING}}
  },
  extends: [
    'eslint:recommended',
    {{#STRICT}}'plugin:security/recommended',{{/STRICT}}
  ],
  rules: {
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'no-debugger': 'error',
    'prefer-const': 'error',
    'no-var': 'error',
  },
};
```

Apply it:
```
/apply-template custom/linting/eslint-strict
```

Prompted variables:
```
AUTHOR: Jane Smith
AUTHOR_EMAIL: jane@example.com
PROJECT_NAME: strict-linting-project
TESTING: yes (for jest environment)
STRICT: yes (for security rules)
```

### Best Practices for Templates

✅ **DO:**
- Use meaningful variable names
- Include comments explaining the purpose
- Test template before sharing
- Document required variables
- Keep templates focused and reusable

❌ **DON'T:**
- Hard-code project-specific values
- Use overly complex variable patterns
- Mix multiple purposes in one template
- Forget to document template requirements
- Create templates with absolute paths

---

## Configuring Hooks

Hooks automate tasks in your workflow. Project Catalyst supports three hook types:

### Hook Types

**SessionStart**
- Runs when Claude Code session starts
- Use for: Setup checks, reminders, health reports

**PostToolUse**
- Runs after you use specific tools
- Use for: Validation, cleanup, notifications

**PreCommit**
- Runs before git commits
- Use for: Linting, testing, verification

### Hook Configuration

Hooks are defined in `hooks/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "**",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/check-analyzed.sh",
            "description": "Check if project analyzed on session start"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-template.sh",
            "args": ["${FILE_PATH}"],
            "description": "Validate files after writing"
          }
        ]
      }
    ],
    "PreCommit": [
      {
        "matcher": "**",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-isolation.sh",
            "description": "Verify isolation before committing"
          }
        ]
      }
    ]
  }
}
```

### Creating Custom Hooks

**Step 1: Create a Hook Script**

```bash
# Create custom script
mkdir -p ~/.claude/plugins/project-catalyst/hooks/custom

cat > ~/.claude/plugins/project-catalyst/hooks/custom/pre-test.sh << 'EOF'
#!/bin/bash
# Pre-test validation hook

PROJECT_DIR="${CLAUDE_PROJECT_DIR}"

echo "Running pre-test validation..."

# Check for test files
if [ ! -f "$PROJECT_DIR/package.json" ]; then
    echo "❌ package.json not found"
    exit 1
fi

# Check test script exists
if ! grep -q '"test"' "$PROJECT_DIR/package.json"; then
    echo "⚠️  No test script found in package.json"
    exit 0
fi

echo "✅ Pre-test validation passed"
exit 0
EOF

chmod +x ~/.claude/plugins/project-catalyst/hooks/custom/pre-test.sh
```

**Step 2: Register the Hook**

Edit `hooks/hooks.json`:

```json
{
  "hooks": {
    "PreCommit": [
      {
        "matcher": "**",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/custom/pre-test.sh",
            "description": "Validate tests before commit"
          }
        ]
      }
    ]
  }
}
```

### Hook Environment Variables

Available in hook scripts:

| Variable | Description |
|----------|-------------|
| `${CLAUDE_PROJECT_DIR}` | Current project directory |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin root directory |
| `${FILE_PATH}` | Path of modified file (PostToolUse) |
| `${TOOL_NAME}` | Name of tool used (PostToolUse) |

### Example Hooks

**Health Check on Session Start**

```bash
#!/bin/bash
# hooks/custom/session-health.sh

PROJECT_DIR="${CLAUDE_PROJECT_DIR}"

echo "🏥 Running health check on session start..."

bash "${CLAUDE_PLUGIN_ROOT}/scripts/health-check.sh" "$PROJECT_DIR"
```

Register in `hooks.json`:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "**",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/custom/session-health.sh"
          }
        ]
      }
    ]
  }
}
```

**Format Check Before File Write**

```bash
#!/bin/bash
# hooks/custom/format-check.sh

FILE_PATH="${1}"

if [[ "$FILE_PATH" == *.js ]]; then
    echo "Checking JavaScript formatting..."
    npx prettier --check "$FILE_PATH" || {
        echo "⚠️  File doesn't match prettier format"
        npx prettier --write "$FILE_PATH"
        echo "✅ Auto-formatted"
    }
fi
```

Register:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/custom/format-check.sh",
            "args": ["${FILE_PATH}"]
          }
        ]
      }
    ]
  }
}
```

---

## Template Variable Substitution

### Manual Substitution

When you apply a template, Project Catalyst prompts for variables:

```bash
/apply-template custom/documentation/api-doc

# Prompts:
Enter PROJECT_NAME: my-api
Enter AUTHOR: Jane Smith
Enter API_VERSION: v1
```

### Conditional Substitution

Use conditional sections in templates:

```markdown
# {{PROJECT_NAME}} API Documentation

This is the official API documentation.

{{#INCLUDE_EXAMPLES}}
## Examples

Here are usage examples:
{{/INCLUDE_EXAMPLES}}

{{#BETA_WARNING}}
⚠️ This API is in BETA and may change
{{/BETA_WARNING}}
```

When applying:
```
INCLUDE_EXAMPLES: yes
BETA_WARNING: no
```

### Default Values

Set defaults for variables:

```bash
# In template file comments
# AUTHOR = "Your Company"
# LANGUAGE = "JavaScript"
# VERSION = "1.0.0"
```

---

## Adding Custom Commands

Extend Project Catalyst with your own commands.

### Creating a Custom Command

**Step 1: Create Command File**

```bash
mkdir -p ~/.claude/plugins/project-catalyst/commands/custom

cat > ~/.claude/plugins/project-catalyst/commands/custom/my-lint-fix.md << 'EOF'
# My Lint Fix

Auto-fix linting issues in your project.

Execute the script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/commands/custom/scripts/lint-fix.sh"
```

## Usage

```
/my-lint-fix
```

## What It Does

1. Runs ESLint with --fix flag
2. Fixes formatting with Prettier
3. Reports fixes applied
4. Runs tests to verify

## Output

```
🔧 Running lint fixes...
  ✅ ESLint fixed 12 issues
  ✅ Prettier formatted 8 files
  ✅ All tests pass

Clean!
```
EOF
```

**Step 2: Create Implementation Script**

```bash
mkdir -p ~/.claude/plugins/project-catalyst/commands/custom/scripts

cat > ~/.claude/plugins/project-catalyst/commands/custom/scripts/lint-fix.sh << 'EOF'
#!/bin/bash
set -e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo "🔧 Running lint fixes..."

# ESLint fix
if [ -f "$PROJECT_DIR/.eslintrc.js" ]; then
    echo "Running ESLint..."
    npx eslint --fix "$PROJECT_DIR/src" "$PROJECT_DIR/tests" 2>/dev/null || true
    echo "  ✅ ESLint fixed issues"
fi

# Prettier format
if [ -f "$PROJECT_DIR/.prettierrc" ]; then
    echo "Running Prettier..."
    npx prettier --write "$PROJECT_DIR/src" "$PROJECT_DIR/tests" 2>/dev/null || true
    echo "  ✅ Prettier formatted files"
fi

echo "✅ Lint fixes complete"
EOF

chmod +x ~/.claude/plugins/project-catalyst/commands/custom/scripts/lint-fix.sh
```

---

## Advanced Isolation Configuration

### Understanding Isolation

Project Catalyst isolates each project's data using local-memory. This prevents context contamination.

### Isolation Enforcement

Edit `scripts/validate-isolation.sh` to add custom rules:

```bash
#!/bin/bash
# Custom isolation validation

PROJECT_DIR="${1:-$(pwd)}"

echo "🔒 Validating isolation..."

# Rule 1: No shared memory between projects
# Check that all local-memory operations use PROJECT_DIR
if grep -r "memory:read" "$PROJECT_DIR" 2>/dev/null | grep -v PROJECT_DIR; then
    echo "❌ Memory operation without PROJECT_DIR isolation"
    exit 1
fi

# Rule 2: No cross-project file access
if grep -r "\.\.\/" "$PROJECT_DIR"/.claude 2>/dev/null; then
    echo "❌ Relative path goes outside project"
    exit 1
fi

echo "✅ Isolation valid"
exit 0
```

### Isolation Best Practices

✅ **DO:**
- Use `${PROJECT_DIR}` for all file paths
- Prefix memory keys with project identifier
- Validate paths before accessing
- Document isolation assumptions

❌ **DON'T:**
- Use absolute paths outside project
- Share memory across projects
- Store project data in global locations
- Trust user input without validation

---

## Best Practices for Customization

### 1. Organize Custom Files

```
~/.claude/plugins/project-catalyst/
├── templates/
│   ├── custom/
│   │   ├── linting/
│   │   └── documentation/
│   └── (built-in templates)
├── hooks/
│   ├── custom/
│   │   ├── pre-test.sh
│   │   └── format-check.sh
│   └── hooks.json
└── commands/
    ├── custom/
    │   ├── my-lint-fix.md
    │   └── scripts/
    └── (built-in commands)
```

### 2. Document Your Customizations

Create a `CUSTOMIZATION.md` in your plugin directory:

```markdown
# Project Catalyst Customizations

## Custom Templates

### custom/linting/eslint-strict
- Purpose: Strict ESLint configuration
- Variables: AUTHOR, PROJECT_NAME, STRICT
- Usage: `/apply-template custom/linting/eslint-strict`

## Custom Hooks

### pre-test.sh
- Trigger: PreCommit
- Purpose: Validate tests before commit
- Actions: Checks test setup exists

## Custom Commands

### /my-lint-fix
- Purpose: Auto-fix linting issues
- Actions: ESLint + Prettier + test
```

### 3. Test Before Using

Always test custom templates and hooks:

```bash
# Test template substitution
bash scripts/validate-template-format.sh templates/custom/mytemplate

# Test hook execution
bash hooks/custom/pre-test.sh /path/to/test/project

# Test command
bash commands/custom/scripts/my-lint-fix.sh
```

### 4. Version Control

Commit customizations to your project:

```bash
# Add custom templates/hooks to git
git add templates/custom
git add hooks/custom
git add commands/custom

git commit -m "Add custom Project Catalyst templates and hooks"
```

### 5. Share with Team

Create a team profile:

```bash
# Create shared profile
/onboard --profile my-team-setup --save

# Teammates use it:
/onboard --profile my-team-setup
```

---

## Troubleshooting Customization

### "Template variables not substituting"

❌ **Error:** `{{VARIABLE}}` appears in output

**Solutions:**
1. Check variable names match exactly (case-sensitive)
2. Ensure variable is provided during application
3. Verify template uses double-braces: `{{VARIABLE}}`

### "Hook not executing"

❌ **Error:** Hook script doesn't run

**Solutions:**
1. Make script executable: `chmod +x hooks/custom/script.sh`
2. Test script manually: `bash hooks/custom/script.sh`
3. Check hook registration in `hooks.json`
4. Verify matcher pattern is correct

### "Command not showing in Claude Code"

❌ **Error:** Custom command doesn't appear

**Solutions:**
1. Verify command file is in `commands/custom/`
2. File must end with `.md`
3. Restart Claude Code to reload plugins
4. Check command format matches built-in examples

### "Isolation validation failing"

❌ **Error:** Validation prevents commits

**Solutions:**
1. Check paths use `${PROJECT_DIR}` prefix
2. Verify no symlinks outside project
3. Test isolation script: `bash scripts/validate-isolation.sh $(pwd)`

---

## Examples

### Example 1: Docker Template

Create a template for Docker setup:

```dockerfile
# {{PROJECT_NAME}}/Dockerfile
# Created by {{AUTHOR}}

FROM {{BASE_IMAGE}}:{{BASE_VERSION}}

WORKDIR /app

COPY package.json .
RUN {{PACKAGE_MANAGER}} install

COPY . .

{{#BUILD_STEP}}
RUN {{BUILD_COMMAND}}
{{/BUILD_STEP}}

EXPOSE {{PORT}}

CMD ["{{START_COMMAND}}"]
```

Apply:
```
/apply-template custom/docker/my-dockerfile
```

### Example 2: API Documentation Template

```markdown
# {{PROJECT_NAME}} API Reference

**Version:** {{API_VERSION}}
**Author:** {{AUTHOR}}

## Base URL

```
{{API_URL}}
```

## Authentication

{{#AUTH_TYPE}}
The API uses {{AUTH_TYPE}} authentication.
{{/AUTH_TYPE}}

## Endpoints

(Generated endpoints will go here)
```

### Example 3: Team Hook for Code Review

```bash
#!/bin/bash
# hooks/custom/check-code-review.sh

# Ensure code review approval before commit

if git log -1 --format=%B | grep -q "Co-authored-by:"; then
    echo "✅ Code review detected"
    exit 0
else
    echo "⚠️  No code review found"
    echo "Add co-author with: git commit --co-authored-by='Name <email>'"
    exit 1
fi
```

---

## Learn More

- **[Getting Started](./getting-started.md)** - Basic setup walkthrough
- **[Troubleshooting](./troubleshooting.md)** - Common issues
- **[Installation](./installation.md)** - Setup instructions

---

**Ready to customize?** Start with a simple template and build from there!
