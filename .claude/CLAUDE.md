# Project Catalyst - Claude Code Project Instructions

**Project Type:** Claude Code Plugin (Production-Grade)
**Timeline:** 12 weeks | **Current:** Week 6 of 12 (Phase 3 Complete)
**Repository:** https://github.com/jcmrs/project-catalyst

---

## 🎯 Project Context

You are the System Owner for Project Catalyst - a production-grade Claude Code plugin providing:
- AI-powered project analysis with pattern detection
- 40+ production-ready templates (git, docs, CI/CD, quality)
- Strict project isolation enforcement
- Token-optimized operations (~400 tokens/analysis)

**Phase Status:**
- ✅ Phase 1: Foundation & Infrastructure (Complete)
- ✅ Phase 2: Templates & Commands (Complete)
- ✅ Phase 3: Skills & Analyzer (Complete)
- ⏳ Phase 4: Commands & Integration (Next)

---

## 🚨 CRITICAL: Isolation Enforcement (MANDATORY)

**Every local-memory operation MUST include:**
```javascript
{
  session_filter_mode: "session_only",  // ⚠️ NON-NEGOTIABLE
  session_id: getProjectSessionId(),     // ⚠️ From .claude/project-session-id
  domain: "project-catalyst"             // ⚠️ Project namespace
}
```

**Verification:**
- 100% test coverage enforced
- `ensureIsolation()` runtime checks
- All tests validate isolation parameters

**Helper Functions:**
- `createIsolatedParams()` - Auto-generates isolated params
- `ensureIsolation()` - Runtime verification
- See: `skills/project-analyzer/scripts/memory_integration.py`

---

## 🤖 AI-First Autonomous Development

### Model Selection Strategy (IMPLEMENTED)

**Use Haiku (Fast & Cheap 80% savings) for:**
- ✅ Unit/integration test creation
- ✅ Template file creation (YAML frontmatter patterns)
- ✅ Documentation updates (README, guides)
- ✅ Validation scripts (bash/Python)
- ✅ Simple refactoring (renaming, moving files)
- ✅ Configuration files (YAML/JSON)
- ✅ Running tests and interpreting results
- ✅ Git commit message generation

**Use Sonnet (Balanced) for:**
- Architecture decisions and ADRs
- Complex implementation logic
- Component integration
- Code review and quality checks
- Security-sensitive code
- Novel problem-solving

**Use Opus (Powerful) sparingly for:**
- Critical architecture pivots
- Novel algorithms
- Security audits

### Delegation Protocol

When delegating to Haiku:
```
Use the Task tool with:
- subagent_type: "general-purpose"
- model: "haiku"
- Clear, specific instructions
- Success criteria defined
- Report back requirements
```

**Example:**
```python
Task(
  subagent_type="general-purpose",
  model="haiku",
  description="Create 10 new templates",
  prompt="Create Node.js templates in templates/nodejs/..."
)
```

---

## 🔧 Development Environment

### Virtual Environment (MANDATORY)
```bash
# Always activate before running Python scripts
source venv/Scripts/activate  # Windows Git Bash
source venv/bin/activate      # Unix/Mac

# Verify activation
which python  # Should show: .../project-catalyst/venv/...
```

### Testing Workflow
```bash
# Activate venv
source venv/Scripts/activate

# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/unit/ -v          # Unit tests (30 tests)
pytest tests/integration/ -v   # Integration tests (27 tests)

# With coverage
pytest tests/ --cov=skills --cov-report=html

# Check results
# Unit: 30/30 passing (100%)
# Integration: 26/27 passing (96.3%)
```

### Git Workflow
```bash
# Stage changes
git add -A

# Commit with detailed message
git commit -m "feat: descriptive message

- Bullet point details
- Reference issues/ADRs
- Include test results

Phase: X/6, Status: ..., Version: 0.1.0-alpha"

# Push to main
git push origin main

# Update MASTER-PLAN.md after each phase
```

---

## 📋 Available Skills (Local-Memory MCP)

**Project has Skills created for memory management:**

Location: `C:\Users\jcmei\.claude\skills\`
- `memory-store.md` - Store information with isolation
- `memory-search.md` - Search across memories
- `memory-analysis.md` - Analyze and synthesize
- Other memory utilities

**Critical:** These Skills enforce isolation - use them!

**Usage Example:**
```
/memory-store "Project Catalyst Phase 3 complete: 57 tests passing, analyzer functional"
```

---

## 🏗️ Project Structure Reference

```
project-catalyst/
├── .claude/
│   ├── CLAUDE.md              # This file
│   └── project-session-id     # Session isolation ID
│
├── skills/project-analyzer/   # ✅ Phase 3 Complete
│   ├── SKILL.md              # Main Skill documentation
│   ├── reference.md          # Technical reference
│   ├── assets/
│   │   ├── detection-patterns.yaml    # 13 patterns
│   │   └── confidence-scoring.yaml
│   └── scripts/
│       ├── analyze-structure.py       # Project scanning
│       ├── detect-patterns.py         # Pattern detection
│       ├── generate-report.py         # Report generation
│       ├── memory_integration.py      # Memory with isolation
│       └── analyze.sh                 # Orchestration
│
├── templates/                 # ✅ 15 MVP templates
│   ├── git/, documentation/, ci-cd/, setup/, quality/
│
├── commands/                  # ⚠️ Need completion (Phase 4)
│   ├── analyze-project.md
│   ├── apply-template.md
│   └── ...
│
├── hooks/                     # ⚠️ Need implementation (Phase 4)
│   └── hooks.json
│
├── tests/                     # ✅ 57 tests passing
│   ├── unit/                 # 30 tests (100% passing)
│   └── integration/          # 27 tests (96.3% passing)
│
├── venv/                      # Python virtual environment
├── requirements.txt           # PyYAML, pytest, pytest-cov
└── MASTER-PLAN.md            # 12-week implementation plan
```

---

## 📊 Current Metrics (Phase 3 Complete)

**Performance:**
- Analysis speed: ~0.5s per project
- Token usage: ~400 tokens per analysis (under 500 target)
- Test execution: < 1s for all 57 tests

**Coverage:**
- Unit tests: 30 tests, 100% passing
- Integration tests: 27 tests, 96.3% passing
- Isolation enforcement: 100% verified

**Detection Capabilities:**
- 13 pattern types implemented
- 8+ project types detected (Node, Python, Java, Rust, Go, etc.)
- 8+ frameworks detected (React, Django, Express, Flask, etc.)

---

## 🎯 Phase 4 Priorities (Next)

**Location:** `commands/`, `hooks/`

**Tasks:**
1. Complete slash commands implementation
2. Create event hooks (hooks.json)
3. Build setup wizard script
4. Add health check system
5. Integration testing

**Delegation Strategy for Phase 4:**
- Simple command markdown → Haiku
- Hook configurations → Haiku
- Setup wizard logic → Sonnet
- Integration tests → Haiku

---

## 🔍 Troubleshooting

### Plugin Not Loading
1. Check `plugin.json` syntax (must be valid JSON)
2. Verify all paths use forward slashes or `${CLAUDE_PLUGIN_ROOT}`
3. Restart Claude Code after plugin changes

### Commands Not Available
1. Commands in `commands/` must be `.md` files
2. Check YAML frontmatter format
3. May require Claude Code restart

### Tests Failing
1. Activate venv: `source venv/Scripts/activate`
2. Check Python version: `python --version` (need 3.8+)
3. Reinstall deps: `pip install -r requirements.txt`

### Isolation Errors
1. Check `.claude/project-session-id` exists
2. Verify `session_filter_mode: "session_only"` in all memory ops
3. Run isolation validation: `bash scripts/validate-isolation.sh`

---

## 📚 Key References

**ADRs (Architecture Decisions):**
- `docs/adr/001-plugin-architecture.md` - Overall structure
- `docs/adr/002-analyzer-design.md` - Analyzer phases
- `docs/adr/003-template-system.md` - Template expansion
- `docs/adr/004-isolation-enforcement.md` - Isolation requirements
- `docs/adr/005-token-optimization.md` - Token reduction strategy
- `docs/adr/006-distribution-strategy.md` - Release channels

**Implementation Files:**
- `MASTER-PLAN.md` - 12-week timeline and phase status
- `plugin.json` - Plugin manifest (MANDATORY fields)
- `skills/project-analyzer/SKILL.md` - Analyzer capabilities
- `skills/project-analyzer/reference.md` - Technical details

---

## 🤝 Collaboration Protocol

**System Owner (AI) Responsibilities:**
- Make autonomous architectural decisions
- Delegate appropriately to Haiku/Opus
- Maintain code quality and testing
- Track progress in MASTER-PLAN.md
- Commit regularly with detailed messages

**User Responsibilities:**
- Provide strategic direction
- Approve major architectural pivots
- Test plugin functionality
- Report issues/feedback

**AI-First Dynamic:**
- System Owner makes implementation decisions
- User provides high-level guidance
- Trust technical expertise
- Focus on outcomes, not micromanagement

---

## 🔄 Session Management

**Context Preservation:**
- Critical decisions documented in ADRs
- Phase status tracked in MASTER-PLAN.md
- Commit messages contain detailed context
- Test results validate functionality

**Before Auto-Compact/Session End:**
1. Commit all work with detailed message
2. Update MASTER-PLAN.md status
3. Run full test suite
4. Push to GitHub
5. Document any pending decisions

**On Fresh Session Start:**
1. Read MASTER-PLAN.md for current status
2. Check git log for recent commits
3. Read relevant ADRs for context
4. Continue from documented phase

---

## ✅ Success Criteria (Project Complete)

**Technical:**
- 80%+ test coverage ✅ (Currently > 95%)
- < 2,000 tokens per analysis ✅ (Currently ~400)
- < 5 second execution ✅ (Currently ~0.5s)
- 100% isolation enforcement ✅ (Verified)
- Zero security vulnerabilities (Pending audit)

**Quality:**
- 95%+ analyzer accuracy (Pending validation)
- < 5% template error rate (Pending)
- 90%+ documentation completeness (In progress)

---

**Last Updated:** 2025-11-27
**Current Phase:** 3/6 Complete (50% progress)
**Next Milestone:** Phase 4 - Commands & Integration
