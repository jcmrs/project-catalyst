# Contributing to Project Catalyst

Thank you for your interest in contributing to Project Catalyst! This document provides guidelines and instructions for contributing to this Claude Code plugin.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Template Contributions](#template-contributions)
- [Code Review Process](#code-review-process)
- [Community](#community)

---

## Code of Conduct

Project Catalyst is committed to providing a welcoming and inclusive environment for all contributors. By participating in this project, you agree to:

- **Be respectful:** Treat all contributors with respect and courtesy
- **Be constructive:** Provide helpful feedback and constructive criticism
- **Be collaborative:** Work together to improve the project
- **Be inclusive:** Welcome contributors of all backgrounds and skill levels

Unacceptable behavior includes harassment, discrimination, or any form of disrespectful conduct. Violations may result in removal from the project.

---

## How to Contribute

### Reporting Issues

Found a bug or have a feature request? Please open an issue on GitHub:

1. **Search existing issues** to avoid duplicates
2. **Use the issue template** (if available)
3. **Provide clear details:**
   - Bug reports: Steps to reproduce, expected vs actual behavior, environment details
   - Feature requests: Use case, proposed solution, alternatives considered

### Suggesting Templates

Want to contribute a new template? Great! Please:

1. **Check existing templates** in `templates/` to avoid duplicates
2. **Open an issue** with template proposal:
   - Template name and category
   - Target languages/frameworks
   - Use case and benefits
   - Example content (optional)
3. **Wait for approval** before implementing

### Submitting Pull Requests

Ready to contribute code? Follow these steps:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/your-feature-name`
3. **Make your changes** (see guidelines below)
4. **Test thoroughly** (see testing requirements)
5. **Commit with clear messages** (see commit guidelines)
6. **Push to your fork:** `git push origin feature/your-feature-name`
7. **Open a pull request** with detailed description

---

## Development Setup

### Prerequisites

- Git
- Node.js 18+ (for testing/validation)
- Claude Code installed
- Basic knowledge of Claude Code plugins

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/project-catalyst.git
cd project-catalyst

# Link to Claude Code plugins directory
# Windows:
mklink /D "%USERPROFILE%\.claude\plugins\project-catalyst" "%CD%"

# macOS/Linux:
ln -s "$(pwd)" "$HOME/.claude/plugins/project-catalyst"

# Verify installation
claude plugin list | grep project-catalyst
```

### Project Structure

```
project-catalyst/
├── docs/adr/              # Architecture Decision Records
├── skills/                # AI Skills (analyzer, generator)
├── templates/             # Template files
├── commands/              # Slash commands
├── hooks/                 # Event hooks
├── scripts/               # Utility scripts
└── tests/                 # Test suite
```

---

## Contribution Guidelines

### Code Style

**General Principles:**
- Follow existing code conventions in the project
- Write clear, self-documenting code
- Keep functions small and focused
- Avoid unnecessary complexity

**Specific Guidelines:**

**JavaScript:**
```javascript
// Use modern ES6+ syntax
const analyzeProject = async (projectPath) => {
  // Clear variable names
  const detectionResults = await detectPatterns(projectPath);

  // Destructuring for clarity
  const { patterns, confidence } = detectionResults;

  return { patterns, confidence };
};

// Error handling with clear messages
if (!sessionId) {
  throw new Error('🚨 ISOLATION ERROR: Session ID required for project isolation');
}
```

**Bash:**
```bash
#!/bin/bash
# Clear script purpose in header
set -e  # Exit on error

# Use descriptive variable names
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"

# Functions for reusability
check_prerequisites() {
  if ! command -v git &> /dev/null; then
    echo "❌ Git not found"
    exit 1
  fi
}
```

**Markdown:**
- Use clear headings (##, ###)
- Include code blocks with language tags
- Add links to related documentation
- Keep line length reasonable (~120 chars)

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(analyzer): add Python-specific pattern detection

Adds detection patterns for:
- Missing requirements.txt
- No pytest config
- Missing virtual environment

Closes #42

---

fix(templates): correct variable substitution in gitignore

Variables were not being replaced due to incorrect regex.
Fixed pattern matching to handle edge cases.

Fixes #38

---

docs(adr): add ADR-007 for testing strategy

Documents comprehensive testing approach including
unit, integration, and E2E test requirements.
```

### Testing Requirements

**All contributions MUST include tests:**

**Unit Tests:**
```javascript
// tests/unit/session-utils.test.js
describe('getProjectSessionId', () => {
  it('should read session ID from file', () => {
    const sessionId = getProjectSessionId();
    expect(sessionId).toMatch(/^session-[a-f0-9-]+$/);
  });

  it('should throw when session ID file missing', () => {
    expect(() => getProjectSessionId()).toThrow('ISOLATION ERROR');
  });
});
```

**Integration Tests:**
```javascript
// tests/integration/analyzer.test.js
describe('Project Analyzer', () => {
  it('should detect missing gitignore', async () => {
    const results = await analyzeProject('./test-fixtures/no-gitignore');
    expect(results.patterns).toContain('missing-gitignore');
  });
});
```

**Template Tests:**
```javascript
// tests/templates/gitignore.test.js
describe('Node.js gitignore template', () => {
  it('should include node_modules', () => {
    const content = readTemplate('git/gitignore/node.gitignore');
    expect(content).toContain('node_modules/');
  });

  it('should support variable substitution', () => {
    const content = applyTemplate('git/gitignore/node.gitignore', {
      PROJECT_NAME: 'test-project'
    });
    expect(content).toContain('test-project');
  });
});
```

**Run tests before submitting:**
```bash
npm test                    # All tests
npm run test:unit           # Unit tests only
npm run test:integration    # Integration tests only
```

### Isolation Requirements (CRITICAL)

**ALL local-memory operations MUST enforce isolation:**

```javascript
// ✅ CORRECT
const params = createIsolatedParams({
  content: analysisData,
  tags: ['project-analysis']
});
await mcp__local_memory__store_memory(params);

// ❌ INCORRECT
await mcp__local_memory__store_memory({
  content: analysisData,
  tags: ['project-analysis']
  // Missing: session_filter_mode, session_id
});
```

**Pre-commit validation will block commits with violations.**

See: [ADR-004: Isolation Enforcement](./docs/adr/004-isolation-enforcement.md)

---

## Template Contributions

### Template Format

All templates must follow standard format:

```yaml
---
id: template-id
version: 1.0.0
category: documentation|git|ci-cd|setup|quality
description: Clear description of template purpose
language: markdown|yaml|json|etc
dependencies: []  # List of required tools/frameworks
variables:
  - name: VARIABLE_NAME
    description: Clear description
    required: true|false
    default: ""  # If not required
---

# Template content with ${VARIABLE} substitution

${PROJECT_NAME} example content
```

### Template Guidelines

1. **Language Agnostic:** Templates should work across languages when possible
2. **Clear Variables:** All variables must be documented with descriptions
3. **Best Practices:** Follow industry-standard best practices
4. **Comments:** Include helpful comments explaining non-obvious sections
5. **Testing:** Include test validating template application

### Template Checklist

Before submitting template PR:

- [ ] Template follows standard format
- [ ] All variables documented
- [ ] Template tested with variable substitution
- [ ] Template linted (if applicable)
- [ ] Test added to `tests/templates/`
- [ ] Documentation updated (if new category)

---

## Code Review Process

### Review Criteria

Pull requests are reviewed for:

1. **Functionality:** Does it work as intended?
2. **Code Quality:** Clear, maintainable, follows conventions?
3. **Tests:** Adequate test coverage?
4. **Isolation:** All local-memory operations enforced?
5. **Documentation:** Changes documented?
6. **Breaking Changes:** Any backward compatibility concerns?

### Review Timeline

- **Initial review:** Within 3 business days
- **Follow-up reviews:** Within 2 business days
- **Merge:** After approval + CI/CD passing

### Addressing Feedback

- Respond to all review comments
- Make requested changes in new commits
- Don't force-push after review started
- Re-request review when ready

---

## Community

### Getting Help

- **GitHub Issues:** Technical questions, bug reports
- **GitHub Discussions:** General questions, ideas (if enabled)
- **Documentation:** Check [README.md](./README.md) and [ADRs](./docs/adr/)

### Recognition

Contributors are recognized in:
- Release notes (significant contributions)
- CONTRIBUTORS.md file (all contributors)
- Project README (major contributors)

---

## License

By contributing to Project Catalyst, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Project Catalyst!** 🎉

Your contributions help make project setup easier for developers worldwide.
