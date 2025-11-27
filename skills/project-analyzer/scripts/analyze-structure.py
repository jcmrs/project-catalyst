#!/usr/bin/env python3
"""
analyze-structure.py - Scan project structure and detect project type

Purpose: Analyze project directory to identify files, detect project type,
         and gather metadata for pattern detection.

Usage: python analyze-structure.py [project-path]
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

class ProjectAnalyzer:
    """Analyzes project structure and detects project type."""

    # Project type detection patterns
    PROJECT_INDICATORS = {
        'node': ['package.json', 'package-lock.json', 'node_modules/'],
        'python': ['requirements.txt', 'setup.py', 'pyproject.toml', '__pycache__/'],
        'java': ['pom.xml', 'build.gradle', 'build.gradle.kts', 'gradlew'],
        'rust': ['Cargo.toml', 'Cargo.lock', 'target/'],
        'go': ['go.mod', 'go.sum'],
        'ruby': ['Gemfile', 'Gemfile.lock'],
        'php': ['composer.json', 'composer.lock'],
        'csharp': ['*.csproj', '*.sln'],
    }

    # Framework detection patterns (from dependencies/imports)
    FRAMEWORK_INDICATORS = {
        'react': ['react', '@types/react'],
        'vue': ['vue', '@vue/'],
        'angular': ['@angular/'],
        'express': ['express'],
        'django': ['django', 'Django'],
        'flask': ['flask', 'Flask'],
        'spring': ['spring-boot', 'org.springframework'],
        'laravel': ['laravel/framework'],
    }

    def __init__(self, project_path: str):
        """Initialize analyzer with project path."""
        self.project_path = Path(project_path).resolve()
        self.project_name = self.project_path.name

        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {self.project_path}")

        if not self.project_path.is_dir():
            raise NotADirectoryError(f"Project path is not a directory: {self.project_path}")

    def scan_structure(self) -> Dict:
        """Scan project structure and return metadata."""
        structure = {
            'project_name': self.project_name,
            'project_path': str(self.project_path),
            'files': [],
            'directories': [],
            'file_count': 0,
            'directory_count': 0,
            'project_types': [],
            'frameworks': [],
            'has_git': False,
            'has_ci': False,
            'has_tests': False,
        }

        # Scan files and directories
        for root, dirs, files in os.walk(self.project_path):
            # Skip hidden directories and common exclusions
            dirs[:] = [d for d in dirs if not self._should_skip(d)]

            rel_root = Path(root).relative_to(self.project_path)

            for dir_name in dirs:
                rel_path = rel_root / dir_name
                structure['directories'].append(str(rel_path))
                structure['directory_count'] += 1

            for file_name in files:
                if not self._should_skip(file_name):
                    rel_path = rel_root / file_name
                    structure['files'].append(str(rel_path))
                    structure['file_count'] += 1

        # Detect project types
        structure['project_types'] = self._detect_project_types(structure['files'], structure['directories'])

        # Detect frameworks
        structure['frameworks'] = self._detect_frameworks()

        # Check for Git
        structure['has_git'] = (self.project_path / '.git').exists()

        # Check for CI/CD
        structure['has_ci'] = self._check_ci_setup(structure['files'], structure['directories'])

        # Check for tests
        structure['has_tests'] = self._check_test_setup(structure['directories'])

        return structure

    def _should_skip(self, name: str) -> bool:
        """Check if file/directory should be skipped."""
        skip_patterns = [
            'node_modules', '__pycache__', '.git', '.venv', 'venv',
            'target', 'dist', 'build', '.next', '.nuxt',
            '*.pyc', '*.class', '*.o', '*.so'
        ]

        for pattern in skip_patterns:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern or name.startswith(pattern):
                return True

        return False

    def _detect_project_types(self, files: List[str], directories: List[str]) -> List[str]:
        """Detect project type(s) based on indicator files."""
        detected_types = []
        all_paths = files + directories

        for project_type, indicators in self.PROJECT_INDICATORS.items():
            for indicator in indicators:
                if indicator.endswith('/'):
                    # Directory indicator
                    if any(d.startswith(indicator[:-1]) for d in directories):
                        detected_types.append(project_type)
                        break
                elif indicator.startswith('*'):
                    # Pattern indicator
                    pattern = indicator[1:]
                    if any(f.endswith(pattern) for f in files):
                        detected_types.append(project_type)
                        break
                else:
                    # Exact file indicator
                    if indicator in files or any(f.endswith(indicator) for f in files):
                        detected_types.append(project_type)
                        break

        return detected_types

    def _detect_frameworks(self) -> List[str]:
        """Detect frameworks from package files."""
        frameworks = []

        # Check Node.js package.json
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    dependencies = {**data.get('dependencies', {}), **data.get('devDependencies', {})}

                    for framework, indicators in self.FRAMEWORK_INDICATORS.items():
                        for indicator in indicators:
                            if any(indicator in dep for dep in dependencies.keys()):
                                frameworks.append(framework)
                                break
            except (json.JSONDecodeError, IOError):
                pass

        # Check Python requirements.txt
        requirements_txt = self.project_path / 'requirements.txt'
        if requirements_txt.exists():
            try:
                with open(requirements_txt, 'r', encoding='utf-8') as f:
                    content = f.read()

                    for framework, indicators in self.FRAMEWORK_INDICATORS.items():
                        for indicator in indicators:
                            if indicator in content:
                                frameworks.append(framework)
                                break
            except IOError:
                pass

        return list(set(frameworks))  # Remove duplicates

    def _check_ci_setup(self, files: List[str], directories: List[str]) -> bool:
        """Check if CI/CD is configured."""
        ci_indicators = [
            '.github/workflows',
            '.gitlab-ci.yml',
            '.circleci/config.yml',
            'azure-pipelines.yml',
            'Jenkinsfile',
        ]

        for indicator in ci_indicators:
            if indicator.endswith('.yml') or indicator.endswith('file'):
                if indicator in files or any(f.endswith(indicator) for f in files):
                    return True
            else:
                if any(d.startswith(indicator) for d in directories):
                    return True

        return False

    def _check_test_setup(self, directories: List[str]) -> bool:
        """Check if tests are set up."""
        test_indicators = ['test', 'tests', 'spec', '__tests__']

        return any(
            any(indicator in d.lower() for indicator in test_indicators)
            for d in directories
        )

    def get_project_info(self) -> Dict:
        """Get high-level project information."""
        structure = self.scan_structure()

        info = {
            'name': self.project_name,
            'path': str(self.project_path),
            'type': structure['project_types'][0] if structure['project_types'] else 'unknown',
            'types': structure['project_types'],
            'frameworks': structure['frameworks'],
            'stats': {
                'files': structure['file_count'],
                'directories': structure['directory_count'],
            },
            'setup': {
                'git': structure['has_git'],
                'ci': structure['has_ci'],
                'tests': structure['has_tests'],
            }
        }

        return info


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        project_path = os.getcwd()
    else:
        project_path = sys.argv[1]

    try:
        analyzer = ProjectAnalyzer(project_path)
        structure = analyzer.scan_structure()

        # Output as JSON
        print(json.dumps(structure, indent=2))

        return 0

    except Exception as e:
        print(f"Error analyzing project: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
