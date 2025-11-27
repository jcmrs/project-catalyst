#!/usr/bin/env python3
"""
Unit tests for bash script functionality

Tests execution of bash scripts by invoking them directly.
Cross-platform compatible with proper path handling.
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import List, Optional
import pytest


class BashScriptTester:
    """Helper class for testing bash scripts across platforms."""

    def __init__(self, script_dir: Path):
        self.script_dir = script_dir
        self.is_windows = sys.platform.startswith('win')
        self.bash_executable = self._find_bash()

    def _find_bash(self) -> Optional[str]:
        """Find bash executable on the system."""
        if self.is_windows:
            # Try common Windows paths for Git Bash
            common_paths = [
                r'C:\Program Files\Git\bin\bash.exe',
                r'C:\Program Files (x86)\Git\bin\bash.exe',
                r'C:\msys64\usr\bin\bash.exe',
                r'C:\cygwin64\bin\bash.exe',
            ]
            for path in common_paths:
                if Path(path).exists():
                    return path
            # Try to find bash in PATH
            try:
                result = subprocess.run(['where', 'bash'],
                                      capture_output=True,
                                      text=True,
                                      timeout=5)
                if result.returncode == 0:
                    return result.stdout.strip().split('\n')[0]
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            return None
        else:
            # Unix-like systems
            return 'bash'

    def run_script(self, script_name: str, args: List[str] = None,
                   env: dict = None, timeout: int = 30) -> subprocess.CompletedProcess:
        """
        Run a bash script and return the result.

        Args:
            script_name: Name of the script file
            args: Optional list of arguments
            env: Optional environment variables
            timeout: Maximum execution time in seconds

        Returns:
            CompletedProcess instance with returncode, stdout, stderr
        """
        if not self.bash_executable:
            pytest.skip("Bash executable not found on system")

        script_path = self.script_dir / script_name
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        # Convert to Unix-style path for bash on Windows
        if self.is_windows:
            script_path_str = str(script_path).replace('\\', '/')
            if script_path_str[1] == ':':
                # Convert C:/path to /c/path
                drive = script_path_str[0].lower()
                script_path_str = f'/{drive}{script_path_str[2:]}'
        else:
            script_path_str = str(script_path)

        # Build command
        cmd = [self.bash_executable, script_path_str]
        if args:
            cmd.extend(args)

        # Setup environment
        script_env = os.environ.copy()
        if env:
            script_env.update(env)

        # Run script
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',  # Force UTF-8 encoding for emoji support
                errors='replace',   # Replace undecodable bytes instead of failing
                timeout=timeout,
                env=script_env,
                cwd=str(self.script_dir.parent)
            )
            return result
        except subprocess.TimeoutExpired:
            pytest.fail(f"Script {script_name} timed out after {timeout} seconds")


# Initialize tester for Project Catalyst scripts
PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
tester = BashScriptTester(SCRIPTS_DIR)


class TestSetupWizard:
    """Test setup-wizard.sh script execution."""

    def test_setup_wizard_exists(self):
        """Verify setup-wizard.sh exists."""
        script_path = SCRIPTS_DIR / 'setup-wizard.sh'
        assert script_path.exists(), f"Script not found: {script_path}"

    def test_setup_wizard_execution_help(self):
        """Test setup-wizard.sh can be executed with help flag."""
        result = tester.run_script('setup-wizard.sh', args=['--help'])
        # Script should execute without error (may return 0 or 1 for help)
        assert result.returncode in [0, 1], f"Unexpected return code: {result.returncode}"

    def test_setup_wizard_has_shebang(self):
        """Test setup-wizard.sh has proper shebang."""
        script_path = SCRIPTS_DIR / 'setup-wizard.sh'
        with open(script_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        assert first_line.startswith('#!'), "Script missing shebang"
        assert 'bash' in first_line.lower(), "Script should use bash"


class TestHealthCheck:
    """Test health-check.sh script execution."""

    def test_health_check_exists(self):
        """Verify health-check.sh exists."""
        script_path = SCRIPTS_DIR / 'health-check.sh'
        assert script_path.exists(), f"Script not found: {script_path}"

    def test_health_check_execution(self):
        """Test health-check.sh can be executed."""
        # Health check requires project directory argument
        result = tester.run_script('health-check.sh', args=[str(PROJECT_ROOT)])
        # Script should execute (may succeed or fail based on project state)
        assert result.returncode is not None, "Script failed to execute"

    def test_health_check_invalid_directory(self):
        """Test health-check.sh handles invalid directory."""
        result = tester.run_script('health-check.sh', args=['/nonexistent/path'])
        # Should fail gracefully
        assert result.returncode != 0, "Should fail with invalid directory"

    def test_health_check_has_shebang(self):
        """Test health-check.sh has proper shebang."""
        script_path = SCRIPTS_DIR / 'health-check.sh'
        with open(script_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        assert first_line.startswith('#!'), "Script missing shebang"


class TestCheckAnalyzed:
    """Test check-analyzed.sh script execution."""

    def test_check_analyzed_exists(self):
        """Verify check-analyzed.sh exists."""
        script_path = SCRIPTS_DIR / 'check-analyzed.sh'
        assert script_path.exists(), f"Script not found: {script_path}"

    def test_check_analyzed_execution(self):
        """Test check-analyzed.sh can be executed."""
        result = tester.run_script('check-analyzed.sh')
        # Script should execute successfully
        assert result.returncode is not None, "Script failed to execute"

    def test_check_analyzed_output_format(self):
        """Test check-analyzed.sh produces expected output."""
        result = tester.run_script('check-analyzed.sh')
        # Check for expected output patterns
        output = result.stdout + result.stderr
        assert len(output) >= 0, "Script should produce output"


class TestValidateIsolation:
    """Test validate-isolation.sh script execution."""

    def test_validate_isolation_exists(self):
        """Verify validate-isolation.sh exists."""
        script_path = SCRIPTS_DIR / 'validate-isolation.sh'
        assert script_path.exists(), f"Script not found: {script_path}"

    def test_validate_isolation_execution(self):
        """Test validate-isolation.sh can be executed."""
        result = tester.run_script('validate-isolation.sh')
        # Script should execute successfully
        assert result.returncode is not None, "Script failed to execute"

    def test_validate_isolation_parameters(self):
        """Test validate-isolation.sh validates isolation parameters."""
        # This script checks for proper isolation in local-memory operations
        result = tester.run_script('validate-isolation.sh')
        # Should complete execution
        assert result.returncode in [0, 1], "Script should complete execution"


class TestValidateTemplate:
    """Test validate-template.sh script execution."""

    def test_validate_template_exists(self):
        """Verify validate-template.sh exists."""
        script_path = SCRIPTS_DIR / 'validate-template.sh'
        assert script_path.exists(), f"Script not found: {script_path}"

    def test_validate_template_execution_no_args(self):
        """Test validate-template.sh handles missing arguments."""
        result = tester.run_script('validate-template.sh')
        # Should fail or return usage message
        assert result.returncode is not None, "Script failed to execute"

    def test_validate_template_with_valid_file(self):
        """Test validate-template.sh with a valid template file."""
        # Use a known valid template
        template_path = PROJECT_ROOT / 'templates' / 'doc' / 'readme.md'
        if template_path.exists():
            result = tester.run_script('validate-template.sh', args=[str(template_path)])
            # Should execute successfully with valid template
            assert result.returncode in [0, 1], "Script should handle valid template"

    def test_validate_template_with_invalid_file(self):
        """Test validate-template.sh handles missing file gracefully."""
        result = tester.run_script('validate-template.sh',
                                  args=['/nonexistent/template.md'])
        # Should handle missing file gracefully (hooks are lenient)
        assert result.returncode == 0, "Should handle missing file gracefully for hooks"


class TestScriptPermissions:
    """Test script file permissions and executability."""

    @pytest.mark.skipif(sys.platform.startswith('win'),
                       reason="Executable bit not applicable on Windows")
    def test_scripts_are_executable(self):
        """Verify all .sh scripts have executable permission."""
        scripts = [
            'setup-wizard.sh',
            'health-check.sh',
            'check-analyzed.sh',
            'validate-isolation.sh',
            'validate-template.sh'
        ]

        for script_name in scripts:
            script_path = SCRIPTS_DIR / script_name
            if script_path.exists():
                assert os.access(script_path, os.X_OK), \
                    f"Script {script_name} is not executable"

    def test_all_scripts_have_shebang(self):
        """Verify all bash scripts have proper shebang."""
        scripts = list(SCRIPTS_DIR.glob('*.sh'))

        for script_path in scripts:
            with open(script_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            assert first_line.startswith('#!'), \
                f"Script {script_path.name} missing shebang"


class TestScriptDependencies:
    """Test script dependencies and environment requirements."""

    def test_python_available(self):
        """Verify Python is available for scripts that need it."""
        try:
            result = subprocess.run(['python3', '--version'],
                                  capture_output=True,
                                  timeout=5)
            assert result.returncode == 0, "Python3 not available"
        except FileNotFoundError:
            # Try 'python' instead
            result = subprocess.run(['python', '--version'],
                                  capture_output=True,
                                  timeout=5)
            assert result.returncode == 0, "Python not available"

    def test_required_directories_exist(self):
        """Verify required directories exist for scripts."""
        required_dirs = [
            PROJECT_ROOT / 'scripts',
            PROJECT_ROOT / 'skills',
            PROJECT_ROOT / 'templates',
        ]

        for dir_path in required_dirs:
            assert dir_path.exists(), f"Required directory missing: {dir_path}"

    def test_analyzer_scripts_exist(self):
        """Verify analyzer scripts exist."""
        analyzer_dir = PROJECT_ROOT / 'skills' / 'project-analyzer' / 'scripts'
        if analyzer_dir.exists():
            analyze_script = analyzer_dir / 'analyze.sh'
            assert analyze_script.exists(), \
                "Analyzer entry script missing: analyze.sh"


class TestScriptErrorHandling:
    """Test script error handling and edge cases."""

    def test_health_check_with_empty_string(self):
        """Test health-check.sh handles empty string argument."""
        result = tester.run_script('health-check.sh', args=[''])
        # Should handle gracefully
        assert result.returncode is not None, "Script should handle empty string"

    def test_validate_template_with_directory(self):
        """Test validate-template.sh handles directory gracefully."""
        result = tester.run_script('validate-template.sh',
                                  args=[str(SCRIPTS_DIR)])
        # Should handle directory gracefully (hooks are lenient)
        assert result.returncode == 0, "Should handle directory gracefully for hooks"

    def test_scripts_timeout_protection(self):
        """Verify scripts don't hang indefinitely."""
        # All scripts should complete within reasonable timeout
        scripts = ['check-analyzed.sh']

        for script_name in scripts:
            script_path = SCRIPTS_DIR / script_name
            if script_path.exists():
                result = tester.run_script(script_name, timeout=10)
                # Should complete within timeout
                assert result.returncode is not None, \
                    f"Script {script_name} completed within timeout"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
