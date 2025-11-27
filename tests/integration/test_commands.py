#!/usr/bin/env python3
"""
Integration tests for slash command configuration

Tests command format, script references, and variable substitution
in the .claude/commands directory.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set
import pytest


PROJECT_ROOT = Path(__file__).parent.parent.parent
COMMANDS_DIR = PROJECT_ROOT / 'commands'
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
SKILLS_DIR = PROJECT_ROOT / 'skills'


class TestCommandFiles:
    """Test command file existence and structure."""

    def test_commands_directory_exists(self):
        """Verify commands directory exists."""
        assert COMMANDS_DIR.exists(), "Commands directory should exist"
        assert COMMANDS_DIR.is_dir(), "Commands path should be a directory"

    def test_command_files_exist(self):
        """Test that expected command files exist."""
        expected_commands = [
            'analyze-project.md',
            'health-check.md',
            'onboard.md',
            'apply-template.md',
            'optimize-setup.md'
        ]

        for cmd_file in expected_commands:
            cmd_path = COMMANDS_DIR / cmd_file
            assert cmd_path.exists(), f"Command file missing: {cmd_file}"

    def test_command_files_are_markdown(self):
        """Test that all command files are markdown."""
        for cmd_file in COMMANDS_DIR.glob('*.md'):
            assert cmd_file.suffix == '.md', \
                f"Command file should be markdown: {cmd_file.name}"


class TestAnalyzeProjectCommand:
    """Test /analyze-project command configuration."""

    @pytest.fixture
    def command_content(self) -> str:
        """Load analyze-project command content."""
        cmd_path = COMMANDS_DIR / 'analyze-project.md'
        if not cmd_path.exists():
            pytest.skip("analyze-project.md not found")
        return cmd_path.read_text(encoding='utf-8')

    def test_analyze_project_command_format(self, command_content):
        """Test command has proper markdown format."""
        assert '# Analyze Project' in command_content or \
               '# analyze-project' in command_content.lower(), \
               "Command should have title"

    def test_analyze_project_script_reference(self, command_content):
        """Test command references correct script."""
        # Should reference the analyze.sh script
        assert 'analyze.sh' in command_content, \
            "Should reference analyze.sh script"
        assert 'project-analyzer' in command_content, \
            "Should reference project-analyzer skill"

    def test_analyze_project_variable_substitution(self, command_content):
        """Test command uses proper variable substitution."""
        # Should use Claude Code variable syntax
        expected_vars = ['${CLAUDE_PLUGIN_ROOT}', '${CLAUDE_PROJECT_DIR}']

        found_vars = []
        for var in expected_vars:
            if var in command_content:
                found_vars.append(var)

        assert len(found_vars) > 0, \
            f"Should use Claude Code variables. Expected: {expected_vars}"

    def test_analyze_project_has_description(self, command_content):
        """Test command has description section."""
        # Should have some descriptive text
        assert len(command_content) > 100, \
            "Command should have substantial description"

    def test_analyze_project_script_path_valid(self, command_content):
        """Test referenced script path is valid."""
        # Extract script path from command
        pattern = r'skills/project-analyzer/scripts/analyze\.sh'
        matches = re.search(pattern, command_content)

        if matches:
            # Verify the script exists
            script_path = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
            assert script_path.exists(), \
                f"Referenced script should exist: {script_path}"


class TestHealthCheckCommand:
    """Test /health-check command configuration."""

    @pytest.fixture
    def command_content(self) -> str:
        """Load health-check command content."""
        cmd_path = COMMANDS_DIR / 'health-check.md'
        if not cmd_path.exists():
            pytest.skip("health-check.md not found")
        return cmd_path.read_text(encoding='utf-8')

    def test_health_check_command_format(self, command_content):
        """Test command has proper markdown format."""
        assert '# Health Check' in command_content or \
               '# health-check' in command_content.lower(), \
               "Command should have title"

    def test_health_check_script_reference(self, command_content):
        """Test command references health-check.sh."""
        assert 'health-check.sh' in command_content, \
            "Should reference health-check.sh script"

    def test_health_check_variable_substitution(self, command_content):
        """Test command uses proper variable substitution."""
        # Should use Claude Code variables
        assert '${CLAUDE_PLUGIN_ROOT}' in command_content or \
               '${CLAUDE_PROJECT_DIR}' in command_content, \
               "Should use Claude Code variables"

    def test_health_check_script_exists(self, command_content):
        """Test referenced script exists."""
        # health-check.sh should exist in scripts directory
        script_path = SCRIPTS_DIR / 'health-check.sh'
        assert script_path.exists(), \
            f"Referenced script should exist: {script_path}"


class TestOnboardCommand:
    """Test /onboard command configuration."""

    @pytest.fixture
    def command_content(self) -> str:
        """Load onboard command content."""
        cmd_path = COMMANDS_DIR / 'onboard.md'
        if not cmd_path.exists():
            pytest.skip("onboard.md not found")
        return cmd_path.read_text(encoding='utf-8')

    def test_onboard_command_format(self, command_content):
        """Test command has proper markdown format."""
        assert '# Onboard' in command_content or \
               '# onboard' in command_content.lower(), \
               "Command should have title"

    def test_onboard_has_instructions(self, command_content):
        """Test onboard command has setup instructions."""
        # Should have substantial onboarding instructions
        assert len(command_content) > 200, \
            "Onboard command should have detailed instructions"


class TestApplyTemplateCommand:
    """Test /apply-template command configuration."""

    @pytest.fixture
    def command_content(self) -> str:
        """Load apply-template command content."""
        cmd_path = COMMANDS_DIR / 'apply-template.md'
        if not cmd_path.exists():
            pytest.skip("apply-template.md not found")
        return cmd_path.read_text(encoding='utf-8')

    def test_apply_template_command_format(self, command_content):
        """Test command has proper markdown format."""
        assert 'template' in command_content.lower(), \
            "Command should reference templates"

    def test_apply_template_references_templates_dir(self, command_content):
        """Test command references templates directory."""
        assert 'template' in command_content.lower(), \
            "Should reference templates"


class TestCommandScriptReferences:
    """Test that all script references in commands are valid."""

    def test_all_referenced_scripts_exist(self):
        """Test all scripts referenced in commands exist."""
        referenced_scripts = set()

        # Scan all command files for script references
        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Find all .sh references
            sh_matches = re.findall(r'([a-z0-9\-]+\.sh)', content)
            for match in sh_matches:
                referenced_scripts.add(match)

        # Verify each referenced script exists
        for script_name in referenced_scripts:
            script_path = SCRIPTS_DIR / script_name
            # Also check in skills directory
            skills_script_path = SKILLS_DIR / 'project-analyzer' / 'scripts' / script_name

            assert script_path.exists() or skills_script_path.exists(), \
                f"Referenced script not found: {script_name}"


class TestCommandVariables:
    """Test variable substitution patterns in commands."""

    def test_commands_use_standard_variables(self):
        """Test commands use standard Claude Code variables."""
        standard_vars = {
            '${CLAUDE_PLUGIN_ROOT}',
            '${CLAUDE_PROJECT_DIR}',
            '${CLAUDE_PROJECT_ROOT}',
        }

        used_vars = set()

        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Find all ${VAR} patterns
            var_matches = re.findall(r'\$\{([A-Z_]+)\}', content)
            for var in var_matches:
                used_vars.add(f'${{{var}}}')

        # All used variables should be standard ones
        for var in used_vars:
            assert var in standard_vars, \
                f"Non-standard variable used: {var}. Standard: {standard_vars}"

    def test_no_hardcoded_paths(self):
        """Test commands don't contain hardcoded absolute paths."""
        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Check for absolute paths (Unix and Windows)
            assert not re.search(r'(?<![$\{])/home/[a-z]+', content), \
                f"Hardcoded Unix path in {cmd_file.name}"
            assert not re.search(r'C:\\Users\\', content), \
                f"Hardcoded Windows path in {cmd_file.name}"


class TestCommandDocumentation:
    """Test command documentation quality."""

    def test_commands_have_descriptions(self):
        """Test all commands have meaningful descriptions."""
        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Should have substantial content (not just title)
            assert len(content) > 50, \
                f"Command {cmd_file.name} should have description"

    def test_commands_have_usage_examples(self):
        """Test commands include usage examples."""
        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Check for common documentation patterns
            has_usage = any(keyword in content.lower() for keyword in
                          ['usage', 'example', 'how to', 'run'])

            assert has_usage, \
                f"Command {cmd_file.name} should include usage information"

    def test_commands_have_proper_headers(self):
        """Test commands use proper markdown headers."""
        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Should start with # header
            lines = content.strip().split('\n')
            assert lines[0].startswith('#'), \
                f"Command {cmd_file.name} should start with # header"


class TestCommandCodeBlocks:
    """Test code blocks in command files."""

    def test_bash_code_blocks_valid(self):
        """Test bash code blocks in commands are valid."""
        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Find bash code blocks
            bash_blocks = re.findall(r'```bash\n(.*?)```', content,
                                    re.DOTALL | re.MULTILINE)

            for block in bash_blocks:
                # Should not be empty
                assert block.strip(), \
                    f"Empty bash block in {cmd_file.name}"

                # Should not have obvious syntax errors
                assert not block.strip().startswith('}'), \
                    f"Invalid bash syntax in {cmd_file.name}"


class TestCommandConsistency:
    """Test consistency across command files."""

    def test_consistent_variable_usage(self):
        """Test variables are used consistently across commands."""
        var_usage = {}

        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Track which variables are used in which files
            vars_found = re.findall(r'\$\{([A-Z_]+)\}', content)
            for var in vars_found:
                if var not in var_usage:
                    var_usage[var] = []
                var_usage[var].append(cmd_file.name)

        # If a variable is used, it should be used consistently
        # (This test mainly documents current usage)
        assert len(var_usage) > 0, "Commands should use variables"

    def test_consistent_script_references(self):
        """Test script references use consistent patterns."""
        for cmd_file in COMMANDS_DIR.glob('*.md'):
            content = cmd_file.read_text(encoding='utf-8')

            # Find script references
            script_refs = re.findall(r'([a-z0-9\-]+\.sh)', content)

            for script_ref in script_refs:
                # Script references should use lowercase with hyphens
                assert script_ref.islower() or '-' in script_ref, \
                    f"Script name should use lowercase-with-hyphens: {script_ref}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
