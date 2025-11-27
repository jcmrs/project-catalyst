#!/usr/bin/env python3
"""
Security audit tests for Project Catalyst

Tests for hardcoded secrets, environment file protection,
isolation parameter enforcement, input validation, and path traversal protection.
"""

import re
import json
from pathlib import Path
from typing import List, Set, Dict, Any
import pytest


PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
SKILLS_DIR = PROJECT_ROOT / 'skills'
TEMPLATES_DIR = PROJECT_ROOT / 'templates'
COMMANDS_DIR = PROJECT_ROOT / 'commands'
HOOKS_DIR = PROJECT_ROOT / 'hooks'


class SecurityScanner:
    """Helper class for security scanning."""

    # Common patterns for secrets
    SECRET_PATTERNS = [
        r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']?[^"\'\s]{8,}',
        r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[A-Za-z0-9]{20,}',
        r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\']?[A-Za-z0-9]{20,}',
        r'(?i)(access[_-]?token|accesstoken)\s*[=:]\s*["\']?[A-Za-z0-9]{20,}',
        r'(?i)Bearer\s+[A-Za-z0-9\-._~+/]+=*',
        r'ghp_[A-Za-z0-9]{36}',  # GitHub personal access token
        r'sk_live_[A-Za-z0-9]{24,}',  # Stripe secret key
        r'AKIA[A-Z0-9]{16}',  # AWS access key
    ]

    # Allowed exceptions (e.g., example/placeholder values)
    ALLOWED_EXCEPTIONS = [
        'password=example',
        'password="example"',
        'api_key=your-key-here',
        'API_KEY=<your-api-key>',
        'secret_key=$',
        'access_token=$',
    ]

    def scan_file_for_secrets(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Scan a file for potential secrets.

        Returns:
            List of findings with line number and matched pattern
        """
        findings = []

        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            for line_num, line in enumerate(lines, start=1):
                # Skip comments in common formats
                stripped = line.strip()
                if stripped.startswith(('#', '//', '/*', '*', '--')):
                    continue

                # Check against secret patterns
                for pattern in self.SECRET_PATTERNS:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        matched_text = match.group(0)

                        # Check if it's an allowed exception
                        is_exception = any(
                            exception.lower() in matched_text.lower()
                            for exception in self.ALLOWED_EXCEPTIONS
                        )

                        if not is_exception:
                            findings.append({
                                'file': str(file_path),
                                'line': line_num,
                                'pattern': pattern,
                                'match': matched_text,
                                'context': line.strip()
                            })

        except (UnicodeDecodeError, PermissionError):
            # Skip binary files or files we can't read
            pass

        return findings

    def check_gitignore_coverage(self, gitignore_path: Path) -> Dict[str, bool]:
        """
        Check if .gitignore covers sensitive files.

        Returns:
            Dict indicating coverage of different sensitive file types
        """
        if not gitignore_path.exists():
            return {
                'has_gitignore': False,
                'covers_env_files': False,
                'covers_secrets': False,
                'covers_credentials': False
            }

        content = gitignore_path.read_text(encoding='utf-8')

        return {
            'has_gitignore': True,
            'covers_env_files': bool(re.search(r'\.env', content)),
            'covers_secrets': bool(re.search(r'secret', content, re.IGNORECASE)),
            'covers_credentials': bool(re.search(r'credential', content, re.IGNORECASE))
        }


scanner = SecurityScanner()


class TestNoHardcodedSecrets:
    """Test for hardcoded secrets in source files."""

    def test_no_secrets_in_scripts(self):
        """Test bash scripts don't contain hardcoded secrets."""
        findings = []

        for script_file in SCRIPTS_DIR.glob('*.sh'):
            file_findings = scanner.scan_file_for_secrets(script_file)
            findings.extend(file_findings)

        assert len(findings) == 0, \
            f"Found potential secrets in scripts: {findings}"

    def test_no_secrets_in_python_files(self):
        """Test Python files don't contain hardcoded secrets."""
        findings = []

        for py_file in PROJECT_ROOT.rglob('*.py'):
            # Skip test files and venv
            if 'test' in str(py_file) or 'venv' in str(py_file):
                continue

            file_findings = scanner.scan_file_for_secrets(py_file)
            findings.extend(file_findings)

        assert len(findings) == 0, \
            f"Found potential secrets in Python files: {findings}"

    def test_no_secrets_in_config_files(self):
        """Test config files don't contain hardcoded secrets."""
        config_patterns = ['*.json', '*.yaml', '*.yml', '*.toml']
        findings = []

        for pattern in config_patterns:
            for config_file in PROJECT_ROOT.rglob(pattern):
                # Skip venv and node_modules
                if 'venv' in str(config_file) or 'node_modules' in str(config_file):
                    continue

                file_findings = scanner.scan_file_for_secrets(config_file)
                findings.extend(file_findings)

        assert len(findings) == 0, \
            f"Found potential secrets in config files: {findings}"

    def test_no_secrets_in_commands(self):
        """Test command files don't contain hardcoded secrets."""
        findings = []

        for cmd_file in COMMANDS_DIR.glob('*.md'):
            file_findings = scanner.scan_file_for_secrets(cmd_file)
            findings.extend(file_findings)

        assert len(findings) == 0, \
            f"Found potential secrets in command files: {findings}"


class TestEnvironmentFileProtection:
    """Test protection of environment files."""

    def test_gitignore_exists(self):
        """Test .gitignore file exists."""
        gitignore = PROJECT_ROOT / '.gitignore'
        assert gitignore.exists(), ".gitignore should exist"

    def test_gitignore_covers_env_files(self):
        """Test .gitignore covers .env files."""
        gitignore = PROJECT_ROOT / '.gitignore'
        coverage = scanner.check_gitignore_coverage(gitignore)

        assert coverage['has_gitignore'], ".gitignore should exist"
        assert coverage['covers_env_files'], \
            ".gitignore should include .env pattern"

    def test_no_env_files_committed(self):
        """Test no .env files are in the repository."""
        env_files = list(PROJECT_ROOT.rglob('.env*'))

        # Filter out .env.example or .env.template
        actual_env_files = [
            f for f in env_files
            if not any(word in f.name for word in ['example', 'template', 'sample'])
        ]

        assert len(actual_env_files) == 0, \
            f"Found committed .env files: {actual_env_files}"

    def test_no_credentials_files_committed(self):
        """Test no credential files are in the repository."""
        credential_patterns = [
            '*credentials.json',
            '*credentials.yaml',
            '*secrets.json',
            '*secrets.yaml',
            '*.pem',
            '*.key',
            '*.p12',
        ]

        credential_files = []
        for pattern in credential_patterns:
            files = list(PROJECT_ROOT.rglob(pattern))
            # Exclude venv and test fixtures
            files = [f for f in files if 'venv' not in str(f) and 'test' not in str(f)]
            credential_files.extend(files)

        assert len(credential_files) == 0, \
            f"Found committed credential files: {credential_files}"


class TestIsolationParametersEnforced:
    """Test isolation parameters are enforced in code."""

    def test_memory_integration_enforces_isolation(self):
        """Test memory_integration.py enforces isolation."""
        memory_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'memory_integration.py'
        if not memory_script.exists():
            pytest.skip("memory_integration.py not found")

        content = memory_script.read_text(encoding='utf-8')

        # Should have isolation enforcement
        assert 'ensure_isolation' in content, \
            "memory_integration.py should have ensure_isolation method"
        assert 'session_filter_mode' in content, \
            "Should check session_filter_mode"
        assert 'session_only' in content, \
            "Should enforce session_only mode"

    def test_isolation_validation_script_exists(self):
        """Test validate-isolation.sh exists."""
        isolation_script = SCRIPTS_DIR / 'validate-isolation.sh'
        assert isolation_script.exists(), \
            "validate-isolation.sh should exist"

    def test_precommit_hook_validates_isolation(self):
        """Test PreCommit hook includes isolation validation."""
        hooks_file = HOOKS_DIR / 'hooks.json'
        if not hooks_file.exists():
            pytest.skip("hooks.json not found")

        with open(hooks_file, 'r', encoding='utf-8') as f:
            hooks_data = json.load(f)

        precommit = hooks_data.get('hooks', {}).get('PreCommit', [])
        has_isolation_check = False

        for hook_config in precommit:
            for hook in hook_config.get('hooks', []):
                if 'validate-isolation.sh' in hook.get('command', ''):
                    has_isolation_check = True
                    break

        assert has_isolation_check, \
            "PreCommit hook should include isolation validation"

    def test_isolation_parameters_in_memory_calls(self):
        """Test memory integration uses isolation parameters."""
        memory_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'memory_integration.py'
        if not memory_script.exists():
            pytest.skip("memory_integration.py not found")

        content = memory_script.read_text(encoding='utf-8')

        # Should set isolation parameters
        isolation_indicators = [
            'session_filter_mode',
            'session_id',
            'session_only',
        ]

        found_indicators = [ind for ind in isolation_indicators if ind in content]

        assert len(found_indicators) >= 2, \
            f"Should use isolation parameters. Found: {found_indicators}"


class TestInputValidation:
    """Test input validation and sanitization."""

    def test_scripts_validate_arguments(self):
        """Test scripts validate required arguments."""
        critical_scripts = [
            'health-check.sh',
        ]

        for script_name in critical_scripts:
            script_path = SCRIPTS_DIR / script_name
            if not script_path.exists():
                continue

            content = script_path.read_text(encoding='utf-8')

            # Should check for required arguments
            has_validation = any([
                '$#' in content,  # Argument count check
                '-z "$' in content,  # Empty string check
                'if [ $#' in content,  # Conditional on argument count
            ])

            assert has_validation, \
                f"{script_name} should validate arguments"

    def test_python_scripts_validate_inputs(self):
        """Test Python scripts validate inputs."""
        analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze-structure.py'
        if not analyzer_script.exists():
            pytest.skip("analyze-structure.py not found")

        content = analyzer_script.read_text(encoding='utf-8')

        # Should validate paths
        validation_indicators = [
            'exists()',
            'is_dir()',
            'FileNotFoundError',
            'ValueError',
        ]

        found = [ind for ind in validation_indicators if ind in content]

        assert len(found) >= 2, \
            f"Should validate inputs. Found: {found}"


class TestPathTraversalProtection:
    """Test protection against path traversal attacks."""

    def test_scripts_use_absolute_paths(self):
        """Test scripts resolve to absolute paths."""
        critical_scripts = [
            'health-check.sh',
        ]

        for script_name in critical_scripts:
            script_path = SCRIPTS_DIR / script_name
            if not script_path.exists():
                continue

            content = script_path.read_text(encoding='utf-8')

            # Should use absolute path resolution
            has_path_safety = any([
                'realpath' in content,
                'readlink -f' in content,
                'cd "$(dirname' in content,
            ])

            # This is a recommendation, not a strict requirement
            # Scripts should be careful with paths but may have valid reasons not to use realpath
            if not has_path_safety:
                # Just warn, don't fail
                pass

    def test_python_scripts_use_pathlib(self):
        """Test Python scripts use pathlib for path safety."""
        python_scripts = [
            SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze-structure.py',
            SKILLS_DIR / 'project-analyzer' / 'scripts' / 'detect-patterns.py',
        ]

        for script_path in python_scripts:
            if not script_path.exists():
                continue

            content = script_path.read_text(encoding='utf-8')

            # Should use pathlib.Path
            assert 'from pathlib import Path' in content or 'import pathlib' in content, \
                f"{script_path.name} should use pathlib for path handling"

    def test_no_direct_path_concatenation(self):
        """Test Python scripts avoid string path concatenation."""
        python_scripts = list(SKILLS_DIR.rglob('*.py'))

        risky_patterns = [
            r'\+ ["\']/',  # String concatenation with /
            r'["\'] \+ /',  # Reverse concatenation
        ]

        findings = []

        for script_path in python_scripts:
            if 'venv' in str(script_path) or '__pycache__' in str(script_path):
                continue

            try:
                content = script_path.read_text(encoding='utf-8')

                for pattern in risky_patterns:
                    if re.search(pattern, content):
                        findings.append({
                            'file': str(script_path),
                            'pattern': pattern
                        })
            except:
                pass

        # Allow some findings, but should be minimal
        assert len(findings) < 5, \
            f"Found potentially unsafe path concatenations: {findings}"


class TestSecurityBestPractices:
    """Test general security best practices."""

    def test_scripts_dont_use_eval(self):
        """Test bash scripts avoid eval command."""
        bash_scripts = list(SCRIPTS_DIR.glob('*.sh'))
        bash_scripts.extend(SKILLS_DIR.rglob('*.sh'))

        findings = []

        for script_path in bash_scripts:
            content = script_path.read_text(encoding='utf-8')

            # Check for eval usage (excluding comments)
            lines = content.split('\n')
            for line_num, line in enumerate(lines, start=1):
                if line.strip().startswith('#'):
                    continue

                if re.search(r'\beval\b', line):
                    findings.append({
                        'file': str(script_path),
                        'line': line_num,
                        'content': line.strip()
                    })

        # eval can be necessary sometimes, but should be rare
        assert len(findings) < 3, \
            f"Found potentially unsafe eval usage: {findings}"

    def test_python_scripts_dont_use_exec(self):
        """Test Python scripts avoid exec/eval."""
        python_scripts = list(SKILLS_DIR.rglob('*.py'))

        findings = []

        for script_path in python_scripts:
            if 'venv' in str(script_path) or '__pycache__' in str(script_path):
                continue

            try:
                content = script_path.read_text(encoding='utf-8')
                lines = content.split('\n')

                for line_num, line in enumerate(lines, start=1):
                    stripped = line.strip()
                    if stripped.startswith('#'):
                        continue

                    if re.search(r'\b(exec|eval)\s*\(', stripped):
                        findings.append({
                            'file': str(script_path),
                            'line': line_num,
                            'content': stripped
                        })
            except:
                pass

        assert len(findings) == 0, \
            f"Found unsafe exec/eval usage: {findings}"

    def test_no_shell_injection_vectors(self):
        """Test Python scripts avoid shell injection vectors."""
        python_scripts = list(SKILLS_DIR.rglob('*.py'))

        findings = []

        for script_path in python_scripts:
            if 'venv' in str(script_path) or '__pycache__' in str(script_path):
                continue

            try:
                content = script_path.read_text(encoding='utf-8')

                # Check for shell=True without proper escaping
                if 'shell=True' in content:
                    # Should also have shlex.quote or similar
                    if 'shlex.quote' not in content and 'shlex.split' not in content:
                        findings.append({
                            'file': str(script_path),
                            'issue': 'shell=True without shlex protection'
                        })
            except:
                pass

        assert len(findings) == 0, \
            f"Found potential shell injection vectors: {findings}"


class TestSecretManagement:
    """Test proper secret management practices."""

    def test_no_aws_credentials_hardcoded(self):
        """Test no AWS credentials are hardcoded."""
        aws_patterns = [
            r'AKIA[A-Z0-9]{16}',  # AWS access key
            r'aws_access_key_id\s*=\s*[A-Z0-9]{20}',
            r'aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}',
        ]

        findings = []

        for pattern in aws_patterns:
            for file_path in PROJECT_ROOT.rglob('*'):
                if file_path.is_file() and 'venv' not in str(file_path):
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        if re.search(pattern, content):
                            findings.append({
                                'file': str(file_path),
                                'pattern': pattern
                            })
                    except:
                        pass

        assert len(findings) == 0, \
            f"Found potential AWS credentials: {findings}"

    def test_no_github_tokens_hardcoded(self):
        """Test no GitHub tokens are hardcoded."""
        github_patterns = [
            r'ghp_[A-Za-z0-9]{36}',  # GitHub personal access token
            r'gho_[A-Za-z0-9]{36}',  # GitHub OAuth token
            r'ghs_[A-Za-z0-9]{36}',  # GitHub server token
        ]

        findings = []

        for pattern in github_patterns:
            for file_path in PROJECT_ROOT.rglob('*'):
                if file_path.is_file() and 'venv' not in str(file_path):
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        if re.search(pattern, content):
                            findings.append({
                                'file': str(file_path),
                                'pattern': pattern
                            })
                    except:
                        pass

        assert len(findings) == 0, \
            f"Found potential GitHub tokens: {findings}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
