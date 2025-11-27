# Project Analyzer

AI-powered project analysis and pattern detection for identifying missing utilities, configuration gaps, and best practice violations.

## Overview

The Project Analyzer Skill examines project structure and detects:
- Missing configuration files (gitignore, CI/CD, documentation)
- Best practice violations
- Outdated patterns
- Template recommendations

## Capabilities

### Pattern Detection

Detects common project patterns:
- **Git Configuration:** .gitignore, hooks, workflows
- **Documentation:** README, CONTRIBUTING, LICENSE
- **CI/CD:** GitHub Actions, Docker, build scripts
- **Code Quality:** Linters, formatters, test setup
- **Setup Files:** .editorconfig, package managers

### Confidence Scoring

Each detection includes confidence level:
- **High (90-100%):** File existence checks
- **Medium (70-89%):** Quality thresholds
- **Low (40-69%):** Pattern matching

### Template Recommendations

Suggests templates from Project Catalyst library based on:
- Missing files detected
- Project language/framework
- Severity of gaps
- User preferences

## Usage

### Automatic Invocation

The analyzer runs automatically when:
- User invokes `/analyze-project` command
- New project detected (via SessionStart hook)
- User requests recommendations

### Manual Invocation

Ask Claude to analyze your project:

```
Analyze this project and recommend templates
```

or

```
What utilities am I missing in this project?
```

## Detection Patterns

The analyzer uses rule-based detection patterns defined in `assets/detection-patterns.yaml`:

```yaml
patterns:
  - id: missing-gitignore
    type: file_absence
    check: .gitignore
    confidence: high
    severity: medium
    recommendation:
      template: git/gitignore
      reason: "Prevents accidental commits of sensitive files"
```

## Analysis Process

1. **Scan Project Structure**
   - List files and directories
   - Identify project type (Node, Python, Java, etc.)
   - Detect frameworks and tools

2. **Apply Detection Patterns**
   - Check for missing files
   - Validate file quality
   - Assess configuration completeness

3. **Score Confidence**
   - High: Direct evidence (file exists/missing)
   - Medium: Quality metrics (file size, sections)
   - Low: Pattern matching (fuzzy detection)

4. **Generate Recommendations**
   - Prioritize by severity (high → medium → low)
   - Suggest relevant templates
   - Provide application commands

5. **Store Results (with Isolation)**
   - Save analysis to local-memory
   - Enforce session_filter_mode: "session_only"
   - Enable historical comparison

## Output Format

### Analysis Report

```
🔍 Project Analysis Results

Project Type: Node.js (TypeScript)
Files Scanned: 127
Patterns Detected: 8

Git Configuration: ⚠️
  ❌ Missing .gitignore (confidence: high, severity: medium)
     → /apply-template git/gitignore/node

  ✅ Git hooks configured

Documentation: ⚠️
  ⚠️  README.md exists but minimal (confidence: medium, severity: low)
     → /apply-template documentation/README-comprehensive

  ❌ Missing CONTRIBUTING.md (confidence: high, severity: low)
     → /apply-template documentation/CONTRIBUTING

CI/CD: ❌
  ❌ No CI/CD configuration (confidence: high, severity: high)
     → /apply-template ci-cd/github-actions/ci-test

Code Quality: ✅
  ✅ ESLint configured
  ✅ Prettier configured

Priority Actions:
  1. Setup CI/CD (high severity)
  2. Add .gitignore (medium severity)
  3. Add CONTRIBUTING.md (low severity)

Project Health: 68/100 (Fair)
```

## Token Optimization

Phase 1 implementation uses ~500 tokens per analysis:
- Detection patterns: ~300 tokens
- Project scan: ~100 tokens
- Recommendations: ~100 tokens

Future optimizations (Phase 2-3):
- local-memory integration: ~1,500 tokens (with history)
- AI-powered contextual retrieval: ~200 tokens (cached)

## Integration with Local-Memory

All analysis results are stored with **mandatory isolation**:

```javascript
const params = createIsolatedParams({
  content: JSON.stringify({
    timestamp: Date.now(),
    patterns_detected: analysisResults.patterns,
    recommendations: analysisResults.recommendations,
    confidence_scores: analysisResults.scores,
    project_type: projectInfo.type
  }),
  tags: ['project-analysis', 'catalyst', 'pattern-detection'],
  importance: 8,
  source: 'project-catalyst-analyzer'
});

await mcp__local_memory__store_memory(params);
```

## Historical Analysis

Compare current analysis with previous runs:

```
📊 Analysis History

Last Analysis: 3 days ago
Changes:
  ✅ Added .gitignore
  ✅ Setup CI/CD
  ⚠️  README still minimal

Health Trend: 45 → 68 (+23 points)
```

## Configuration

### Custom Patterns

Add custom detection patterns in `assets/detection-patterns.yaml`:

```yaml
patterns:
  - id: custom-pattern
    type: file_absence
    check: custom-config.json
    confidence: high
    severity: medium
    recommendation:
      template: custom/config
      reason: "Your custom reason"
```

### Severity Levels

- **High:** Critical gaps (CI/CD, LICENSE, .gitignore)
- **Medium:** Important but not blocking (documentation)
- **Low:** Nice-to-have (editorconfig, additional docs)

## Related Commands

- `/analyze-project` - Run full analysis
- `/apply-template` - Apply recommended templates
- `/health-check` - Quick health score
- `/optimize-setup` - Improve existing files

## Technical Details

**Implementation:** Rule-based pattern detection (Phase 1)
**Language:** Python + Bash
**Dependencies:** None (standalone)
**Token Usage:** ~500 tokens per analysis
**Isolation:** 100% enforced (session_only)

See `reference.md` for detailed implementation documentation.
