#!/usr/bin/env python3
"""
Integration tests for event hook configuration

Tests hooks.json structure, hook definitions, and command path validation.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import pytest


PROJECT_ROOT = Path(__file__).parent.parent.parent
HOOKS_DIR = PROJECT_ROOT / 'hooks'
HOOKS_FILE = HOOKS_DIR / 'hooks.json'
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'


class TestHooksFile:
    """Test hooks.json file existence and structure."""

    def test_hooks_directory_exists(self):
        """Verify hooks directory exists."""
        assert HOOKS_DIR.exists(), "Hooks directory should exist"
        assert HOOKS_DIR.is_dir(), "Hooks path should be a directory"

    def test_hooks_json_exists(self):
        """Verify hooks.json exists."""
        assert HOOKS_FILE.exists(), f"hooks.json should exist at {HOOKS_FILE}"

    def test_hooks_json_valid(self):
        """Test hooks.json is valid JSON."""
        try:
            with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert data is not None, "hooks.json should contain data"
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in hooks.json: {e}")

    def test_hooks_json_structure(self):
        """Test hooks.json has required top-level structure."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert 'hooks' in data, "hooks.json should have 'hooks' key"
        assert isinstance(data['hooks'], dict), "'hooks' should be a dictionary"


class TestHookTypes:
    """Test different hook types are properly defined."""

    @pytest.fixture
    def hooks_data(self) -> Dict[str, Any]:
        """Load hooks.json data."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_sessionstart_hook_defined(self, hooks_data):
        """Test SessionStart hook is defined."""
        hooks = hooks_data.get('hooks', {})
        assert 'SessionStart' in hooks, "SessionStart hook should be defined"

    def test_posttooluse_hook_defined(self, hooks_data):
        """Test PostToolUse hook is defined."""
        hooks = hooks_data.get('hooks', {})
        assert 'PostToolUse' in hooks, "PostToolUse hook should be defined"

    def test_precommit_hook_defined(self, hooks_data):
        """Test PreCommit hook is defined."""
        hooks = hooks_data.get('hooks', {})
        assert 'PreCommit' in hooks, "PreCommit hook should be defined"

    def test_hook_types_are_lists(self, hooks_data):
        """Test all hook types contain lists of configurations."""
        hooks = hooks_data.get('hooks', {})

        for hook_type, hook_configs in hooks.items():
            assert isinstance(hook_configs, list), \
                f"{hook_type} should be a list of hook configurations"


class TestSessionStartHook:
    """Test SessionStart hook configuration."""

    @pytest.fixture
    def sessionstart_hooks(self) -> List[Dict[str, Any]]:
        """Get SessionStart hook configurations."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('hooks', {}).get('SessionStart', [])

    def test_sessionstart_has_matcher(self, sessionstart_hooks):
        """Test SessionStart hooks have matcher field."""
        for hook_config in sessionstart_hooks:
            assert 'matcher' in hook_config, \
                "SessionStart hook should have 'matcher' field"

    def test_sessionstart_has_hooks_list(self, sessionstart_hooks):
        """Test SessionStart hooks have hooks list."""
        for hook_config in sessionstart_hooks:
            assert 'hooks' in hook_config, \
                "SessionStart hook should have 'hooks' list"
            assert isinstance(hook_config['hooks'], list), \
                "hooks should be a list"

    def test_sessionstart_check_analyzed_configured(self, sessionstart_hooks):
        """Test SessionStart includes check-analyzed.sh."""
        has_check_analyzed = False

        for hook_config in sessionstart_hooks:
            for hook in hook_config.get('hooks', []):
                command = hook.get('command', '')
                if 'check-analyzed.sh' in command:
                    has_check_analyzed = True
                    break

        assert has_check_analyzed, \
            "SessionStart should include check-analyzed.sh hook"


class TestPostToolUseHook:
    """Test PostToolUse hook configuration."""

    @pytest.fixture
    def posttooluse_hooks(self) -> List[Dict[str, Any]]:
        """Get PostToolUse hook configurations."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('hooks', {}).get('PostToolUse', [])

    def test_posttooluse_has_matcher(self, posttooluse_hooks):
        """Test PostToolUse hooks have matcher field."""
        for hook_config in posttooluse_hooks:
            assert 'matcher' in hook_config, \
                "PostToolUse hook should have 'matcher' field"

    def test_posttooluse_write_validation(self, posttooluse_hooks):
        """Test PostToolUse includes Write tool validation."""
        has_write_matcher = False

        for hook_config in posttooluse_hooks:
            if hook_config.get('matcher') == 'Write':
                has_write_matcher = True
                # Should validate templates
                for hook in hook_config.get('hooks', []):
                    command = hook.get('command', '')
                    if 'validate-template.sh' in command:
                        return  # Found it!

        if has_write_matcher:
            pytest.fail("Write matcher exists but missing validate-template.sh")


class TestPreCommitHook:
    """Test PreCommit hook configuration."""

    @pytest.fixture
    def precommit_hooks(self) -> List[Dict[str, Any]]:
        """Get PreCommit hook configurations."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('hooks', {}).get('PreCommit', [])

    def test_precommit_has_matcher(self, precommit_hooks):
        """Test PreCommit hooks have matcher field."""
        for hook_config in precommit_hooks:
            assert 'matcher' in hook_config, \
                "PreCommit hook should have 'matcher' field"

    def test_precommit_isolation_validation(self, precommit_hooks):
        """Test PreCommit includes isolation validation."""
        has_isolation_check = False

        for hook_config in precommit_hooks:
            for hook in hook_config.get('hooks', []):
                command = hook.get('command', '')
                if 'validate-isolation.sh' in command:
                    has_isolation_check = True
                    break

        assert has_isolation_check, \
            "PreCommit should include validate-isolation.sh hook"


class TestHookCommands:
    """Test hook command configurations."""

    @pytest.fixture
    def all_hooks(self) -> List[Dict[str, Any]]:
        """Get all hook configurations."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        all_hooks = []
        for hook_type, hook_configs in data.get('hooks', {}).items():
            for hook_config in hook_configs:
                for hook in hook_config.get('hooks', []):
                    all_hooks.append({
                        'type': hook_type,
                        'matcher': hook_config.get('matcher'),
                        'hook': hook
                    })
        return all_hooks

    def test_hooks_have_type(self, all_hooks):
        """Test all hooks have type field."""
        for hook_info in all_hooks:
            hook = hook_info['hook']
            assert 'type' in hook, "Hook should have 'type' field"

    def test_hooks_have_command(self, all_hooks):
        """Test command-type hooks have command field."""
        for hook_info in all_hooks:
            hook = hook_info['hook']
            if hook.get('type') == 'command':
                assert 'command' in hook, \
                    "Command-type hook should have 'command' field"

    def test_hooks_have_description(self, all_hooks):
        """Test all hooks have description field."""
        for hook_info in all_hooks:
            hook = hook_info['hook']
            assert 'description' in hook, \
                "Hook should have 'description' field"
            assert len(hook['description']) > 0, \
                "Description should not be empty"


class TestHookCommandPaths:
    """Test that hook command paths are valid."""

    @pytest.fixture
    def all_commands(self) -> List[str]:
        """Extract all command paths from hooks."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        commands = []
        for hook_type, hook_configs in data.get('hooks', {}).items():
            for hook_config in hook_configs:
                for hook in hook_config.get('hooks', []):
                    if hook.get('type') == 'command':
                        commands.append(hook.get('command', ''))
        return commands

    def test_hook_commands_use_variables(self, all_commands):
        """Test hook commands use proper variable substitution."""
        for command in all_commands:
            if command:
                # Should use ${CLAUDE_PLUGIN_ROOT} for plugin scripts
                assert '${CLAUDE_PLUGIN_ROOT}' in command, \
                    f"Command should use ${{CLAUDE_PLUGIN_ROOT}}: {command}"

    def test_hook_commands_reference_valid_scripts(self, all_commands):
        """Test hook commands reference existing scripts."""
        for command in all_commands:
            if not command:
                continue

            # Extract script name (last part after /)
            parts = command.split('/')
            script_name = parts[-1]

            # Remove any variable references
            if script_name.startswith('${'):
                continue

            # Verify script exists
            script_path = SCRIPTS_DIR / script_name
            assert script_path.exists(), \
                f"Referenced script should exist: {script_name} at {script_path}"

    def test_no_hardcoded_absolute_paths(self, all_commands):
        """Test commands don't use hardcoded absolute paths."""
        for command in all_commands:
            if not command:
                continue

            # Should not start with / or C:\ (absolute paths)
            assert not command.startswith('/'), \
                f"Command should not use absolute path: {command}"
            assert not (len(command) > 2 and command[1] == ':'), \
                f"Command should not use Windows absolute path: {command}"


class TestHookArguments:
    """Test hook argument configurations."""

    @pytest.fixture
    def hooks_with_args(self) -> List[Dict[str, Any]]:
        """Get hooks that use arguments."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        hooks_with_args = []
        for hook_type, hook_configs in data.get('hooks', {}).items():
            for hook_config in hook_configs:
                for hook in hook_config.get('hooks', []):
                    if 'args' in hook:
                        hooks_with_args.append({
                            'type': hook_type,
                            'hook': hook
                        })
        return hooks_with_args

    def test_args_are_lists(self, hooks_with_args):
        """Test args field is a list."""
        for hook_info in hooks_with_args:
            hook = hook_info['hook']
            assert isinstance(hook['args'], list), \
                "Hook args should be a list"

    def test_args_use_valid_variables(self, hooks_with_args):
        """Test args use valid Claude Code variables."""
        valid_vars = {
            '${FILE_PATH}',
            '${CLAUDE_PROJECT_DIR}',
            '${CLAUDE_PLUGIN_ROOT}',
        }

        for hook_info in hooks_with_args:
            hook = hook_info['hook']
            for arg in hook.get('args', []):
                # If arg contains a variable, it should be a valid one
                if '${' in arg:
                    # Extract variable
                    import re
                    vars_in_arg = re.findall(r'\$\{[A-Z_]+\}', arg)
                    for var in vars_in_arg:
                        assert var in valid_vars, \
                            f"Invalid variable in args: {var}. Valid: {valid_vars}"


class TestHookMatchers:
    """Test hook matcher configurations."""

    @pytest.fixture
    def all_matchers(self) -> List[str]:
        """Get all matcher patterns."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        matchers = []
        for hook_type, hook_configs in data.get('hooks', {}).items():
            for hook_config in hook_configs:
                matchers.append(hook_config.get('matcher', ''))
        return matchers

    def test_matchers_not_empty(self, all_matchers):
        """Test matchers are not empty strings."""
        for matcher in all_matchers:
            assert matcher, "Matcher should not be empty"

    def test_matchers_valid_patterns(self, all_matchers):
        """Test matchers use valid pattern syntax."""
        for matcher in all_matchers:
            # Should be either '**' (wildcard) or a specific tool name
            assert matcher == '**' or matcher.isalpha(), \
                f"Matcher should be '**' or tool name: {matcher}"


class TestHookConsistency:
    """Test consistency across hook configurations."""

    def test_all_command_hooks_have_required_fields(self):
        """Test all command hooks have required fields."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        required_fields = ['type', 'command', 'description']

        for hook_type, hook_configs in data.get('hooks', {}).items():
            for hook_config in hook_configs:
                for hook in hook_config.get('hooks', []):
                    if hook.get('type') == 'command':
                        for field in required_fields:
                            assert field in hook, \
                                f"Command hook missing {field} in {hook_type}"

    def test_hook_descriptions_meaningful(self):
        """Test hook descriptions are meaningful."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for hook_type, hook_configs in data.get('hooks', {}).items():
            for hook_config in hook_configs:
                for hook in hook_config.get('hooks', []):
                    description = hook.get('description', '')
                    assert len(description) > 10, \
                        f"Hook description too short in {hook_type}: {description}"


class TestHookIntegration:
    """Test hook integration with project structure."""

    def test_hooks_reference_existing_scripts(self):
        """Test all hook script references are valid."""
        with open(HOOKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        expected_scripts = []
        for hook_type, hook_configs in data.get('hooks', {}).items():
            for hook_config in hook_configs:
                for hook in hook_config.get('hooks', []):
                    command = hook.get('command', '')
                    if command and '.sh' in command:
                        # Extract script name
                        parts = command.split('/')
                        script_name = parts[-1]
                        expected_scripts.append(script_name)

        # Verify scripts exist
        for script_name in expected_scripts:
            script_path = SCRIPTS_DIR / script_name
            assert script_path.exists(), \
                f"Hook references non-existent script: {script_name}"

    def test_hooks_directory_structure(self):
        """Test hooks directory has expected structure."""
        # Should only contain hooks.json
        hook_files = list(HOOKS_DIR.glob('*'))
        assert len(hook_files) >= 1, "Hooks directory should contain hooks.json"

        # hooks.json should be present
        assert HOOKS_FILE in hook_files, "hooks.json should exist"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
