# ADR-003: Template System - Phased Expansion Strategy

**Status:** Accepted
**Date:** 2025-11-27
**Deciders:** Project Catalyst Team
**Technical Story:** Template Library Design (40+ Templates, Phased Delivery)

---

## Context

### Background

Project Catalyst provides production-ready templates for common project utilities. Templates must be language-agnostic, well-tested, and easy to apply while avoiding overwhelming users with too many options at once.

### Requirements

1. **Phased Expansion:** Start with 15 MVP templates, expand to 40+ over time
2. **Language Agnostic:** Work across Node, Python, Java, Go, Rust, etc.
3. **Variable Substitution:** Support ${VARIABLE} placeholders
4. **Validation:** Ensure template quality and proper substitution
5. **Maintainability:** Community contributions encouraged
6. **Progressive Loading:** Don't load all templates into context at once

---

## Decision

### Chosen Approach: Three-Phase Template Expansion with Standard Format

**Phase 1 (Weeks 3-4): 15 MVP Templates**
Prove core value with essential templates covering 80% of common needs.

**Phase 2 (Weeks 5-8): Expand to 25 Templates**
Add variants and advanced configurations based on Phase 1 feedback.

**Phase 3 (Weeks 9-12): Complete 40+ Templates**
Specialized templates for quality tools, security, testing frameworks.

### Template Structure

**Directory Organization:**
```
templates/
├── git/                    # 8 templates
│   ├── gitignore/
│   │   ├── node.gitignore
│   │   ├── python.gitignore
│   │   ├── java.gitignore
│   │   ├── go.gitignore
│   │   └── rust.gitignore
│   ├── hooks/
│   │   ├── pre-commit
│   │   └── pre-push
│   └── workflows/
│       ├── ci-test.yml
│       └── release.yml
│
├── documentation/          # 10 templates
│   ├── README-comprehensive.md
│   ├── README-minimal.md
│   ├── CONTRIBUTING.md
│   ├── CODE_OF_CONDUCT.md
│   └── architecture/
│
├── ci-cd/                  # 12 templates
│   ├── github-actions/
│   ├── gitlab-ci/
│   ├── jenkins/
│   └── docker/
│
├── setup/                  # 5 templates
│   ├── licenses/
│   ├── editorconfig/
│   └── structure/
│
└── quality/                # 5 templates
    ├── linting/
    ├── formatting/
    └── testing/
```

**Template Format:**
```markdown
---
id: readme-comprehensive
version: 1.0.0
category: documentation
description: Comprehensive README with all standard sections
language: markdown
dependencies: []
variables:
  - name: PROJECT_NAME
    description: Name of the project
    required: true
  - name: DESCRIPTION
    description: Brief project description
    required: true
  - name: AUTHOR
    description: Project author/organization
    required: false
    default: ""
---

# ${PROJECT_NAME}

${DESCRIPTION}

## Installation

\`\`\`bash
# Installation instructions
\`\`\`

## Usage

\`\`\`bash
# Usage examples
\`\`\`

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## License

${LICENSE_TYPE} - See [LICENSE](./LICENSE) for details.

## Author

${AUTHOR}
```

### Phase Distribution

**Phase 1 (15 MVP Templates) - Weeks 3-4:**

**Git (5):**
- .gitignore (Node, Python, Java)
- pre-commit hook (basic)
- GitHub Actions CI (test + build)

**Documentation (3):**
- README.md (comprehensive)
- README.md (minimal)
- CONTRIBUTING.md

**CI/CD (3):**
- GitHub Actions (test workflow)
- GitHub Actions (build workflow)
- Dockerfile (basic)

**Setup (2):**
- LICENSE (MIT)
- .editorconfig

**Quality (2):**
- ESLint config (JavaScript)
- Prettier config

**Phase 2 (Add 10, Total 25) - Weeks 5-8:**

**Git (3 more):**
- .gitignore (Go, Rust)
- pre-push hook

**Documentation (3 more):**
- CODE_OF_CONDUCT.md
- ARCHITECTURE.md
- API.md

**CI/CD (3 more):**
- Docker Compose
- GitHub Actions (release)
- GitLab CI (basic)

**Quality (1 more):**
- Pytest config

**Phase 3 (Add 15+, Total 40+) - Weeks 9-12:**

**CI/CD (6 more):**
- Jenkins pipeline
- Security scanning
- Deployment workflows

**Setup (3 more):**
- LICENSE (Apache, GPL)
- Project structure scaffolds

**Quality (6+ more):**
- Pylint config
- Black config
- Clippy config (Rust)
- Testing frameworks
- Security scanning configs

---

## Considered Alternatives

### Alternative 1: All 40+ Templates at Once

**Pros:**
- Feature-complete at launch
- Comprehensive coverage immediately
- Impressive marketing

**Cons:**
- Overwhelming for users (choice paralysis)
- Unvalidated templates (no feedback)
- Testing burden (40+ templates = 120+ tests)
- Higher risk of stale templates

**Why Not Chosen:**
Violates "inverted approach." Need to validate 15 MVP templates with real usage before expanding.

### Alternative 2: Dynamic Template Generation

**Pros:**
- Infinite customization
- AI-generated templates
- Adapts to any project

**Cons:**
- Unpredictable quality
- High token costs (generate per use)
- Hard to test (infinite variations)
- Security concerns (code generation)

**Why Not Chosen:**
Production quality requires hand-crafted, tested templates. Generation can be Phase 4+ enhancement.

### Alternative 3: External Template Repository

**Pros:**
- More templates available (GitHub, etc.)
- Community maintained externally
- Always up-to-date

**Cons:**
- Quality inconsistent
- No validation/testing
- External dependency
- License concerns

**Why Not Chosen:**
Plugin must work standalone. Can reference external templates later as enhancement.

---

## Consequences

### Positive

1. **Proven Value Early:** 15 MVP templates solve 80% of needs (Week 4)
2. **Community Validated:** Phase 2 expansion guided by real feedback
3. **Manageable Testing:** Phased expansion = manageable test burden
4. **Lower Risk:** Stale templates easier to identify and update in small batches
5. **Progressive Loading:** Analyzer recommends 2-5 templates, not 40+
6. **Extensibility:** Clear pattern for community contributions

### Negative

1. **Feature Perception:** "Only 15 templates at launch" may seem limited (mitigated: "MVP" messaging)
2. **Expansion Overhead:** Must revisit templates in Phases 2-3 (mitigated: scheduled in timeline)
3. **Variant Maintenance:** Language-specific variants increase maintenance (mitigated: automated testing)

### Risks

**Risk 1: Template Staleness**
- **Impact:** Outdated best practices harm credibility
- **Probability:** High (tech evolves quickly)
- **Mitigation:** Quarterly review process, community contributions, deprecation policy

**Risk 2: Variable Substitution Failures**
- **Impact:** Broken templates frustrate users
- **Probability:** Medium (human error)
- **Mitigation:** `validate-template.sh` hook, automated tests, clear error messages

---

## Implementation Notes

### Variable Substitution

**Implementation (scripts/lib/template-utils.js):**
```javascript
function substituteVariables(template, variables) {
  let result = template;

  for (const [key, value] of Object.entries(variables)) {
    const pattern = new RegExp(`\\$\\{${key}\\}`, 'g');
    result = result.replace(pattern, value);
  }

  // Check for unsubstituted variables
  const remaining = result.match(/\$\{[A-Z_][A-Z0-9_]*\}/g);
  if (remaining) {
    console.warn(`⚠️  Unsubstituted variables: ${remaining.join(', ')}`);
  }

  return result;
}
```

**Validation (scripts/validate-template.sh):**
```bash
# Check for unsubstituted variables after application
if grep -q '\${[A-Z_][A-Z0-9_]*}' "${FILE_PATH}"; then
  echo "⚠️  Warning: Unsubstituted template variables found"
  echo "   Variables: $(grep -o '\${[A-Z_][A-Z0-9_]*}' "${FILE_PATH}")"
fi
```

### Testing Strategy

**Per Template:**
- Variable substitution test
- Valid syntax test (linting)
- Applicability test (works in real project)

**Total Tests:**
- Phase 1: 15 templates × 3 tests = 45 tests
- Phase 2: 25 templates × 3 tests = 75 tests
- Phase 3: 40 templates × 3 tests = 120 tests

---

## References

1. [ADR-001: Plugin Architecture](./001-plugin-architecture.md)
2. [ADR-002: Analyzer Design](./002-analyzer-design.md)
3. [GitHub .gitignore Templates](https://github.com/github/gitignore)
4. [Contributor Covenant](https://www.contributor-covenant.org/)

---

## Validation

### Success Criteria

**Phase 1 (Week 4):**
- ✅ 15 MVP templates complete and tested
- ✅ 45 tests passing
- ✅ Variable substitution works correctly
- ✅ Documentation for each template

**Phase 2 (Week 8):**
- ✅ 25 total templates
- ✅ User feedback incorporated
- ✅ 75 tests passing

**Phase 3 (Week 12):**
- ✅ 40+ total templates
- ✅ 120+ tests passing
- ✅ < 5% error rate in application

### Metrics

- Template application success rate: > 95%
- User satisfaction with templates: > 80%
- Community contributions: 5+ (Month 3)
- Template freshness: < 6 months since last review

---

**Last Updated:** 2025-11-27
**Related ADRs:** [ADR-001](./001-plugin-architecture.md), [ADR-002](./002-analyzer-design.md), [ADR-004](./004-isolation-enforcement.md), [ADR-005](./005-token-optimization.md)
