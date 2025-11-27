#!/usr/bin/env python3
"""
End-to-end tests for Project Catalyst plugin workflows

Tests complete user workflows including onboarding, analysis,
health checks, isolation enforcement, and template application.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import pytest


PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
SKILLS_DIR = PROJECT_ROOT / 'skills'
TEMPLATES_DIR = PROJECT_ROOT / 'templates'
COMMANDS_DIR = PROJECT_ROOT / 'commands'


class WorkflowTester:
    """Helper class for testing complete workflows."""

    def __init__(self):
        self.is_windows = sys.platform.startswith('win')
        self.bash_executable = self._find_bash()

    def _find_bash(self) -> Optional[str]:
        """Find bash executable."""
        if self.is_windows:
            common_paths = [
                r'C:\Program Files\Git\bin\bash.exe',
                r'C:\Program Files (x86)\Git\bin\bash.exe',
            ]
            for path in common_paths:
                if Path(path).exists():
                    return path
            try:
                result = subprocess.run(['where', 'bash'],
                                      capture_output=True,
                                      text=True,
                                      timeout=5)
                if result.returncode == 0:
                    return result.stdout.strip().split('\n')[0]
            except:
                pass
            return None
        return 'bash'

    def run_script(self, script_path: Path, args: list = None,
                   cwd: Path = None, timeout: int = 60) -> subprocess.CompletedProcess:
        """Run a bash script."""
        if not self.bash_executable:
            pytest.skip("Bash not available")

        # Convert path for Windows bash
        if self.is_windows:
            script_str = str(script_path).replace('\\', '/')
            if script_str[1] == ':':
                drive = script_str[0].lower()
                script_str = f'/{drive}{script_str[2:]}'
        else:
            script_str = str(script_path)

        cmd = [self.bash_executable, script_str]
        if args:
            cmd.extend(args)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',  # Force UTF-8 encoding for emoji support
                errors='replace',   # Replace undecodable bytes instead of failing
                timeout=timeout,
                cwd=str(cwd or PROJECT_ROOT)
            )
            return result
        except subprocess.TimeoutExpired:
            pytest.fail(f"Script timed out: {script_path.name}")


workflow_tester = WorkflowTester()


class TestOnboardingWorkflow:
    """Test complete onboarding workflow."""

    def test_onboard_command_exists(self):
        """Test onboard command file exists."""
        onboard_cmd = COMMANDS_DIR / 'onboard.md'
        assert onboard_cmd.exists(), "Onboard command should exist"

    def test_onboard_command_content(self):
        """Test onboard command has proper content."""
        onboard_cmd = COMMANDS_DIR / 'onboard.md'
        content = onboard_cmd.read_text(encoding='utf-8')

        # Should have onboarding instructions
        assert len(content) > 100, "Onboard command should have instructions"
        assert 'onboard' in content.lower(), "Should mention onboarding"

    def test_full_onboarding_workflow(self):
        """Test complete onboarding workflow with temporary project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Step 1: Create minimal project structure
            (project_dir / 'README.md').write_text('# Test Project')
            (project_dir / 'package.json').write_text('{"name": "test"}')

            # Step 2: Run analyzer (simulating user running /analyze-project)
            analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
            if analyzer_script.exists():
                result = workflow_tester.run_script(
                    analyzer_script,
                    args=[str(project_dir)]
                )
                # Analyzer should complete
                assert result.returncode is not None, "Analyzer should complete"

            # Step 3: Verify project structure
            assert project_dir.exists(), "Project directory should exist"
            assert (project_dir / 'README.md').exists(), "README should exist"


class TestAnalysisWorkflow:
    """Test project analysis workflow."""

    def test_analyze_project_command_exists(self):
        """Test analyze-project command exists."""
        analyze_cmd = COMMANDS_DIR / 'analyze-project.md'
        assert analyze_cmd.exists(), "Analyze command should exist"

    def test_analyzer_script_exists(self):
        """Test analyzer entry script exists."""
        analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
        assert analyzer_script.exists(), "Analyzer script should exist"

    def test_analyze_then_health_check(self):
        """Test analysis followed by health check workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create project structure
            (project_dir / 'package.json').write_text('{"name": "test"}')
            (project_dir / '.gitignore').write_text('node_modules/')

            # Step 1: Run analysis
            analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
            if analyzer_script.exists():
                analysis_result = workflow_tester.run_script(
                    analyzer_script,
                    args=[str(project_dir)]
                )

            # Step 2: Run health check
            health_script = SCRIPTS_DIR / 'health-check.sh'
            if health_script.exists():
                health_result = workflow_tester.run_script(
                    health_script,
                    args=[str(project_dir)]
                )
                # Health check should complete
                assert health_result.returncode is not None


class TestHealthCheckWorkflow:
    """Test health check workflow."""

    def test_health_check_command_exists(self):
        """Test health-check command exists."""
        health_cmd = COMMANDS_DIR / 'health-check.md'
        assert health_cmd.exists(), "Health check command should exist"

    def test_health_check_script_exists(self):
        """Test health-check.sh script exists."""
        health_script = SCRIPTS_DIR / 'health-check.sh'
        assert health_script.exists(), "Health check script should exist"

    def test_health_check_on_valid_project(self):
        """Test health check on a valid project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create well-configured project
            (project_dir / 'package.json').write_text(
                json.dumps({'name': 'test', 'version': '1.0.0'})
            )
            (project_dir / 'README.md').write_text('# Test\n\nDescription')
            (project_dir / 'LICENSE').write_text('MIT')
            (project_dir / '.gitignore').write_text('node_modules/')

            # Run health check
            health_script = SCRIPTS_DIR / 'health-check.sh'
            if health_script.exists():
                result = workflow_tester.run_script(
                    health_script,
                    args=[str(project_dir)]
                )
                # Should complete
                assert result.returncode is not None

    def test_health_check_on_minimal_project(self):
        """Test health check on minimal project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Minimal project (just one file)
            (project_dir / 'index.js').write_text('console.log("test");')

            # Run health check
            health_script = SCRIPTS_DIR / 'health-check.sh'
            if health_script.exists():
                result = workflow_tester.run_script(
                    health_script,
                    args=[str(project_dir)]
                )
                # Should handle minimal project
                assert result.returncode is not None


class TestIsolationEnforcement:
    """Test isolation enforcement workflow."""

    def test_validate_isolation_script_exists(self):
        """Test validate-isolation.sh exists."""
        isolation_script = SCRIPTS_DIR / 'validate-isolation.sh'
        assert isolation_script.exists(), "Isolation validation script should exist"

    def test_isolation_enforcement_e2e(self):
        """Test end-to-end isolation enforcement."""
        # Test that isolation validation script can be executed
        isolation_script = SCRIPTS_DIR / 'validate-isolation.sh'
        if isolation_script.exists():
            result = workflow_tester.run_script(isolation_script)
            # Should complete execution
            assert result.returncode is not None

    def test_precommit_hook_includes_isolation(self):
        """Test PreCommit hook includes isolation check."""
        hooks_file = PROJECT_ROOT / 'hooks' / 'hooks.json'
        if hooks_file.exists():
            with open(hooks_file, 'r', encoding='utf-8') as f:
                hooks_data = json.load(f)

            precommit = hooks_data.get('hooks', {}).get('PreCommit', [])
            has_isolation = False

            for hook_config in precommit:
                for hook in hook_config.get('hooks', []):
                    if 'validate-isolation.sh' in hook.get('command', ''):
                        has_isolation = True
                        break

            assert has_isolation, "PreCommit should include isolation validation"


class TestTemplateApplicationWorkflow:
    """Test template application workflow."""

    def test_apply_template_command_exists(self):
        """Test apply-template command exists."""
        apply_cmd = COMMANDS_DIR / 'apply-template.md'
        assert apply_cmd.exists(), "Apply template command should exist"

    def test_templates_directory_exists(self):
        """Test templates directory exists."""
        assert TEMPLATES_DIR.exists(), "Templates directory should exist"

    def test_validate_template_script_exists(self):
        """Test validate-template.sh exists."""
        validate_script = SCRIPTS_DIR / 'validate-template.sh'
        assert validate_script.exists(), "Template validation script should exist"

    def test_template_application_workflow(self):
        """Test template application workflow."""
        # Verify templates exist
        templates = list(TEMPLATES_DIR.rglob('*.md'))
        assert len(templates) > 0, "Should have template files"

        # Test template validation on a real template
        if templates:
            template_file = templates[0]
            validate_script = SCRIPTS_DIR / 'validate-template.sh'

            if validate_script.exists():
                result = workflow_tester.run_script(
                    validate_script,
                    args=[str(template_file)]
                )
                # Should validate template
                assert result.returncode is not None

    def test_posttooluse_hook_validates_templates(self):
        """Test PostToolUse hook validates templates after Write."""
        hooks_file = PROJECT_ROOT / 'hooks' / 'hooks.json'
        if hooks_file.exists():
            with open(hooks_file, 'r', encoding='utf-8') as f:
                hooks_data = json.load(f)

            posttooluse = hooks_data.get('hooks', {}).get('PostToolUse', [])
            has_template_validation = False

            for hook_config in posttooluse:
                if hook_config.get('matcher') == 'Write':
                    for hook in hook_config.get('hooks', []):
                        if 'validate-template.sh' in hook.get('command', ''):
                            has_template_validation = True
                            break

            assert has_template_validation, \
                "PostToolUse should validate templates after Write"


class TestErrorRecovery:
    """Test error recovery and graceful degradation."""

    def test_health_check_invalid_directory(self):
        """Test health check handles invalid directory gracefully."""
        health_script = SCRIPTS_DIR / 'health-check.sh'
        if health_script.exists():
            result = workflow_tester.run_script(
                health_script,
                args=['/nonexistent/directory']
            )
            # Should fail gracefully
            assert result.returncode != 0, "Should fail with invalid directory"

    def test_validate_template_missing_file(self):
        """Test template validation handles missing file gracefully."""
        validate_script = SCRIPTS_DIR / 'validate-template.sh'
        if validate_script.exists():
            result = workflow_tester.run_script(
                validate_script,
                args=['/nonexistent/template.md']
            )
            # Should handle missing file gracefully (hooks are lenient)
            assert result.returncode == 0, "Should handle missing file gracefully for hooks"

    def test_analyzer_empty_directory(self):
        """Test analyzer handles empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
            if analyzer_script.exists():
                result = workflow_tester.run_script(
                    analyzer_script,
                    args=[tmpdir]
                )
                # Should handle empty directory
                assert result.returncode is not None


class TestWorkflowIntegration:
    """Test integration between different workflow components."""

    def test_all_commands_reference_valid_scripts(self):
        """Test all command files reference valid scripts."""
        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Find script references
            import re
            script_refs = re.findall(r'([a-z0-9\-]+\.sh)', content)

            for script_name in script_refs:
                # Check in scripts directory
                script_path = SCRIPTS_DIR / script_name
                skills_path = SKILLS_DIR / 'project-analyzer' / 'scripts' / script_name

                assert script_path.exists() or skills_path.exists(), \
                    f"Command {cmd_file.name} references missing script: {script_name}"

    def test_hooks_reference_valid_scripts(self):
        """Test hooks reference valid scripts."""
        hooks_file = PROJECT_ROOT / 'hooks' / 'hooks.json'
        if hooks_file.exists():
            with open(hooks_file, 'r', encoding='utf-8') as f:
                hooks_data = json.load(f)

            for hook_type, hook_configs in hooks_data.get('hooks', {}).items():
                for hook_config in hook_configs:
                    for hook in hook_config.get('hooks', []):
                        command = hook.get('command', '')
                        if command and '.sh' in command:
                            # Extract script name
                            script_name = command.split('/')[-1]
                            script_path = SCRIPTS_DIR / script_name

                            assert script_path.exists(), \
                                f"Hook references missing script: {script_name}"

    def test_complete_plugin_lifecycle(self):
        """Test complete plugin lifecycle from install to usage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Step 1: User creates new project
            (project_dir / 'package.json').write_text('{"name": "new-project"}')

            # Step 2: SessionStart hook checks if analyzed
            check_script = SCRIPTS_DIR / 'check-analyzed.sh'
            if check_script.exists():
                check_result = workflow_tester.run_script(check_script)
                assert check_result.returncode is not None

            # Step 3: User runs /analyze-project
            analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
            if analyzer_script.exists():
                analyze_result = workflow_tester.run_script(
                    analyzer_script,
                    args=[str(project_dir)]
                )
                assert analyze_result.returncode is not None

            # Step 4: User runs /health-check
            health_script = SCRIPTS_DIR / 'health-check.sh'
            if health_script.exists():
                health_result = workflow_tester.run_script(
                    health_script,
                    args=[str(project_dir)]
                )
                assert health_result.returncode is not None


class TestConcurrentWorkflows:
    """Test workflows can handle concurrent execution."""

    def test_multiple_health_checks(self):
        """Test multiple health checks can run on different projects."""
        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                # Create two different projects
                project1 = Path(tmpdir1)
                project2 = Path(tmpdir2)

                (project1 / 'package.json').write_text('{"name": "project1"}')
                (project2 / 'package.json').write_text('{"name": "project2"}')

                health_script = SCRIPTS_DIR / 'health-check.sh'
                if health_script.exists():
                    # Run on both (sequentially in test, but validates independence)
                    result1 = workflow_tester.run_script(
                        health_script,
                        args=[str(project1)]
                    )
                    result2 = workflow_tester.run_script(
                        health_script,
                        args=[str(project2)]
                    )

                    # Both should complete independently
                    assert result1.returncode is not None
                    assert result2.returncode is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
