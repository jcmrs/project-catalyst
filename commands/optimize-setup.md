# Optimize Setup

Optimize existing project configuration by analyzing current setup and recommending improvements. Unlike `/analyze-project` which detects missing files, this command improves existing ones.

## What This Command Does

1. **Analyzes existing configuration files** (gitignore, CI/CD, linters, etc.)
2. **Compares against best practices** from Project Catalyst
3. **Identifies improvement opportunities** (missing patterns, outdated config, etc.)
4. **Suggests optimizations** with confidence scores
5. **Provides upgrade paths** for existing files

## Usage

```
/optimize-setup
```

### Analyze Specific Category

```
/optimize-setup --category git
/optimize-setup --category ci-cd
/optimize-setup --category quality
```

## What Gets Optimized

**Git Configuration:**
- .gitignore completeness (missing common patterns)
- Git hooks efficiency
- Workflow optimizations (caching, parallelization)

**CI/CD:**
- GitHub Actions workflow improvements
- Build time optimizations
- Cache configuration
- Matrix testing strategies

**Code Quality:**
- Linter rule updates
- Formatter configuration improvements
- Test coverage enhancements

**Documentation:**
- README completeness
- Missing sections
- Outdated information

## Example Output

```
🔧 Optimization Recommendations

.gitignore:
  ⚠️  Missing 12 common Node.js patterns (confidence: high)
     Patterns: .pnpm-debug.log*, .yarn/cache, etc.
     → Action: Update with enhanced patterns

.github/workflows/ci.yml:
  💡 Can improve build time by 40% (confidence: medium)
     - Add npm cache
     - Run tests in parallel
     - Use matrix strategy
     → Action: Apply optimizations

eslint.config.js:
  📦 Using outdated rules (confidence: high)
     - 5 deprecated rules found
     - 8 new recommended rules available
     → Action: Upgrade to ESLint 9.x config

README.md:
  📝 Missing 3 recommended sections (confidence: medium)
     - Installation instructions
     - Contributing guidelines link
     - License badge
     → Action: Enhance documentation

Priority Optimizations:
  1. Update .gitignore (2 min, high impact)
  2. Optimize CI/CD workflow (5 min, high impact)
  3. Upgrade ESLint config (10 min, medium impact)
```

## Optimization Modes

**Safe Mode (default):**
- Only suggests backward-compatible changes
- No breaking modifications
- Easy to roll back

**Aggressive Mode:**
```
/optimize-setup --aggressive
```
- Suggests breaking changes if beneficial
- Major version upgrades
- Modern best practices (may require code changes)

## Before/After Previews

For each optimization, see what will change:

```
📊 .gitignore Optimization

Current (15 patterns):
  node_modules/
  dist/
  .env

Optimized (27 patterns):
  node_modules/
  dist/
  .env
  + .pnpm-debug.log*
  + .yarn/cache
  + *.tsbuildinfo
  + ... (9 more patterns)

Impact: Prevents 12 common accidental commits
```

## Apply Optimizations

After review, apply recommended optimizations:

```
Apply all optimizations? (y/n): y
✅ .gitignore updated (12 patterns added)
✅ CI workflow optimized (build time: 3m → 1.8m)
✅ ESLint config upgraded
```

## Related Commands

- `/analyze-project` - Detect missing files
- `/apply-template` - Add new templates
- `/health-check` - Verify optimizations
