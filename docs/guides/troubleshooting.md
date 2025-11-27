# Troubleshooting Guide

Experiencing issues with Project Catalyst? Find solutions to common problems here.

---

## Quick Reference

**Common Issues:**
- [Project not analyzed](#project-not-analyzed-error)
- [Template validation failing](#template-validation-failing)
- [Isolation enforcement issues](#isolation-enforcement-failures)
- [Hook execution problems](#hook-execution-problems)
- [Performance issues](#performance-issues)
- [Commands not working](#commands-not-responding)

---

## Project Not Analyzed Error

### Issue Description

When running `/analyze-project`, you get:

```
❌ Error: Project has not been analyzed
No analysis data available. Run /onboard first.
```

Or the analysis is empty/shows no results.

### Root Causes

1. **Project hasn't been analyzed yet** - New projects need initial analysis
2. **Analysis cache expired** - Analysis data older than 7 days
3. **Project directory changed** - Different project path than before
4. **Local memory not initialized** - MCP server not responding
5. **Incomplete plugin installation** - Missing analyzer script

### Solutions

#### Solution 1: Run Onboard First

✅ **For new projects:**

```bash
/onboard
```

This:
- Analyzes project structure
- Creates analysis cache
- Applies recommended templates

#### Solution 2: Force Re-Analysis

✅ **If cache expired:**

```bash
# Clear analysis cache
rm -rf ~/.claude/plugins/project-catalyst/.cache/analysis

# Re-run analysis
/analyze-project
```

#### Solution 3: Verify Project Directory

✅ **If using different path:**

```bash
# Check current project directory
echo $CLAUDE_PROJECT_DIR

# If wrong, ensure you're in correct directory
cd /path/to/actual/project
/analyze-project
```

#### Solution 4: Restart Local Memory

✅ **If MCP not responding:**

```bash
# Stop local memory server (if running)
ps aux | grep "local-memory"
kill -9 <PID>

# Reinitialize
bash ~/.claude/plugins/project-catalyst/scripts/setup-wizard.sh
```

#### Solution 5: Check Analyzer Script

✅ **If script missing:**

```bash
# Check if analyzer exists
ls -la ~/.claude/plugins/project-catalyst/scripts/

# Should show: health-check.sh, setup-wizard.sh, etc.

# If missing, reinstall
cd ~/.claude/plugins/project-catalyst
git pull origin main
```

### Verification

After fixing, verify:

```bash
# 1. Project directory is correct
pwd
ls -la | head -20

# 2. Analyzer script exists
ls -la ~/.claude/plugins/project-catalyst/scripts/health-check.sh

# 3. Run analysis
/analyze-project

# Expected output:
# 🔍 Project Analysis Results
# [analysis data]
```

---

## Template Validation Failing

### Issue Description

When applying templates:

```
⚠️ Warning: Template validation failed
❌ Invalid template variables found
Variables not substituted: {{PROJECT_NAME}}, {{AUTHOR}}
```

Or:

```
❌ Error: Template file not found at git/gitignore/node
```

### Root Causes

1. **Template file doesn't exist** - Wrong template path
2. **Variables missing** - Didn't provide required variables
3. **Template syntax error** - Invalid markup in template file
4. **File permissions issue** - Can't read template file
5. **Plugin directory wrong** - Using wrong install location

### Solutions

#### Solution 1: Verify Template Exists

✅ **Check if template available:**

```bash
# List available templates
ls -la ~/.claude/plugins/project-catalyst/templates/

# Should show: git/, documentation/, ci-cd/, quality/, setup/

# Check specific template
ls ~/.claude/plugins/project-catalyst/templates/git/gitignore/

# Should show: node.gitignore, python.gitignore, java.gitignore
```

**Fix:** Use correct template path from listing above.

#### Solution 2: Provide All Variables

✅ **When prompted, provide all variables:**

```
/apply-template documentation/README-comprehensive

# Prompts appear:
Enter AUTHOR: Jane Smith
Enter PROJECT_NAME: my-app
Enter DESCRIPTION: A task manager
# Provide all required variables before proceeding
```

**Common variables required:**
- `AUTHOR` - Your name
- `PROJECT_NAME` - Project name
- `DESCRIPTION` - Brief description
- `EMAIL` - Contact email

#### Solution 3: Validate Template Format

✅ **Check template file syntax:**

```bash
# Validate specific template
bash ~/.claude/plugins/project-catalyst/scripts/validate-template-format.sh \
  ~/.claude/plugins/project-catalyst/templates/git/gitignore/node.gitignore

# Output should be:
# ✅ Template format valid
```

If invalid, check for:
- Mismatched braces: `{{VARIABLE}` (missing closing brace)
- Invalid variable names (must be uppercase with underscores)
- Unicode encoding issues

#### Solution 4: Fix File Permissions

✅ **Ensure template readable:**

```bash
# Check permissions
ls -la ~/.claude/plugins/project-catalyst/templates/git/gitignore/

# Files should be readable (r--)
# Fix if needed:
chmod 644 ~/.claude/plugins/project-catalyst/templates/**/*
chmod 755 ~/.claude/plugins/project-catalyst/templates/**/
```

#### Solution 5: Verify Installation Path

✅ **Confirm correct installation:**

```bash
# Check where plugin is installed
echo $CLAUDE_PLUGIN_ROOT

# Should point to: ~/.claude/plugins/project-catalyst
# or: /Users/username/.claude/plugins/project-catalyst (macOS)
# or: C:\Users\username\.claude\plugins\project-catalyst (Windows)

# If wrong, reinstall to correct location
```

### Debugging

Enable debug mode:

```bash
# Run with verbose output
DEBUG=true /apply-template git/gitignore/node

# Should show:
# [DEBUG] Loading template from: .../templates/git/gitignore/node.gitignore
# [DEBUG] Found variables: {{AUTHOR}}, {{PROJECT_NAME}}
# [DEBUG] Substituting variables...
```

---

## Isolation Enforcement Failures

### Issue Description

Getting isolation-related errors:

```
❌ Error: Isolation validation failed
Detected cross-project file access
Memory operations require project isolation
```

Or commits being blocked:

```
❌ Pre-commit hook failed: Isolation validation
Cannot commit without proper isolation
```

### Root Causes

1. **Memory operations using wrong key** - Not prefixed with project ID
2. **Accessing files outside project** - Using paths with `../`
3. **Shared memory between projects** - Multiple projects using same memory key
4. **Relative paths in scripts** - Not using absolute paths
5. **Symlinks crossing project boundary** - Symbolic links outside project dir

### Solutions

#### Solution 1: Check Memory Key Format

✅ **Verify memory uses proper isolation:**

In scripts, ensure memory keys include project identifier:

```bash
# ❌ WRONG - not isolated
memory:read_graph project-info

# ✅ CORRECT - isolated with project prefix
memory:read_graph ${PROJECT_ID}:project-info
```

**Where `PROJECT_ID` is:**
```bash
PROJECT_ID=$(basename $CLAUDE_PROJECT_DIR)
```

#### Solution 2: Fix Path References

✅ **Use absolute paths with $CLAUDE_PROJECT_DIR:**

```bash
# ❌ WRONG - relative path
cd ../../../shared
cp file.txt .

# ✅ CORRECT - absolute path
cp "${CLAUDE_PROJECT_DIR}/templates/file.txt" .
```

#### Solution 3: Check for Symlinks

✅ **Find and fix problematic symlinks:**

```bash
# Find all symlinks
find "$CLAUDE_PROJECT_DIR" -type l

# For each symlink, check target
ls -la <symlink>

# If target outside project, remove and replace with copy:
rm <symlink>
cp <target> <symlink-location>
```

#### Solution 4: Verify Project Isolation

✅ **Test isolation validation:**

```bash
# Run isolation check
bash ~/.claude/plugins/project-catalyst/scripts/validate-isolation.sh

# Output should be:
# ✅ Isolation valid
# ✅ No cross-project access detected
# ✅ Memory operations properly isolated
```

If fails, examine output for specific violations.

#### Solution 5: Reset Isolation (Last Resort)

✅ **Only if above solutions don't work:**

```bash
# Clear isolation cache
rm -rf "${CLAUDE_PROJECT_DIR}/.claude/isolation-cache"

# Re-initialize
bash ~/.claude/plugins/project-catalyst/scripts/setup-wizard.sh

# Re-run validation
bash ~/.claude/plugins/project-catalyst/scripts/validate-isolation.sh
```

### Prevention

Add to your `.claude/CLAUDE.md`:

```markdown
## Project Isolation

All operations must use `${CLAUDE_PROJECT_DIR}` prefix:

```bash
# ✅ Correct
cp "${CLAUDE_PROJECT_DIR}/file.txt" .
memory:read ${PROJECT_ID}:key

# ❌ Incorrect
cp file.txt .
memory:read key
```
```

---

## Hook Execution Problems

### Issue Description

Hooks aren't running:

```
⚠️ Warning: Hook did not execute
❌ Hook validation failed
Pre-commit hook exited with status 127
```

Or hooks running but not doing anything:

```
[Hook running...]
(no output, hook appears stuck)
```

### Root Causes

1. **Hook script not executable** - Missing execute permission
2. **Script syntax error** - Bash error in script
3. **Command not found** - Missing dependencies
4. **Hook registration incorrect** - Wrong configuration in hooks.json
5. **Script path incorrect** - Path doesn't exist
6. **Timeout** - Hook taking too long

### Solutions

#### Solution 1: Make Scripts Executable

✅ **Ensure hook scripts are executable:**

```bash
# Check permissions
ls -la ~/.claude/plugins/project-catalyst/scripts/

# Should show: -rwxr-xr-x (executable)
# Fix if needed:
chmod +x ~/.claude/plugins/project-catalyst/scripts/*.sh
chmod +x ~/.claude/plugins/project-catalyst/hooks/custom/*.sh
```

#### Solution 2: Test Hook Script Manually

✅ **Run hook directly to see errors:**

```bash
# Test with explicit path
bash ~/.claude/plugins/project-catalyst/scripts/validate-isolation.sh

# Should output:
# ✅ Isolation valid
# Exit code 0

# If it fails, you'll see the error
```

#### Solution 3: Check Hook Registration

✅ **Verify hooks.json is correct:**

```bash
# View hook configuration
cat ~/.claude/plugins/project-catalyst/hooks/hooks.json

# Should have valid JSON structure:
# {
#   "hooks": {
#     "SessionStart": [...],
#     "PostToolUse": [...],
#     "PreCommit": [...]
#   }
# }

# Validate JSON syntax
python3 -m json.tool ~/.claude/plugins/project-catalyst/hooks/hooks.json
```

**Common issues:**
- Missing commas between entries
- Unmatched quotes
- Incorrect path separators (use forward slashes even on Windows)

#### Solution 4: Check Command Dependencies

✅ **Verify hook dependencies installed:**

```bash
# If hook uses external commands, verify they exist
which python3
which git
which npm

# If missing:
# macOS: brew install <command>
# Linux: sudo apt-get install <command>
# Windows: Install via package manager
```

#### Solution 5: Increase Timeout

✅ **If hook times out:**

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
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-isolation.sh",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

Timeout is in milliseconds. Increase as needed.

#### Solution 6: Enable Hook Debugging

✅ **Debug hook execution:**

```bash
# Set debug environment variable
export HOOK_DEBUG=1

# Re-run the trigger action
git commit -m "Test"

# Should show detailed hook output
```

Add to hook script:

```bash
#!/bin/bash
set -x  # Print each command before executing
# ... rest of script
set +x
```

---

## Performance Issues

### Issue Description

Project Catalyst running slowly:

```
⏳ /analyze-project taking >30 seconds
⏳ /health-check taking >10 seconds
⏳ Templates applying slowly
```

Or Claude Code becoming sluggish:

```
🔴 Claude Code responsiveness degraded
Hooks appear to hang
Memory usage increasing
```

### Root Causes

1. **Large project directory** - Analyzing huge codebases
2. **Slow disk** - Network drive or slow SSD
3. **Many files** - Large number of small files
4. **Memory pressure** - Other processes consuming RAM
5. **Inefficient patterns** - Unoptimized scripts or queries
6. **Nested isolation** - Multiple levels of project nesting

### Solutions

#### Solution 1: Check Disk Performance

✅ **Test disk speed:**

```bash
# macOS/Linux
time dd if=/dev/zero of=test.dat bs=1m count=100
rm test.dat

# Windows (PowerShell)
Measure-Command { 1..1000 | % { [System.IO.File]::WriteAllText("test.txt", "test") } }
```

If very slow (>100ms for writes), consider:
- Moving project to local SSD
- Closing other disk-heavy applications
- Checking disk for errors

#### Solution 2: Exclude Large Directories

✅ **Skip analysis on large folders:**

Edit analysis to skip node_modules, .git, etc:

```bash
# In scripts, exclude patterns
find "$PROJECT_DIR" -type f \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  ...
```

#### Solution 3: Cache Results Aggressively

✅ **Use longer cache timeout:**

Edit script caching:

```bash
# Increase cache validity
CACHE_DURATION=604800  # 7 days instead of 1 day

# Cache analysis results
echo "$analysis_output" > ~/.claude/plugins/project-catalyst/.cache/analysis
```

#### Solution 4: Reduce Analysis Scope

✅ **Run targeted analysis:**

```bash
# Instead of full analysis
/analyze-project --full

# Run faster specific analysis
/analyze-project --scope git
/analyze-project --scope documentation
/analyze-project --scope ci-cd
```

#### Solution 5: Disable Hooks During Development

✅ **Temporarily disable slow hooks:**

```bash
# Edit hooks.json, remove or comment out slow hooks

# Or set environment variable
export DISABLE_HOOKS=1

# Re-enable when done
unset DISABLE_HOOKS
```

#### Solution 6: Monitor Resource Usage

✅ **Check what's consuming resources:**

```bash
# Monitor during analysis
top -p $(pgrep -f "project-catalyst")

# Or use Activity Monitor (macOS) / Task Manager (Windows)

# Look for:
# - CPU usage >80%
# - Memory usage >500MB
# - Disk I/O constantly high
```

If any are consistently high, the performance issue is identified.

### Optimization Checklist

- [ ] Project on fast local SSD (not network drive)
- [ ] Large directories excluded from analysis
- [ ] Unnecessary hooks disabled
- [ ] Cache not corrupted: `rm -rf ~/.claude/plugins/project-catalyst/.cache`
- [ ] Latest version: `git pull origin main`
- [ ] No other heavy processes running
- [ ] Sufficient disk space (>1GB free)

---

## Commands Not Responding

### Issue Description

Commands hang or don't produce output:

```
/analyze-project
(appears to hang, no output for 2+ minutes)
```

Or:

```
❌ Error: Command failed with timeout
Command exceeded maximum execution time
```

### Root Causes

1. **Network issue** - Can't reach required services
2. **Process stuck** - Script in infinite loop
3. **Resource exhaustion** - Out of memory or disk space
4. **Missing dependencies** - Required tools not installed
5. **Stale process** - Old plugin process still running
6. **Timeout too short** - Command needs more time

### Solutions

#### Solution 1: Kill Hanging Processes

✅ **Stop stuck command:**

```bash
# Find hanging process
ps aux | grep project-catalyst

# Kill it
kill -9 <PID>

# Then retry command
/analyze-project
```

#### Solution 2: Check Network Connectivity

✅ **Verify network access:**

```bash
# Test internet connectivity
ping -c 3 google.com

# Test local services
curl http://localhost:3000/health  # local-memory MCP

# If failing, restart service:
bash ~/.claude/plugins/project-catalyst/scripts/setup-wizard.sh
```

#### Solution 3: Clear Cache and Temp Files

✅ **Remove potentially corrupted cache:**

```bash
# Clear cache
rm -rf ~/.claude/plugins/project-catalyst/.cache

# Clear temp files
rm -rf /tmp/project-catalyst-*

# Retry command
/analyze-project
```

#### Solution 4: Check System Resources

✅ **Ensure sufficient resources:**

```bash
# Check disk space
df -h

# Should have >1GB free on project drive

# Check memory
free -h  # Linux/macOS
Get-Volume  # Windows PowerShell

# If low, free up space or close other applications
```

#### Solution 5: Increase Timeout

✅ **Give command more time:**

In Claude Code settings or environment:

```bash
export COMMAND_TIMEOUT=60000  # 60 seconds instead of default
/analyze-project
```

#### Solution 6: Run Verbose Mode

✅ **Get detailed output:**

```bash
# Run with debug output
DEBUG=true /analyze-project

# Should show step-by-step execution
# Look for where it gets stuck
```

---

## Getting Help

### Before Reporting Issues

1. **Check this guide** - Your issue likely covered above
2. **Check [Installation Guide](./installation.md)** - Setup issues
3. **Check [Customization Guide](./customization.md)** - Configuration issues
4. **Run diagnostics:**

```bash
# Self-diagnosis script
bash ~/.claude/plugins/project-catalyst/scripts/check-analyzed.sh
```

### How to Report Issues

**On GitHub Issues:**

Include:
```
## Environment
- OS: [Windows/macOS/Linux]
- Claude Code version: [output of `claude --version`]
- Plugin version: [check plugin.json]

## Problem
[Detailed description]

## Steps to Reproduce
1. ...
2. ...
3. ...

## Expected vs Actual
- Expected: [what should happen]
- Actual: [what happens]

## Error Output
[Full error message/logs]

## Diagnostics
- `bash scripts/check-analyzed.sh`: [output]
- `bash scripts/health-check.sh`: [output]
- Installation verification: [pass/fail]
```

### Getting Answers

- **[GitHub Issues](https://github.com/jcmrs/project-catalyst/issues)** - Bug reports
- **[GitHub Discussions](https://github.com/jcmrs/project-catalyst/discussions)** - Questions
- **[Documentation](../../../README.md)** - Comprehensive guides

---

## Contacting Support

### Primary Support Channels

1. **GitHub Issues** - Bug reports and feature requests
2. **GitHub Discussions** - Questions and help
3. **Email** - jcmrs@users.noreply.github.com

### Information to Include

Always provide:
- OS and version
- Claude Code version
- Steps to reproduce
- Error messages/logs
- Project type (language, framework)

---

## Common Questions

**Q: Why is analyze-project slow on my huge codebase?**
A: Large projects take time to scan. Use `--scope` to analyze specific areas, or increase cache timeout.

**Q: Can I disable certain hooks?**
A: Yes, edit `hooks/hooks.json` or set `DISABLE_HOOKS=1`.

**Q: Do I lose data if I reinstall?**
A: No, reinstalling the plugin doesn't affect your projects. Templates are in `templates/` directory.

**Q: Can hooks fail without blocking work?**
A: Yes, set `required: false` in hooks.json for non-critical hooks.

**Q: How do I reset everything?**
A: Remove plugin: `rm -rf ~/.claude/plugins/project-catalyst` and reinstall from scratch.

---

## Diagnostic Commands

Keep these handy for troubleshooting:

```bash
# Check installation
bash ~/.claude/plugins/project-catalyst/scripts/check-analyzed.sh

# Quick health check
/health-check

# Detailed analysis
/analyze-project --detailed

# Validate templates
bash ~/.claude/plugins/project-catalyst/scripts/validate-template-format.sh

# Check isolation
bash ~/.claude/plugins/project-catalyst/scripts/validate-isolation.sh

# Clear cache
rm -rf ~/.claude/plugins/project-catalyst/.cache

# Test local memory
curl http://localhost:3000/health
```

---

**Still stuck?** Open a [GitHub Issue](https://github.com/jcmrs/project-catalyst/issues) with your diagnostics!
