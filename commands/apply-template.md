# Apply Template

Apply a production-ready template from Project Catalyst's library to your project. Supports variable substitution and validation.

## What This Command Does

1. **Loads template** from Project Catalyst library
2. **Prompts for variables** (if template requires input)
3. **Substitutes variables** in template content
4. **Validates substitution** (ensures no missing variables)
5. **Writes file** to your project with proper permissions

## Usage

### Basic Usage

```
/apply-template <template-path>
```

### Examples

**Apply Node.js .gitignore:**
```
/apply-template git/gitignore/node
```

**Apply comprehensive README:**
```
/apply-template documentation/README-comprehensive
```

**Apply GitHub Actions CI workflow:**
```
/apply-template ci-cd/github-actions/ci-test
```

## Template Categories

**Git Templates:**
- `git/gitignore/node` - Node.js .gitignore
- `git/gitignore/python` - Python .gitignore
- `git/gitignore/java` - Java .gitignore
- `git/hooks/pre-commit` - Pre-commit hook
- `git/workflows/ci-test` - GitHub Actions CI workflow
- `git/workflows/release` - GitHub Actions release workflow

**Documentation Templates:**
- `documentation/README-comprehensive` - Full-featured README
- `documentation/README-minimal` - Minimal README
- `documentation/CONTRIBUTING` - Contribution guidelines

**CI/CD Templates:**
- `ci-cd/github-actions/build` - Build workflow
- `ci-cd/github-actions/ci-test` - Test workflow
- `ci-cd/docker/Dockerfile` - Basic Dockerfile

**Setup Templates:**
- `setup/licenses/MIT` - MIT License
- `setup/editorconfig/.editorconfig` - EditorConfig

**Quality Templates:**
- `quality/linting/eslint.config` - ESLint configuration
- `quality/formatting/.prettierrc` - Prettier configuration

## Variable Substitution

Templates may require variables. You'll be prompted:

```
📝 Template requires variables:

  PROJECT_NAME: Name of the project
  DESCRIPTION: Brief project description
  AUTHOR: Project author

Enter PROJECT_NAME: my-awesome-project
Enter DESCRIPTION: A tool for awesome things
Enter AUTHOR: jcmrs

✅ Template applied successfully to README.md
```

## Validation

After application, the template is validated:

- ✅ No unsubstituted variables remain
- ✅ File syntax is valid (if applicable)
- ✅ Permissions set correctly (for executable files)

## Output Location

Templates are written to standard locations:

- `.gitignore` → project root
- `README.md` → project root
- `.github/workflows/*.yml` → .github/workflows/
- `.editorconfig` → project root
- etc.

## Related Commands

- `/analyze-project` - Discover which templates you need
- `/optimize-setup` - Optimize applied templates
- `/health-check` - Verify template application
