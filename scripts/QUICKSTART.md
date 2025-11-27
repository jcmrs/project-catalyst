# Setup Wizard - Quick Start Guide

## 🚀 One-Minute Setup

```bash
./scripts/setup-wizard.sh
```

That's it! The wizard will:
1. ✅ Detect your project type
2. ✅ Create `.catalyst/` directory
3. ✅ Ask about your preferences
4. ✅ Save configuration
5. ✅ Show next steps

---

## 📋 What Gets Created

After setup, you'll have:

```
.catalyst/
├── setup.log           ← All operations logged here
├── config.json         ← Your preferences
├── analyzed            ← Analysis timestamp
├── setup-complete      ← Completion flag
└── templates/          ← Templates directory
```

---

## 🎯 Common Commands

### Interactive Setup (Recommended)
```bash
./scripts/setup-wizard.sh
```

### Preview Changes (No Modifications)
```bash
./scripts/setup-wizard.sh --dry-run
```

### Detailed Logging
```bash
./scripts/setup-wizard.sh --verbose
```

### Without Colors (CI/CD)
```bash
./scripts/setup-wizard.sh --no-color
```

### Help
```bash
./scripts/setup-wizard.sh --help
```

---

## 🔍 Project Types Detected

The wizard automatically detects:

- **Node.js** - package.json, yarn.lock, pnpm-lock.yaml
- **Python** - setup.py, pyproject.toml, requirements.txt
- **Java** - pom.xml, build.gradle
- **Rust** - Cargo.toml
- **Go** - go.mod, go.sum
- **Ruby** - Gemfile, Rakefile
- **PHP** - composer.json
- **C#** - *.csproj, *.sln

---

## ⚙️ Configuration Options

During setup, you'll be asked:

1. **Run full analysis?** (Recommended: Yes)
   - Scans project structure
   - Provides detailed findings
   - Generates recommendations

2. **Auto-run analyzer on startup?** (Default: Yes)
   - Automatically analyze on session start
   - Keep insights current

3. **Suggest templates automatically?** (Default: Yes)
   - Get template recommendations
   - Speed up setup

4. **Validation strictness?** (Options: strict/moderate/relaxed)
   - **Strict:** Fail on any issues
   - **Moderate:** Fail on critical only
   - **Relaxed:** Log issues, don't fail

---

## 📖 Output Meanings

| Symbol | Meaning |
|--------|---------|
| ✅ | Success - operation completed |
| ❌ | Error - operation failed |
| ⚠️ | Warning - non-critical issue |
| 💡 | Info - helpful information |
| 🔍 | Search - analyzing project |

---

## 🛠️ Troubleshooting

### "Permission denied"
```bash
chmod +x scripts/setup-wizard.sh
```

### "Bash 4.4 or later required"
- macOS: `brew install bash`
- Linux: Update system Bash

### Colors look weird
```bash
./scripts/setup-wizard.sh --no-color
```

### Need to reconfigure
Just run the wizard again - it will prompt for reconfiguration

---

## 📂 File Locations

| File | Purpose |
|------|---------|
| `.catalyst/setup.log` | Full operation log |
| `.catalyst/config.json` | Your preferences |
| `.catalyst/analyzed` | Analysis was run |
| `.catalyst/setup-complete` | Setup finished |

---

## ✨ What's Next

After setup:

1. **Review configuration**
   ```bash
   cat .catalyst/config.json
   ```

2. **Check setup log**
   ```bash
   tail .catalyst/setup.log
   ```

3. **Run analyzer again** (if available)
   - Check project structure
   - Get recommendations
   - Review findings

4. **Apply templates**
   - Use recommended templates
   - Configure your project
   - Start development

---

## 💡 Tips

- **First time?** Just say "Yes" to all questions
- **Reconfiguring?** Wizard won't overwrite existing files
- **CI/CD?** Use `--dry-run --no-color` to preview
- **Debugging?** Use `--verbose` to see all details
- **Stuck?** Check `.catalyst/setup.log` for errors

---

## 🔗 More Information

- **Full Guide:** See `SETUP_WIZARD_README.md`
- **Implementation Details:** See `IMPLEMENTATION_SUMMARY.md`
- **Testing:** See `test-setup-wizard.sh`

---

**Ready?** Just run:
```bash
./scripts/setup-wizard.sh
```

Your Project Catalyst setup is just seconds away! 🚀
