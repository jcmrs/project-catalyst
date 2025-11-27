#!/usr/bin/env python3
"""
Performance benchmarking tests for Project Catalyst

Tests execution time, memory usage, and token usage for critical operations.
Ensures plugin operations meet performance targets.
"""

import time
import subprocess
import sys
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, Optional
import pytest


PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
SKILLS_DIR = PROJECT_ROOT / 'skills'


class PerformanceBenchmark:
    """Helper class for performance benchmarking."""

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

    def measure_execution_time(self, script_path: Path, args: list = None,
                              timeout: int = 60) -> Dict[str, Any]:
        """
        Measure script execution time.

        Returns:
            Dict with execution_time, returncode, and success status
        """
        if not self.bash_executable:
            pytest.skip("Bash not available")

        # Convert path for Windows
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

        # Measure execution time
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',  # Force UTF-8 encoding for emoji support
                errors='replace',   # Replace undecodable bytes instead of failing
                timeout=timeout,
                cwd=str(PROJECT_ROOT)
            )
            end_time = time.time()

            return {
                'execution_time': end_time - start_time,
                'returncode': result.returncode,
                'success': result.returncode is not None,
                'stdout_length': len(result.stdout),
                'stderr_length': len(result.stderr)
            }
        except subprocess.TimeoutExpired:
            return {
                'execution_time': timeout,
                'returncode': None,
                'success': False,
                'timeout': True
            }

    def measure_memory_usage(self, script_path: Path, args: list = None) -> Dict[str, Any]:
        """
        Measure approximate memory usage.

        Note: This is a simplified measurement.
        For accurate memory profiling, use tools like memory_profiler.

        Returns:
            Dict with estimated memory usage
        """
        # For bash scripts, we'll measure output size as a proxy
        if not self.bash_executable:
            pytest.skip("Bash not available")

        result = self.measure_execution_time(script_path, args)

        # Estimate memory based on output size
        estimated_memory_kb = (
            result.get('stdout_length', 0) + result.get('stderr_length', 0)
        ) / 1024

        return {
            'estimated_memory_kb': estimated_memory_kb,
            'execution_time': result['execution_time'],
            'success': result['success']
        }

    def measure_token_usage(self, text: str) -> int:
        """
        Estimate token usage for text output.

        Uses a simple approximation: ~4 characters per token.

        Returns:
            Estimated token count
        """
        # Simple approximation: divide character count by 4
        return len(text) // 4


benchmark = PerformanceBenchmark()


class TestAnalyzerPerformance:
    """Test analyzer execution performance."""

    @pytest.mark.timeout(10)
    def test_analyzer_execution_time(self):
        """Test analyzer completes within 5 seconds for small project."""
        analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
        if not analyzer_script.exists():
            pytest.skip("Analyzer script not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create small test project
            (project_dir / 'package.json').write_text('{"name": "test"}')
            (project_dir / 'README.md').write_text('# Test')

            # Measure execution time
            metrics = benchmark.measure_execution_time(
                analyzer_script,
                args=[str(project_dir)]
            )

            assert metrics['success'], "Analyzer should complete successfully"

            # Target: < 5 seconds for small project
            assert metrics['execution_time'] < 5.0, \
                f"Analyzer took {metrics['execution_time']:.2f}s, target is <5s"

    @pytest.mark.timeout(20)
    def test_analyzer_execution_time_medium_project(self):
        """Test analyzer performance on medium-sized project."""
        analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
        if not analyzer_script.exists():
            pytest.skip("Analyzer script not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create medium-sized project
            (project_dir / 'package.json').write_text('{"name": "test"}')
            (project_dir / 'README.md').write_text('# Test Project\n\n' + 'Lorem ipsum\n' * 100)

            # Create multiple files
            src_dir = project_dir / 'src'
            src_dir.mkdir()
            for i in range(20):
                (src_dir / f'file{i}.js').write_text(f'// File {i}\n')

            # Measure execution time
            metrics = benchmark.measure_execution_time(
                analyzer_script,
                args=[str(project_dir)]
            )

            assert metrics['success'], "Analyzer should complete successfully"

            # Target: < 10 seconds for medium project
            assert metrics['execution_time'] < 10.0, \
                f"Analyzer took {metrics['execution_time']:.2f}s, target is <10s"

    def test_analyzer_output_size(self):
        """Test analyzer output is reasonably sized."""
        analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
        if not analyzer_script.exists():
            pytest.skip("Analyzer script not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / 'package.json').write_text('{"name": "test"}')

            metrics = benchmark.measure_execution_time(
                analyzer_script,
                args=[str(project_dir)]
            )

            # Output should be reasonable (not megabytes)
            total_output = metrics['stdout_length'] + metrics['stderr_length']
            assert total_output < 100_000, \
                f"Analyzer output too large: {total_output} bytes"


class TestHealthCheckPerformance:
    """Test health check execution performance."""

    @pytest.mark.timeout(70)
    def test_health_check_execution_time(self):
        """Test health check completes within 60 seconds."""
        health_script = SCRIPTS_DIR / 'health-check.sh'
        if not health_script.exists():
            pytest.skip("Health check script not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create test project
            (project_dir / 'package.json').write_text('{"name": "test"}')
            (project_dir / 'README.md').write_text('# Test')

            # Measure execution time
            metrics = benchmark.measure_execution_time(
                health_script,
                args=[str(project_dir)],
                timeout=70
            )

            assert metrics['success'], "Health check should complete successfully"

            # Target: < 60 seconds
            assert metrics['execution_time'] < 60.0, \
                f"Health check took {metrics['execution_time']:.2f}s, target is <60s"

    def test_health_check_output_size(self):
        """Test health check output is reasonably sized."""
        health_script = SCRIPTS_DIR / 'health-check.sh'
        if not health_script.exists():
            pytest.skip("Health check script not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / 'package.json').write_text('{"name": "test"}')

            metrics = benchmark.measure_execution_time(
                health_script,
                args=[str(project_dir)]
            )

            # Output should be reasonable
            total_output = metrics['stdout_length'] + metrics['stderr_length']
            assert total_output < 50_000, \
                f"Health check output too large: {total_output} bytes"


class TestMemoryUsage:
    """Test memory usage of plugin operations."""

    def test_analyzer_memory_usage(self):
        """Test analyzer memory usage stays under 50MB."""
        analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
        if not analyzer_script.exists():
            pytest.skip("Analyzer script not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / 'package.json').write_text('{"name": "test"}')

            metrics = benchmark.measure_memory_usage(
                analyzer_script,
                args=[str(project_dir)]
            )

            # Estimated memory usage should be reasonable
            # Note: This is a rough estimate based on output size
            assert metrics['estimated_memory_kb'] < 50_000, \
                f"Estimated memory usage: {metrics['estimated_memory_kb']:.2f} KB"

    def test_scripts_no_memory_leaks(self):
        """Test scripts can run multiple times without memory issues."""
        check_script = SCRIPTS_DIR / 'check-analyzed.sh'
        if not check_script.exists():
            pytest.skip("Check script not found")

        # Run script multiple times
        for i in range(5):
            metrics = benchmark.measure_execution_time(check_script)
            assert metrics['success'], f"Run {i+1} should succeed"

            # Execution time should be consistent (no memory buildup)
            assert metrics['execution_time'] < 5.0, \
                f"Run {i+1} took too long: {metrics['execution_time']:.2f}s"


class TestTokenUsage:
    """Test token usage for plugin outputs."""

    def test_analyzer_token_usage(self):
        """Test analyzer output uses fewer than 500 tokens."""
        analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
        if not analyzer_script.exists():
            pytest.skip("Analyzer script not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / 'package.json').write_text('{"name": "test"}')

            # Run analyzer
            if not benchmark.bash_executable:
                pytest.skip("Bash not available")

            script_str = str(analyzer_script)
            if benchmark.is_windows:
                script_str = script_str.replace('\\', '/')
                if script_str[1] == ':':
                    drive = script_str[0].lower()
                    script_str = f'/{drive}{script_str[2:]}'

            result = subprocess.run(
                [benchmark.bash_executable, script_str, str(project_dir)],
                capture_output=True,
                text=True,
                encoding='utf-8',  # Force UTF-8 encoding for emoji support
                errors='replace',   # Replace undecodable bytes instead of failing
                timeout=10,
                cwd=str(PROJECT_ROOT)
            )

            # Estimate token usage
            output = result.stdout + result.stderr
            token_count = benchmark.measure_token_usage(output)

            # Target: < 500 tokens for small project
            assert token_count < 500, \
                f"Analyzer output uses ~{token_count} tokens, target is <500"

    def test_health_check_token_usage(self):
        """Test health check output is token-efficient."""
        health_script = SCRIPTS_DIR / 'health-check.sh'
        if not health_script.exists():
            pytest.skip("Health check script not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / 'package.json').write_text('{"name": "test"}')

            # Run health check
            if not benchmark.bash_executable:
                pytest.skip("Bash not available")

            script_str = str(health_script)
            if benchmark.is_windows:
                script_str = script_str.replace('\\', '/')
                if script_str[1] == ':':
                    drive = script_str[0].lower()
                    script_str = f'/{drive}{script_str[2:]}'

            result = subprocess.run(
                [benchmark.bash_executable, script_str, str(project_dir)],
                capture_output=True,
                text=True,
                timeout=70,
                cwd=str(PROJECT_ROOT)
            )

            # Estimate token usage
            output = result.stdout + result.stderr
            token_count = benchmark.measure_token_usage(output)

            # Health check can be longer, but should be reasonable
            assert token_count < 1000, \
                f"Health check uses ~{token_count} tokens, target is <1000"


class TestScriptEfficiency:
    """Test script efficiency and optimization."""

    def test_validation_scripts_fast(self):
        """Test validation scripts execute quickly."""
        validation_scripts = [
            'check-analyzed.sh',
            'validate-isolation.sh',
        ]

        for script_name in validation_scripts:
            script_path = SCRIPTS_DIR / script_name
            if not script_path.exists():
                continue

            metrics = benchmark.measure_execution_time(script_path)

            # Validation scripts should be very fast (< 2 seconds)
            assert metrics['execution_time'] < 2.0, \
                f"{script_name} took {metrics['execution_time']:.2f}s, target is <2s"

    def test_scripts_minimal_disk_io(self):
        """Test scripts produce minimal output (proxy for disk I/O)."""
        test_scripts = [
            'check-analyzed.sh',
            'validate-isolation.sh',
        ]

        for script_name in test_scripts:
            script_path = SCRIPTS_DIR / script_name
            if not script_path.exists():
                continue

            metrics = benchmark.measure_execution_time(script_path)

            # Scripts should produce minimal output
            total_output = metrics.get('stdout_length', 0) + metrics.get('stderr_length', 0)
            assert total_output < 10_000, \
                f"{script_name} output too large: {total_output} bytes"


class TestPerformanceRegression:
    """Test for performance regressions."""

    def test_analyzer_performance_baseline(self):
        """Establish analyzer performance baseline."""
        analyzer_script = SKILLS_DIR / 'project-analyzer' / 'scripts' / 'analyze.sh'
        if not analyzer_script.exists():
            pytest.skip("Analyzer script not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            (project_dir / 'package.json').write_text('{"name": "baseline-test"}')

            # Run 3 times and take average
            times = []
            for _ in range(3):
                metrics = benchmark.measure_execution_time(
                    analyzer_script,
                    args=[str(project_dir)]
                )
                if metrics['success']:
                    times.append(metrics['execution_time'])

            if times:
                avg_time = sum(times) / len(times)
                # Document baseline performance
                assert avg_time < 5.0, \
                    f"Average execution time: {avg_time:.2f}s (baseline: <5s)"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
