# Project Catalyst User Guides

Welcome to Project Catalyst user documentation! These guides will help you install, set up, and customize the plugin for your workflow.

---

## Quick Navigation

### New Users

Start here if you're just getting started:

1. **[Installation Guide](./installation.md)** (10-15 minutes)
   - Prerequisites and system requirements
   - Step-by-step installation for Windows, macOS, Linux
   - Platform-specific notes and troubleshooting
   - Verification checklist

2. **[Getting Started Guide](./getting-started.md)** (15-20 minutes)
   - Interactive onboarding walkthrough
   - Understanding health checks
   - Basic workflow example
   - Common customizations

### Existing Users

Deepen your knowledge with these guides:

3. **[Customization Guide](./customization.md)** (30-45 minutes)
   - Creating custom templates
   - Configuring hooks for automation
   - Template variables and substitution
   - Advanced isolation configuration
   - Team best practices

4. **[Troubleshooting Guide](./troubleshooting.md)** (as needed)
   - Common issues and solutions
   - Debugging techniques
   - Performance optimization
   - Getting support

---

## Documentation Structure

### Installation Guide
**Purpose:** Get Project Catalyst up and running

**Topics:**
- Prerequisites (Claude Code, Git, Bash)
- Installation steps (clone, setup wizard, verify)
- Platform-specific guides (Windows Git Bash, macOS, Linux)
- Common installation issues and fixes
- Next steps after installation

**Best for:** First-time users, team leads setting up infrastructure

### Getting Started Guide
**Purpose:** Set up your first project with best practices

**Topics:**
- Overview of how Project Catalyst works
- Interactive onboarding (`/onboard`)
- Project analysis (`/analyze-project`)
- Understanding health checks
- Basic workflow walkthrough
- Common customizations
- FAQ for common questions

**Best for:** New projects, learning the plugin, quick reference

### Customization Guide
**Purpose:** Extend Project Catalyst for your specific needs

**Topics:**
- Creating custom templates
- Configuring hooks (SessionStart, PostToolUse, PreCommit)
- Template variables and substitution
- Adding custom commands
- Advanced isolation enforcement
- Team best practices
- Real-world examples
- Sharing customizations

**Best for:** Advanced users, teams with specific standards, automation

### Troubleshooting Guide
**Purpose:** Solve problems quickly and efficiently

**Topics:**
- Project not analyzed errors
- Template validation failures
- Isolation enforcement issues
- Hook execution problems
- Performance optimization
- Debugging techniques
- Support and help resources

**Best for:** When things go wrong, optimization, diagnostics

---

## Common Workflows

### "I want to set up a new project"

1. Read: [Getting Started Guide](./getting-started.md)
2. Run: `/onboard`
3. Follow interactive prompts
4. Review: Generated files and next steps

**Estimated time:** 10-15 minutes

### "I have an existing project and want to improve it"

1. Read: [Getting Started Guide - Analyze Method](./getting-started.md#method-2-analyze-existing-project)
2. Run: `/analyze-project`
3. Review: Recommendations
4. Apply: Recommended templates
5. Check: `/health-check`

**Estimated time:** 15-30 minutes

### "I need to customize templates for my team"

1. Read: [Customization Guide](./customization.md)
2. Create: Custom template files
3. Test: Template substitution
4. Share: Template bundle with team
5. Document: Usage and variables

**Estimated time:** 30-60 minutes

### "Hooks and automation aren't working"

1. Check: [Troubleshooting - Hook Execution Problems](./troubleshooting.md#hook-execution-problems)
2. Run: Diagnostic commands
3. Fix: Using provided solutions
4. Test: Hook execution manually

**Estimated time:** 10-30 minutes

### "I'm experiencing performance issues"

1. Check: [Troubleshooting - Performance Issues](./troubleshooting.md#performance-issues)
2. Run: Provided diagnostics
3. Optimize: Following recommendations
4. Verify: Performance improvements

**Estimated time:** 15-45 minutes

---

## Key Concepts

### Templates

Pre-built, production-ready files for common project needs.

**Categories:**
- Git: .gitignore, hooks, workflows
- Documentation: README, CONTRIBUTING, LICENSE
- CI/CD: GitHub Actions, Docker, Kubernetes
- Quality: Linting, formatting, testing
- Setup: Configuration files, version managers

**Usage:** `/apply-template <template-path>`

### Commands

Interactive commands for project setup and analysis.

**Main commands:**
- `/onboard` - Interactive setup wizard
- `/analyze-project` - Detailed project analysis
- `/health-check` - Quick project assessment
- `/apply-template` - Apply individual templates

### Hooks

Automated tasks that run on specific events.

**Types:**
- SessionStart: Run when Claude Code starts
- PostToolUse: Run after using specific tools
- PreCommit: Run before git commits

### Health Check

Quick assessment of project setup quality.

**Scores 0-100:**
- 90-100: Excellent (production-ready)
- 75-89: Good (solid foundation)
- 60-74: Fair (improvements needed)
- 0-59: Needs attention (run analyze)

### Isolation

Strict project separation to prevent context contamination.

**Features:**
- Per-project memory storage
- No cross-project access
- Path validation
- Runtime enforcement

---

## Features at a Glance

| Feature | Installation | Getting Started | Customization | Troubleshooting |
|---------|--------------|-----------------|---|---|
| Prerequisites | ✓ | - | - | ✓ |
| Installation steps | ✓ | - | - | ✓ |
| Platform guides | ✓ | - | - | - |
| First-time setup | - | ✓ | - | ✓ |
| Template usage | - | ✓ | ✓ | ✓ |
| Health checks | - | ✓ | - | ✓ |
| Custom templates | - | - | ✓ | ✓ |
| Hooks & automation | - | - | ✓ | ✓ |
| Advanced config | - | - | ✓ | ✓ |
| Troubleshooting | ✓ | ✓ | ✓ | ✓ |
| Performance | - | - | ✓ | ✓ |

---

## Guide Statistics

**Installation Guide**
- Length: 418 lines (~8.4 KB)
- Sections: 8 major + 20 subsections
- Code examples: 25+
- Troubleshooting topics: 8

**Getting Started Guide**
- Length: 587 lines (~14 KB)
- Sections: 8 major + 15 subsections
- Workflows: 3 complete examples
- Questions answered: 6

**Customization Guide**
- Length: 818 lines (~16 KB)
- Sections: 6 major + 25 subsections
- Code examples: 30+
- Best practices: 15+

**Troubleshooting Guide**
- Length: 916 lines (~19 KB)
- Issues covered: 7 major + 35 subtopics
- Solutions per issue: 3-6
- Code examples: 40+

**Total: 2,739 lines (~57 KB) of comprehensive documentation**

---

## How to Use These Guides

### Reading Order

**For first-time users:**
1. Installation Guide (complete)
2. Getting Started Guide (complete)
3. Customization Guide (as needed)
4. Troubleshooting Guide (when issues arise)

**For experienced users:**
1. Customization Guide (specific sections)
2. Troubleshooting Guide (when needed)
3. Installation Guide (reference only)

### Finding Information

**By topic:**
- Use document section headers (Ctrl+F)
- Check table of contents at guide start
- Follow cross-references between guides

**By problem:**
- Start with [Troubleshooting Guide](./troubleshooting.md)
- Use issue descriptions to find solutions
- Follow diagnostic steps provided

**By workflow:**
- See "Common Workflows" section above
- Follow the guide recommendations
- Complete listed tasks in order

### Code Examples

All guides include practical examples:

- **Installation Guide:** Installation commands for each platform
- **Getting Started Guide:** Complete workflow walkthrough
- **Customization Guide:** Template and hook examples
- **Troubleshooting Guide:** Diagnostic and fix commands

You can copy-paste commands directly, or adapt them for your environment.

---

## Cross-References

Quick links to related topics:

### Installation
- [Installation - Windows](./installation.md#windows-git-bash)
- [Installation - macOS](./installation.md#macos)
- [Installation - Linux](./installation.md#linux)
- [Installation - Troubleshooting](./installation.md#troubleshooting-installation)

### Getting Started
- [Getting Started - Onboarding](./getting-started.md#method-1-interactive-onboarding-recommended-for-new-projects)
- [Getting Started - Analysis](./getting-started.md#method-2-analyze-existing-project)
- [Getting Started - Health Checks](./getting-started.md#understanding-health-check-results)
- [Getting Started - FAQ](./getting-started.md#common-questions)

### Customization
- [Customization - Templates](./customization.md#creating-custom-templates)
- [Customization - Hooks](./customization.md#configuring-hooks)
- [Customization - Commands](./customization.md#adding-custom-commands)
- [Customization - Isolation](./customization.md#advanced-isolation-configuration)

### Troubleshooting
- [Troubleshooting - Analysis Errors](./troubleshooting.md#project-not-analyzed-error)
- [Troubleshooting - Template Issues](./troubleshooting.md#template-validation-failing)
- [Troubleshooting - Hooks](./troubleshooting.md#hook-execution-problems)
- [Troubleshooting - Performance](./troubleshooting.md#performance-issues)

---

## Getting Help

### Self-Help Resources

1. **Check this README** for overview
2. **Use Ctrl+F** in guides to search
3. **Follow Common Workflows** for step-by-step guidance
4. **Run diagnostic commands** from troubleshooting guide

### When You Need More Help

1. **GitHub Issues** - Report bugs and feature requests
   - [Open an issue](https://github.com/jcmrs/project-catalyst/issues)
   - Include diagnostic information from guide

2. **GitHub Discussions** - Ask questions
   - [Start a discussion](https://github.com/jcmrs/project-catalyst/discussions)
   - Share your setup and what you're trying to do

3. **Email** - Contact project maintainer
   - jcmrs@users.noreply.github.com
   - Include guide reference and error output

---

## Feedback and Improvements

These guides are actively maintained. If you:

- Find an error or typo
- Have a better explanation
- Want to add a section
- Have a question not covered

**Please open an issue or discussion on GitHub!**

Your feedback helps make Project Catalyst better for everyone.

---

## Document Versions

| Guide | Version | Last Updated | Status |
|-------|---------|--------------|--------|
| Installation | 1.0 | 2025-11-27 | Stable |
| Getting Started | 1.0 | 2025-11-27 | Stable |
| Customization | 1.0 | 2025-11-27 | Stable |
| Troubleshooting | 1.0 | 2025-11-27 | Stable |

---

## Related Documentation

Beyond user guides:

- **[Main README](../../README.md)** - Project overview
- **[Master Plan](../../MASTER-PLAN.md)** - Development roadmap
- **[Commands](../../commands/)** - Detailed command reference
- **[Architecture Decisions](../adr/)** - Design documentation
- **[API Documentation](../api/)** - Technical reference

---

**Start with [Installation Guide](./installation.md) or [Getting Started Guide](./getting-started.md) based on your situation!**

For questions, visit [GitHub Discussions](https://github.com/jcmrs/project-catalyst/discussions).
