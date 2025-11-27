# Installation Guide

Welcome to Project Catalyst! This guide will walk you through installing and verifying the plugin in your Claude Code environment.

---

## Prerequisites

Before installing Project Catalyst, ensure you have:

- **Claude Code** (v1.0.0 or later)
  - [Download Claude Code](https://claude.ai/code)
  - Verify: `claude --version`

- **Git** (v2.25.0 or later)
  - [Download Git](https://git-scm.com/downloads)
  - Verify: `git --version`

- **Bash** (v4.0 or later)
  - macOS/Linux: Pre-installed
  - Windows: [Git Bash](https://git-scm.com/download/win) or WSL2
  - Verify: `bash --version`

- **5 MB disk space** for plugin and templates

---

## Installation Steps

### Step 1: Clone the Repository

Choose your preferred location and clone:

```bash
# Clone to your plugins directory (recommended)
git clone https://github.com/jcmrs/project-catalyst.git \
  ~/.claude/plugins/project-catalyst

# Navigate to plugin directory
cd ~/.claude/plugins/project-catalyst
```

**Alternative: Manual Installation**

If you prefer, download and extract:

1. Download: https://github.com/jcmrs/project-catalyst/releases/latest
2. Extract to: `~/.claude/plugins/project-catalyst`
3. Navigate: `cd ~/.claude/plugins/project-catalyst`

### Step 2: Run the Setup Wizard

Initialize the plugin in your Claude Code environment:

```bash
bash ./scripts/setup-wizard.sh
```

The wizard will:

- Detect your Claude Code installation
- Verify prerequisites (Git, Bash)
- Configure plugin paths
- Create necessary directories
- Initialize local memory storage

**Expected Output:**

```
✅ Claude Code detected at: /path/to/claude
✅ Git version: 2.40.0
✅ Bash version: 5.1.4
✅ Plugin directory writable
✅ Setup complete!

Next step: Run /onboard to set up your first project
```

### Step 3: Verify Installation

Test that everything is working:

```bash
bash ./scripts/check-analyzed.sh
```

**Expected Output:**

```
✅ Project Catalyst is installed and ready!
✅ Commands available: /onboard, /analyze-project, /health-check, /apply-template
```

Alternatively, in Claude Code, type:

```
/health-check
```

You should see a health assessment of your current project.

---

## Platform-Specific Notes

### Windows (Git Bash)

#### Installation

1. **Install Git Bash:**
   - Download from [git-scm.com](https://git-scm.com/download/win)
   - Choose "Git Bash Here" during installation
   - Verify: Open Git Bash and run `bash --version`

2. **Clone the Repository:**
   ```bash
   cd ~/.claude/plugins
   git clone https://github.com/jcmrs/project-catalyst.git
   ```

3. **Run Setup:**
   ```bash
   cd project-catalyst
   bash scripts/setup-wizard.sh
   ```

#### Path Handling

Project Catalyst automatically converts paths:
- Windows: `C:\Users\jcmei\projects\my-app`
- Git Bash: `/c/Users/jcmei/projects/my-app`

No manual conversion needed!

#### Troubleshooting

**Issue:** "bash: command not found"
- **Solution:** Install Git Bash (see above)

**Issue:** "Permission denied" on scripts
- **Solution:** Run: `chmod +x scripts/*.sh`

**Issue:** Scripts timeout
- **Solution:** Increase timeout in `scripts/setup-wizard.sh` (look for `TIMEOUT=`)

### macOS

#### Installation

1. **Ensure Bash 4+:**
   ```bash
   # macOS ships with Bash 3.2
   # Install Bash 4+ via Homebrew
   brew install bash
   ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/jcmrs/project-catalyst.git \
     ~/.claude/plugins/project-catalyst
   ```

3. **Run Setup:**
   ```bash
   cd ~/.claude/plugins/project-catalyst
   bash ./scripts/setup-wizard.sh
   ```

#### Important Notes

- Make sure `/usr/local/bin/bash` is used, not `/bin/bash`
- Update your shell: `chsh -s /usr/local/bin/bash`

### Linux

#### Installation

1. **Ensure Prerequisites:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install git bash

   # CentOS/RHEL
   sudo yum install git bash

   # Verify versions
   git --version    # Should be 2.25+
   bash --version   # Should be 4.0+
   ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/jcmrs/project-catalyst.git \
     ~/.claude/plugins/project-catalyst
   ```

3. **Run Setup:**
   ```bash
   cd ~/.claude/plugins/project-catalyst
   bash ./scripts/setup-wizard.sh
   ```

#### Linux-Specific Tips

- Use your system's package manager for Git/Bash
- Plugin directory should be readable/writable by your user
- SELinux: May need to adjust file contexts if you get permission errors

---

## Troubleshooting Installation

### "Claude Code not found"

❌ **Error:** Setup wizard can't find Claude Code installation

**Solutions:**

1. **Verify Claude Code is installed:**
   ```bash
   which claude
   claude --version
   ```

2. **Set Claude Code path manually:**
   ```bash
   export CLAUDE_HOME="/path/to/claude"
   bash scripts/setup-wizard.sh
   ```

3. **Check installation location:**
   - Windows: `C:\Users\YourName\AppData\Local\Claude`
   - macOS: `/Applications/Claude.app`
   - Linux: `~/.local/share/claude`

### "Git not found"

❌ **Error:** Git is not installed or not in PATH

**Solutions:**

1. **Install Git:**
   - Windows: [git-scm.com](https://git-scm.com/download/win)
   - macOS: `brew install git`
   - Linux: `sudo apt-get install git` (Ubuntu/Debian)

2. **Verify Git PATH:**
   ```bash
   git --version
   which git
   ```

3. **Add to PATH (if needed):**
   ```bash
   export PATH="/usr/local/bin:$PATH"
   ```

### "Permission denied" on script execution

❌ **Error:** `bash: scripts/setup-wizard.sh: Permission denied`

**Solutions:**

1. **Make scripts executable:**
   ```bash
   chmod +x scripts/*.sh
   ```

2. **Run with explicit bash:**
   ```bash
   bash scripts/setup-wizard.sh
   ```

3. **Check file ownership:**
   ```bash
   ls -la scripts/setup-wizard.sh
   # Should show your username as owner
   ```

### "Port already in use" (local-memory MCP)

❌ **Error:** Setup wizard reports port conflict

**Solutions:**

1. **Find process using port:**
   ```bash
   # Find process on port 3000 (default)
   lsof -i :3000

   # Kill the process
   kill -9 <PID>
   ```

2. **Use different port:**
   ```bash
   export LOCAL_MEMORY_PORT=3001
   bash scripts/setup-wizard.sh
   ```

### "Template validation failed"

❌ **Error:** Templates fail validation after installation

**Solutions:**

1. **Re-run setup wizard:**
   ```bash
   bash scripts/setup-wizard.sh
   ```

2. **Check template directory:**
   ```bash
   ls -la templates/
   # Should show git/, documentation/, ci-cd/, quality/, setup/
   ```

3. **Validate templates manually:**
   ```bash
   bash scripts/validate-template-format.sh
   ```

### "Module import errors"

❌ **Error:** Python module not found during setup

**Solutions:**

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   .\venv\Scripts\activate   # Windows

   pip install -r requirements.txt
   ```

---

## Verify Complete Installation

Run this checklist after installation:

```bash
# 1. Check Claude Code
claude --version

# 2. Check Git
git --version

# 3. Check Bash
bash --version

# 4. Check plugin directory
ls -la ~/.claude/plugins/project-catalyst/

# 5. Check templates
ls -la templates/

# 6. Check scripts are executable
ls -la scripts/

# 7. Test in Claude Code
/health-check
```

All checks should return ✅ status.

---

## Next Steps

Congratulations! Project Catalyst is installed and ready to use.

### Quick Start

1. **Get Started with a New Project:**
   ```
   /onboard
   ```
   See [Getting Started Guide](./getting-started.md) for walkthrough

2. **Analyze an Existing Project:**
   ```
   /analyze-project
   ```

3. **Apply Individual Templates:**
   ```
   /apply-template git/gitignore/node
   ```

4. **Check Project Health:**
   ```
   /health-check
   ```

### Learn More

- **[Getting Started Guide](./getting-started.md)** - First-time setup walkthrough
- **[Customization Guide](./customization.md)** - Create custom templates and hooks
- **[Troubleshooting Guide](./troubleshooting.md)** - Common issues and solutions

### Support

- **Issues:** [GitHub Issues](https://github.com/jcmrs/project-catalyst/issues)
- **Discussions:** [GitHub Discussions](https://github.com/jcmrs/project-catalyst/discussions)
- **Documentation:** See `/docs` directory

---

**Installation Complete!** Ready to set up your first project? Jump to [Getting Started](./getting-started.md).
