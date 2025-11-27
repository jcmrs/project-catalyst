# Project Catalyst - Production-Grade Plugin Architecture Plan

**Status:** Approved for Implementation
**Timeline:** 12 weeks
**Target:** Production-ready Claude Code plugin package
**Working Directory:** `C:\localmemory\project-catalyst\`

---

## ⚠️ CRITICAL: Project Directory Structure

**All project files MUST be within:** `C:\localmemory\project-catalyst\`

**DO NOT create files in:**
- ❌ `C:\Users\jcmei\.claude\` (global Claude installation)
- ❌ Any location outside `C:\localmemory\`

**Why:** This ensures the package is self-contained, portable, and doesn't contaminate the global Claude Code installation.

---

## Executive Summary

Project Catalyst is a comprehensive Claude Code plugin that provides language-agnostic project utilities through a hybrid approach: pre-built templates + AI-powered analysis. The package enforces project isolation, optimizes token usage, and follows production-grade development practices.

**Key Features:**
- 40+ production-ready templates (git, docs, CI/CD, quality)
- AI-powered project analyzer with contextual recommendations
- Strict project isolation (prevents context contamination)
- Token-optimized (contextual retrieval, progressive loading)
- Multi-channel distribution (GitHub + marketplace + setup script)

---

## Package Structure

```
project-catalyst/                     # ROOT: C:\localmemory\project-catalyst\
├── MASTER-PLAN.md                   # This file
├── README.md                        # Project overview
├── plugin.json                      # Plugin metadata
├── CONTRIBUTING.md                  # Contribution guidelines
├── LICENSE                          # MIT License
│
├── skills/                          # AI Skills (core intelligence)
│   ├── project-analyzer/            # Main analyzer Skill
│   │   ├── SKILL.md                # Skill instructions
│   │   ├── assets/
│   │   │   ├── detection-patterns.yaml
│   │   │   ├── recommendation-rules.yaml
│   │   │   └── confidence-scoring.yaml
│   │   ├── references/
│   │   │   ├── analysis-guide.md
│   │   │   └── pattern-library.md
│   │   └── scripts/
│   │       ├── analyze-structure.py
│   │       ├── detect-patterns.py
│   │       └── generate-recommendations.py
│   │
│   └── utility-generator/           # Template generation Skill
│       ├── SKILL.md
│       └── scripts/
│           ├── apply-template.sh
│           └── customize-template.py
│
├── templates/                       # Pre-built utilities (40+ templates)
│   ├── git/                        # Git workflows
│   ├── documentation/              # Documentation templates
│   ├── ci-cd/                      # CI/CD configurations
│   ├── setup/                      # Project setup
│   └── quality/                    # Code quality
│
├── commands/                        # Slash commands
│   ├── analyze-project.md          # Run analyzer
│   ├── apply-template.md           # Apply template
│   ├── optimize-setup.md           # Optimize configuration
│   ├── health-check.md             # Validate installation
│   └── onboard.md                  # Interactive onboarding
│
├── hooks/                           # Event hooks
│   ├── project-start.yaml          # Auto-analyze new projects
│   ├── template-apply.yaml         # Post-template validation
│   └── analyzer-complete.yaml      # Post-analysis actions
│
├── scripts/                         # Installation & maintenance
│   ├── install.sh                  # One-command installer
│   ├── setup-wizard.sh             # Interactive configuration
│   ├── validate-isolation.sh       # Verify isolation enforcement
│   └── health-check.sh             # System health validation
│
├── tests/                           # Comprehensive test suite
│   ├── unit/                       # 75 unit tests
│   ├── integration/                # 20 integration tests
│   └── e2e/                        # 5 end-to-end tests
│
└── docs/                            # Development documentation
    ├── adr/                        # Architecture Decision Records
    ├── sdd/                        # Software Design Documents
    │   ├── plans/                  # High-level phase plans
    │   └── specs/                  # Detailed specifications
    ├── guides/                     # User guides
    └── api/                        # API documentation
```

---

## Implementation Timeline

### Phase 1: Foundation & Infrastructure (Weeks 1-2)
**Location:** `docs/adr/`, root files

**Tasks:**
- Set up repository structure (IN PROJECT DIRECTORY)
- Write 6 ADRs (Architecture Decision Records)
- Create plugin.json and metadata
- Implement isolation enforcement verification
- Set up CI/CD pipeline configuration
- Write contribution guidelines

**Deliverables:**
- Complete repository structure in `C:\localmemory\project-catalyst\`
- 6 ADRs documented in `docs/adr/`
- Isolation verification script working
- CI/CD pipeline configuration ready

### Phase 2: Template Library (Weeks 3-4)
**Location:** `templates/`

**MVP (15 templates):**
- Git: .gitignore (5 variants), pre-commit hook
- Documentation: README.md (comprehensive, minimal), CONTRIBUTING.md
- CI/CD: GitHub Actions (test, build), Docker basics
- Setup: LICENSE (MIT, Apache), .editorconfig
- Quality: ESLint config, Prettier config

**Deliverables:**
- 15 MVP templates in `templates/`
- Template validator script
- Application system working
- Template documentation

### Phase 3: Analyzer Skill (Weeks 5-6)
**Location:** `skills/project-analyzer/`

**Tasks:**
- Design rule-based detection patterns (YAML)
- Implement recommendation rules
- Build confidence scoring system
- Integrate with local-memory (isolation enforced)
- Add progressive loading

**Deliverables:**
- Analyzer Skill functional
- Pattern detection accurate (95%+ target)
- local-memory integration complete
- Token optimization verified (~500 tokens)

### Phase 4: Commands & Integration (Weeks 7-8)
**Location:** `commands/`, `hooks/`

**Tasks:**
- Implement 5 slash commands
- Create 3 event hooks
- Build setup wizard script
- Add health check system
- Implement validation scripts

**Deliverables:**
- All commands working
- Hooks integrated
- Setup wizard functional
- Validation complete

### Phase 5: Testing & Quality (Weeks 9-10)
**Location:** `tests/`

**Tasks:**
- Write 75 unit tests (80%+ coverage)
- Write 20 integration tests
- Write 5 E2E tests
- Implement 100% isolation test coverage
- Performance benchmarking
- Security audit

**Deliverables:**
- 100 comprehensive tests
- 80%+ overall coverage
- Performance targets met
- Security validated

### Phase 6: Documentation & Launch (Weeks 11-12)
**Location:** `docs/`

**Tasks:**
- Write user guides (installation, getting-started, customization, troubleshooting)
- Create API documentation
- Finalize README
- Create marketplace listing
- Configure distribution channels
- Launch preparation

**Deliverables:**
- Complete documentation suite
- Professional README
- Multi-channel distribution ready

---

## Trade-off Decisions (Finalized)

### 1. Template Scope - Phased Approach
- Start with 15 MVP templates (Weeks 3-4)
- Expand to 25 (Weeks 5-8)
- Complete 40+ (Weeks 9-12)
- **Rationale:** Proves value quickly, validates with community, reduces risk

### 2. Analyzer Intelligence - Progressive Enhancement
- Rule-based pattern detection first (~500 tokens)
- Add local-memory integration (~1,500 tokens)
- Implement AI contextual retrieval (~200 tokens cached)
- **Rationale:** Easier to test, lower token costs initially, scales with proof

### 3. Distribution Strategy - All Channels
- GitHub → Marketplace → Setup Script (Week 12)
- **Rationale:** Maximizes reach, serves all user types

### 4. Timeline - Full 12 Weeks (Production-Grade)
- 100 comprehensive tests
- Complete documentation
- Security validated
- **Rationale:** Quality over speed, "one mistake can have ripple effects"

---

## Token Optimization Strategy

**Target: 87% reduction vs naive approach**

- Phase 1 (Rule-based): ~500 tokens per analysis
- Phase 2 (Integrated): ~1,500 tokens per analysis
- Phase 3 (Optimized): ~200 tokens per cached operation

**Techniques:**
- Progressive disclosure loading
- Contextual retrieval (hybrid BM25 + semantic)
- 1-hour prompt caching
- Response format optimization

---

## Isolation Enforcement (MANDATORY)

**Every local-memory operation MUST include:**
```javascript
{
  session_filter_mode: "session_only",  // ⚠️ MANDATORY
  session_id: getProjectSessionId(),     // ⚠️ From .claude/project-session-id
  domain: "project-catalyst"             // ⚠️ Project identifier
}
```

**Verification:**
- 100% test coverage for isolation logic
- Runtime verification script (`scripts/validate-isolation.sh`)
- CI/CD validation gate

---

## Success Metrics

**Technical:**
- 80%+ test coverage
- < 2,000 tokens per analysis
- < 5 second analyzer execution
- 100% isolation enforcement
- Zero security vulnerabilities

**Quality:**
- 95%+ analyzer accuracy
- < 5% template error rate
- 90%+ documentation completeness

---

## Critical References

**Pattern Examples (Within Global Installation - READ ONLY):**
1. Multi-Agent Command: `C:\Users\jcmei\.claude\plugins\marketplaces\claude-code-workflows\plugins\git-pr-workflows\commands\git-workflow.md`
2. Multi-File Skill: `C:\Users\jcmei\.claude\plugins\marketplaces\claude-code-workflows\plugins\shell-scripting\skills\bash-defensive-patterns\SKILL.md`
3. Token Optimization: `C:\Users\jcmei\.claude\skills\context-optimizer.md`
4. Isolation Patterns: `C:\localmemory\PROJECT-ISOLATION-SETUP.md`

**⚠️ Note:** These are READ-ONLY references. Never modify files outside `C:\localmemory\project-catalyst\`.

---

## ⚠️ CRITICAL TECHNICAL SPECIFICATIONS (Anthropic AI Validated)

### 1. Plugin Manifest (plugin.json) - MANDATORY FIELDS

```json
{
  "name": "project-catalyst",
  "version": "1.0.0",
  "description": "Language-agnostic project utilities with AI-powered analysis",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/your-org/project-catalyst",
  "license": "MIT",
  "keywords": ["utilities", "templates", "analyzer", "project-setup"],
  "commands": ["./commands/"],
  "agents": "./agents/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Source:** [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference#plugin-components-reference)

### 2. Skills Naming Convention - MANDATORY

**CRITICAL:** Skills MUST use `SKILL.md` filename (case-sensitive, not `skill.md` or `analyzer.md`)

```
skills/
├── project-analyzer/
│   ├── SKILL.md              # ⚠️ MANDATORY filename
│   ├── reference.md          # Optional detailed docs
│   └── scripts/
└── utility-generator/
    ├── SKILL.md              # ⚠️ MANDATORY filename
    └── scripts/
```

**Source:** [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins#next-steps)

### 3. Hooks Format - MUST USE hooks.json (NOT YAML)

**CRITICAL CHANGE:** Hooks must be in `hooks/hooks.json` format, not YAML files.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "**",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/check-analyzed.sh"
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
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-template.sh"
          }
        ]
      }
    ]
  }
}
```

**Source:** [Claude Code Hooks Documentation](https://code.claude.com/docs/en/hooks)

### 4. Path Variable - MANDATORY for All Scripts

**ALL script paths MUST use `${CLAUDE_PLUGIN_ROOT}` variable:**

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/analyze.py"
}
```

**Source:** [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)

### 5. Session ID Implementation - MANDATORY

```javascript
function getProjectSessionId() {
  const sessionIdPath = path.join(
    process.env.CLAUDE_PROJECT_DIR || process.cwd(),
    '.claude',
    'project-session-id'
  )
  return fs.readFileSync(sessionIdPath, 'utf-8').trim()
}
```

**Must read from:** `.claude/project-session-id` file in project root

**Source:** [Claude Code Plugin Development](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/README.md)

### 6. MCP Graceful Degradation - REQUIRED

```javascript
try {
  await mcp__local-memory__store_memory({
    content: data,
    session_filter_mode: "session_only",
    session_id: getProjectSessionId(),
    domain: "project-catalyst"
  })
} catch (error) {
  if (error.code === 'MCP_SERVER_UNAVAILABLE') {
    // Fallback to local file storage
    await fs.writeFile('.catalyst/cache.json', JSON.stringify(data))
    console.warn('⚠️ MCP unavailable, using local fallback')
  }
  throw error
}
```

**Source:** [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference#plugin-components-reference)

### 7. Plugin Validator - ADD TO CI/CD

```bash
# Add to CI/CD pipeline (Week 1-2)
./scripts/validate-plugin.sh

# Or use plugin-dev toolkit
npx @anthropic-ai/plugin-validator ./
```

**Source:** [Plugin Development Toolkit](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/README.md)

### 8. Token Optimization Validation

**Targets validated against Anthropic research:**

**Contextual Retrieval Performance:**
- Without optimization: ~5,000 tokens typical
- With contextual embeddings: 35% reduction → ~3,250 tokens
- With contextual embeddings + BM25: 49% reduction → ~2,550 tokens
- With prompt caching (1-hour): 87% additional reduction → ~332 tokens

**Our Targets (ACHIEVABLE):**
- First run: 1,500 tokens ✅ (focused queries)
- Cached: 200 tokens ✅ (1-hour cache duration)

**Source:** [Anthropic Contextual Retrieval Research](https://www.anthropic.com/news/contextual-retrieval)

---

## Updated Package Structure (Technical Compliance)

```
project-catalyst/
├── plugin.json                      # With MANDATORY fields
├── README.md
├── CONTRIBUTING.md
├── LICENSE (MIT)
│
├── skills/
│   ├── project-analyzer/
│   │   ├── SKILL.md                # ⚠️ MUST be SKILL.md (not skill.md)
│   │   ├── reference.md            # Optional detailed docs
│   │   ├── assets/
│   │   │   ├── detection-patterns.yaml
│   │   │   ├── recommendation-rules.yaml
│   │   │   └── confidence-scoring.yaml
│   │   └── scripts/
│   │       ├── analyze-structure.py
│   │       ├── detect-patterns.py
│   │       └── generate-recommendations.py
│   │
│   └── utility-generator/
│       ├── SKILL.md                # ⚠️ MUST be SKILL.md
│       └── scripts/
│           ├── apply-template.sh
│           └── customize-template.py
│
├── templates/                       # (40+ templates, phased)
├── commands/                        # Slash commands
│
├── hooks/
│   └── hooks.json                  # ⚠️ MUST be hooks.json (not YAML)
│
├── scripts/
│   ├── install.sh
│   ├── setup-wizard.sh
│   ├── validate-isolation.sh
│   ├── validate-plugin.sh          # ⚠️ ADD: Plugin validator
│   └── health-check.sh
│
├── tests/                           # (100 tests)
└── docs/                            # (ADRs, SDDs, guides, API)
```

---

## Revised Phase 1 Deliverables (Weeks 1-2)

**Week 1:**
1. ✅ Project structure established
2. ✅ MASTER-PLAN.md with technical corrections
3. ✅ README.md created
4. ⏳ Create `plugin.json` with MANDATORY fields
5. ⏳ Create `hooks/hooks.json` (NOT YAML)
6. ⏳ Implement `getProjectSessionId()` function
7. ⏳ Add `${CLAUDE_PLUGIN_ROOT}` to all script paths
8. ⏳ Write ADR 001: Plugin Architecture (include technical specs)

**Week 2:**
9. ⏳ Write ADR 002-006
10. ⏳ Implement isolation verification with 100% coverage
11. ⏳ Add plugin validator to CI/CD
12. ⏳ Implement MCP graceful degradation
13. ⏳ Write CONTRIBUTING.md
14. ⏳ Create LICENSE (MIT)

---

## Next Steps

**Immediate (Week 1):**
1. ✅ Restructure to project directory
2. ✅ Create README.md
3. ✅ Integrate Anthropic AI technical corrections
4. ⏳ Create `plugin.json` with validated structure
5. ⏳ Create `hooks/hooks.json` (correct format)
6. ⏳ Implement `getProjectSessionId()` function
7. ⏳ Write ADR 001: Plugin Architecture

---

**Status:** Implementation in progress - Phase 1 (Week 1)
**Version:** 1.3
**Last Updated:** 2025-11-27 (Integrated Anthropic AI technical corrections)
**Working Directory:** `C:\localmemory\project-catalyst\`
**Validated By:** Anthropic Documentation AI
