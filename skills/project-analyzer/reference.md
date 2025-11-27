# Project Analyzer - Technical Reference

Complete implementation reference for the Project Analyzer Skill.

## Architecture

The analyzer uses a modular pipeline architecture:

```
┌──────────────────┐
│  analyze.sh      │ ← Main orchestration script
└────────┬─────────┘
         │
         ├─► analyze-structure.py  (Step 1: Project scanning)
         │        │
         │        ▼
         │   structure.json (intermediate)
         │        │
         ├─► detect-patterns.py   (Step 2: Pattern detection)
         │        │
         │        ▼
         │   detection.json (intermediate)
         │        │
         └─► generate-report.py   (Step 3: Report generation)
                  │
                  ▼
             Human-readable report
```

## Components

### 1. analyze-structure.py

**Purpose:** Scan project directory and detect project type/frameworks.

**Input:** Project path (directory)

**Output:** JSON structure with:
- File list
- Directory list
- Project type detection (Node, Python, Java, etc.)
- Framework detection (React, Django, Express, etc.)
- Setup flags (Git, CI/CD, tests)

**Key Classes:**
- `ProjectAnalyzer`: Main analyzer class

**Detection Patterns:**
```python
PROJECT_INDICATORS = {
    'node': ['package.json', 'package-lock.json', 'node_modules/'],
    'python': ['requirements.txt', 'setup.py', 'pyproject.toml'],
    'java': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
    # ...
}

FRAMEWORK_INDICATORS = {
    'react': ['react', '@types/react'],
    'vue': ['vue', '@vue/'],
    'django': ['django', 'Django'],
    # ...
}
```

**Usage:**
```bash
python analyze-structure.py /path/to/project > structure.json
```

### 2. detect-patterns.py

**Purpose:** Apply detection patterns from YAML to project structure.

**Input:**
- Project structure JSON (from analyze-structure.py)
- Detection patterns YAML (assets/detection-patterns.yaml)

**Output:** JSON detection results with:
- Individual detections (issue_found flag)
- Recommendations (template + reason)
- Summary statistics (total patterns, issues by severity)

**Key Classes:**
- `PatternDetector`: Applies detection rules

**Pattern Types:**
- `file_absence`: Check if file is missing
- `directory_absence`: Check if directory is missing
- `file_quality`: Check if file meets quality criteria

**Confidence Scoring:**
```python
confidence_map = {
    'high': 1.0,    # File existence checks
    'medium': 0.7,  # Quality thresholds
    'low': 0.4      # Pattern matching
}
```

**Priority Calculation:**
```python
priority_score = confidence × severity_multiplier × priority_score

Where:
  confidence ∈ {1.0, 0.7, 0.4}
  severity_multiplier ∈ {1.0, 0.6, 0.3}
  priority_score ∈ {10, 5, 2}
```

**Usage:**
```bash
python detect-patterns.py structure.json assets/detection-patterns.yaml > detection.json
```

### 3. generate-report.py

**Purpose:** Generate human-readable analysis report with recommendations.

**Input:** Detection results JSON (from detect-patterns.py)

**Output:** Formatted text report with:
- Project information (type, frameworks, statistics)
- Category status (Git, Documentation, CI/CD, Quality, Setup)
- Issue details with recommendations
- Priority actions (top 5)
- Health score (0-100)

**Key Classes:**
- `ReportGenerator`: Formats detection results

**Health Score Calculation:**
```python
issues_penalty = (issues_found / total_patterns) × 100
high_penalty = high_severity_count × 20
medium_penalty = medium_severity_count × 10

health_score = max(0, 100 - issues_penalty - high_penalty - medium_penalty)

Ratings:
  90-100: Excellent 🚀
  75-89:  Good ✅
  50-74:  Fair ⚠️
  0-49:   Needs Improvement ❌
```

**Usage:**
```bash
python generate-report.py detection.json
```

### 4. memory_integration.py

**Purpose:** Integrate with local-memory MCP server with mandatory isolation.

**Key Classes:**
- `MemoryIntegration`: Handles storage/retrieval with isolation

**Isolation Enforcement:**
```python
def create_isolated_params(content, tags, importance):
    params = {
        'content': json.dumps(content),
        'tags': tags,
        'importance': importance,
        'source': 'project-catalyst-analyzer',
        'domain': 'project-catalyst',
        'session_filter_mode': 'session_only',  # MANDATORY
        'session_id': session_id,  # Required
    }
    return params
```

**Session ID Resolution:**
1. Check function parameter
2. Read from `.claude/project-session-id` file
3. Search parent directories (up to 5 levels)
4. Raise error if not found

**Storage Format:**
```json
{
  "timestamp": "2025-11-27T02:00:12",
  "project_name": "project-catalyst",
  "patterns_detected": 13,
  "issues_found": 4,
  "recommendations": [...],
  "confidence_scores": {...},
  "project_type": ["node"],
  "frameworks": ["react"],
  "health_score": 68
}
```

**Usage:**
```python
from memory_integration import MemoryIntegration

# Create integration
integration = MemoryIntegration(session_id='...')

# Store analysis
params = integration.store_analysis(results, 'my-project')
# → Use with mcp__local_memory__store_memory(params)

# Retrieve history
params = integration.retrieve_analysis_history('my-project')
# → Use with mcp__local_memory__search(params)
```

### 5. analyze.sh

**Purpose:** Main orchestration script (Bash).

**Workflow:**
1. Create temporary directory for intermediate files
2. Run analyze-structure.py → structure.json
3. Run detect-patterns.py → detection.json
4. Run generate-report.py → stdout
5. Clean up temporary files

**Usage:**
```bash
./analyze.sh /path/to/project
```

## Configuration Files

### detection-patterns.yaml

Defines detection patterns with metadata.

**Structure:**
```yaml
patterns:
  - id: pattern-id                    # Unique identifier
    type: file_absence                # Detection type
    check: .gitignore                 # File/directory to check
    confidence: high                  # Confidence level
    severity: medium                  # Severity level
    recommendation:
      template: git/gitignore         # Template to recommend
      reason: "Why this is important" # Human explanation
      variants:                       # Optional language variants
        - condition: "package.json exists"
          template: git/gitignore/node
    applies_when: "package.json exists" # Optional conditional
```

**Pattern Types:**

1. **file_absence**: Check if file is missing
   ```yaml
   type: file_absence
   check: README.md
   ```

2. **directory_absence**: Check if directory is missing
   ```yaml
   type: directory_absence
   check: .github/workflows
   ```

3. **file_quality**: Check if file meets quality criteria
   ```yaml
   type: file_quality
   check: README.md
   criteria:
     min_lines: 50
     required_sections:
       - Installation
       - Usage
   ```

**Current Patterns (Phase 1):**
- Git Configuration (3): gitignore, CI workflows, hooks
- Documentation (4): README, README quality, CONTRIBUTING, LICENSE
- CI/CD (3): build workflow, release workflow, Dockerfile
- Code Quality (2): ESLint, Prettier
- Setup (1): .editorconfig

### confidence-scoring.yaml

Defines confidence scoring rules and thresholds.

**Structure:**
```yaml
scoring_rules:
  high_confidence:
    weight: 1.0
    threshold: 0.9
    conditions:
      - type: file_exists
      - type: directory_exists
      - type: exact_match

quality_thresholds:
  readme:
    min_lines: 50
    required_sections: [...]
    confidence_boost: 0.2

severity_priority:
  high:
    priority_score: 10
    multiplier: 1.0
  medium:
    priority_score: 5
    multiplier: 0.6
  low:
    priority_score: 2
    multiplier: 0.3
```

## Token Usage

### Phase 1 (Rule-Based) - Current Implementation

**Per-analysis token usage:**
- Detection patterns YAML: ~300 tokens (cached after first load)
- Project structure scan: ~100 tokens
- Pattern detection: ~50 tokens
- Report generation: ~50 tokens
- **Total: ~500 tokens** (300 tokens after cache)

**Optimization:**
- YAML configs cached after first load
- Minimal JSON intermediate files
- Concise text output

### Phase 2 (Planned) - local-memory Integration

**Additional token usage:**
- Store analysis: ~200 tokens
- Retrieve history: ~100 tokens (concise format)
- Compare analyses: ~50 tokens
- **Total addition: ~350 tokens**

**With history (10 previous analyses):**
- Historical data: ~1,500 tokens (concise format)
- **Total with history: ~1,850 tokens**

### Phase 3 (Planned) - AI Contextual Retrieval

**Token reduction strategy:**
- Hybrid BM25 + semantic search: 49% accuracy improvement
- 1-hour prompt caching: 90% cost reduction on cache hits
- Progressive loading: Load only relevant patterns
- **Target: ~200 tokens** (with caching)

**Overall target (Phases 1-3):**
- Baseline (naive): ~2,500 tokens
- Optimized (Phase 3): ~320 tokens
- **Reduction: 87%**

## Testing

### Manual Testing

Test individual components:

```bash
# Test structure analyzer
python analyze-structure.py /path/to/project

# Test pattern detector
python detect-patterns.py structure.json detection-patterns.yaml

# Test report generator
python generate-report.py detection.json

# Test memory integration
python memory_integration.py store detection.json project-name

# Test full pipeline
./analyze.sh /path/to/project
```

### Integration Testing

Test with real projects:

```bash
# Test with Node.js project
./analyze.sh /path/to/node-project

# Test with Python project
./analyze.sh /path/to/python-project

# Test with Java project
./analyze.sh /path/to/java-project

# Test with project-catalyst itself
./analyze.sh /path/to/project-catalyst
```

### Expected Results

For project-catalyst:
- ✅ README.md exists
- ✅ LICENSE exists
- ✅ CONTRIBUTING.md exists
- ✅ .gitignore exists (repository has .git)
- ⚠️ Git hooks missing
- ❌ CI/CD workflows missing
- ⚠️ Build workflow missing
- ℹ️ Release workflow missing

Health Score: ~40-70 (Fair - missing CI/CD)

## Error Handling

### Common Errors

1. **FileNotFoundError**
   - Cause: Project path doesn't exist
   - Solution: Verify path is correct

2. **NotADirectoryError**
   - Cause: Project path is file, not directory
   - Solution: Pass directory path

3. **JSONDecodeError**
   - Cause: Invalid JSON in intermediate files
   - Solution: Check previous step output

4. **UnicodeEncodeError**
   - Cause: Windows console encoding (emojis)
   - Solution: Script automatically fixes with UTF-8 wrapper

5. **ValueError: No session ID**
   - Cause: `.claude/project-session-id` file not found
   - Solution: Create file or pass session_id parameter

### Debugging

Enable verbose output:

```bash
# Run with Python's verbose mode
python -v analyze-structure.py /path/to/project

# Add debug prints
python -c "
import sys
sys.path.insert(0, '.')
from analyze_structure import ProjectAnalyzer

analyzer = ProjectAnalyzer('/path/to/project')
structure = analyzer.scan_structure()

print('Files:', len(structure['files']))
print('Directories:', len(structure['directories']))
print('Project Types:', structure['project_types'])
"
```

## Future Enhancements

### Phase 2 (Weeks 7-8)

**local-memory Integration:**
- Store analysis results with timestamps
- Retrieve historical analyses
- Compare current vs previous
- Track improvements over time

**Example:**
```
📊 Analysis History

Last Analysis: 3 days ago
Changes:
  ✅ Added .gitignore
  ✅ Setup CI/CD
  ⚠️  README still minimal

Health Trend: 45 → 68 (+23 points)
```

### Phase 3 (Weeks 9-10)

**AI-Powered Contextual Retrieval:**
- Semantic search for patterns
- Context-aware recommendations
- Project-specific templates
- Learning from user preferences

**Example:**
```
🔍 Contextual Analysis

Based on your previous projects:
  → You prefer Jest over Mocha (3/3 projects)
  → Recommendation: ci-cd/github-actions/ci-test-jest

Project similarity: 87% match with "project-alpha"
  → Consider reusing: .prettierrc, tsconfig.json
```

## Troubleshooting

### No detections found

**Symptoms:** All patterns return `issue_found: false`

**Causes:**
1. Project already well-configured
2. Detection patterns not matching file structure
3. File paths using wrong separator (Windows vs Unix)

**Solution:**
- Verify files exist: `ls -la /path/to/project`
- Check pattern configuration
- Review path normalization in code

### Incorrect project type detection

**Symptoms:** Project type shows `unknown` or wrong type

**Causes:**
1. Missing indicator files (package.json, requirements.txt, etc.)
2. Indicator files in subdirectories (not project root)
3. Pattern not defined in PROJECT_INDICATORS

**Solution:**
- Add indicator files to project root
- Update PROJECT_INDICATORS dict
- Add custom detection logic

### Memory integration fails

**Symptoms:** `ValueError: No session ID`

**Causes:**
1. `.claude/project-session-id` file doesn't exist
2. File in wrong location
3. File has incorrect permissions

**Solution:**
- Create `.claude/project-session-id` file manually
- Place in project root or parent directory
- Ensure file is readable: `chmod 644 .claude/project-session-id`
- Pass session_id parameter directly

## Performance

### Benchmarks

**Test Environment:**
- Platform: Windows 10
- Python: 3.11
- Project Size: 45 files, 34 directories

**Results:**
```
analyze-structure.py:  ~0.2s  (100 tokens)
detect-patterns.py:    ~0.1s  (50 tokens)
generate-report.py:    ~0.1s  (50 tokens)
memory_integration.py: ~0.1s  (200 tokens)
────────────────────────────────────────
Total:                 ~0.5s  (400 tokens)
```

**Scalability:**
- Linear with file count
- Pattern detection: O(patterns × files)
- Expected: ~1s for 500 files, ~5s for 5,000 files

### Optimization Tips

1. **Skip large directories:**
   - Add to `_should_skip()` method
   - Examples: `node_modules`, `__pycache__`, `target`

2. **Reduce pattern count:**
   - Only load relevant patterns
   - Use conditional `applies_when` clauses

3. **Cache results:**
   - Store structure.json for reuse
   - Cache detection patterns YAML

4. **Parallel processing:**
   - Run pattern detection in parallel (future)
   - Use multiprocessing for large projects

## Maintenance

### Adding New Patterns

1. **Define pattern in detection-patterns.yaml:**
```yaml
- id: missing-jest-config
  type: file_absence
  check: jest.config.js
  confidence: medium
  severity: low
  recommendation:
    template: quality/testing/jest.config.js
    reason: "Jest config enables better test configuration"
  applies_when: "package.json exists"
```

2. **Create template (if needed):**
- Add template to `templates/` directory
- Follow standard YAML frontmatter format

3. **Test pattern:**
```bash
./analyze.sh /path/to/test-project
```

### Updating Confidence Scoring

1. **Modify confidence-scoring.yaml:**
```yaml
quality_thresholds:
  jest_config:
    min_test_files: 5
    required_sections:
      - testEnvironment
      - collectCoverage
    confidence_boost: 0.15
```

2. **Update PatternDetector._check_file_quality():**
```python
elif file_path == 'jest.config.js':
    # Custom jest config quality check
    return check_jest_quality(file_path, criteria)
```

3. **Test scoring:**
```bash
python detect-patterns.py structure.json detection-patterns.yaml
```

## License

MIT License - See LICENSE file for details.

## Support

For issues or questions:
- GitHub: https://github.com/jcmrs/project-catalyst
- Discussions: Project Catalyst GitHub Discussions
- ADR-002: Analyzer Design Documentation
