---
id: contributing-guide
version: 1.0.0
category: documentation
description: Standard contribution guidelines for open source projects
language: markdown
dependencies: []
variables:
  - name: PROJECT_NAME
    description: Name of the project
    required: true
  - name: AUTHOR
    description: Project author or maintainer
    required: false
    default: ""
---

# Contributing to ${PROJECT_NAME}

Thank you for your interest in contributing to ${PROJECT_NAME}!

## 🤝 Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Provide constructive feedback
- Welcome newcomers and help them learn

## 🐛 Reporting Issues

Before creating an issue:
1. Search existing issues to avoid duplicates
2. Provide clear reproduction steps
3. Include environment details (OS, version, etc.)

## 💡 Suggesting Features

Feature requests should include:
- Use case and problem it solves
- Proposed solution
- Alternatives considered

## 🔧 Development Setup

\`\`\`bash
# Clone the repository
git clone https://github.com/${AUTHOR}/${PROJECT_NAME}.git
cd ${PROJECT_NAME}

# Install dependencies
npm install

# Run tests
npm test
\`\`\`

## 📝 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch: \`git checkout -b feature/your-feature\`
3. **Make** your changes
4. **Test** your changes: \`npm test\`
5. **Commit** with clear messages
6. **Push** to your fork
7. **Open** a pull request

### Commit Message Format

\`\`\`
type(scope): subject

body

footer
\`\`\`

**Types:**
- \`feat\`: New feature
- \`fix\`: Bug fix
- \`docs\`: Documentation changes
- \`refactor\`: Code refactoring
- \`test\`: Test additions/changes
- \`chore\`: Maintenance tasks

## ✅ Checklist Before Submitting

- [ ] Tests pass locally
- [ ] Code follows project style
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear
- [ ] No unrelated changes included

## 🧪 Testing Guidelines

All contributions should include tests:

\`\`\`bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage
\`\`\`

## 📖 Documentation

Update documentation if your changes:
- Add new features
- Change existing behavior
- Introduce breaking changes

## 🙏 Recognition

Contributors will be recognized in:
- Release notes
- CONTRIBUTORS.md
- Project README

---

**Questions?** Open an issue or reach out to ${AUTHOR}.
