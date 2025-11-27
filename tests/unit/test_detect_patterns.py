#!/usr/bin/env python3
"""
Unit tests for detect-patterns.py
"""

import sys
import yaml
import tempfile
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'skills' / 'project-analyzer' / 'scripts'))

# Import with the correct module name (using hyphen-to-underscore conversion)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "detect_patterns",
    Path(__file__).parent.parent.parent / 'skills' / 'project-analyzer' / 'scripts' / 'detect-patterns.py'
)
detect_patterns = importlib.util.module_from_spec(spec)
spec.loader.exec_module(detect_patterns)
PatternDetector = detect_patterns.PatternDetector


def create_test_patterns_yaml():
    """Create a temporary patterns YAML file for testing."""
    patterns = {
        'patterns': [
            {
                'id': 'test-missing-readme',
                'type': 'file_absence',
                'check': 'README.md',
                'confidence': 'high',
                'severity': 'high',
                'recommendation': {
                    'template': 'documentation/README',
                    'reason': 'Test reason'
                }
            },
            {
                'id': 'test-missing-gitignore',
                'type': 'file_absence',
                'check': '.gitignore',
                'confidence': 'high',
                'severity': 'medium',
                'recommendation': {
                    'template': 'git/gitignore',
                    'reason': 'Test reason'
                }
            },
            {
                'id': 'test-missing-ci',
                'type': 'directory_absence',
                'check': ['.github/workflows', '.gitlab-ci.yml'],
                'confidence': 'high',
                'severity': 'high',
                'recommendation': {
                    'template': 'ci-cd/github-actions',
                    'reason': 'Test reason'
                }
            }
        ],
        'scoring': {
            'high': {'weight': 1.0},
            'medium': {'weight': 0.7},
            'low': {'weight': 0.4}
        },
        'severity': {
            'high': {'priority': 1},
            'medium': {'priority': 2},
            'low': {'priority': 3}
        }
    }

    tmpfile = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
    yaml.dump(patterns, tmpfile)
    tmpfile.close()
    return tmpfile.name


def test_pattern_detector_initialization():
    """Test PatternDetector initialization."""
    patterns_file = create_test_patterns_yaml()

    try:
        detector = PatternDetector(patterns_file)
        assert len(detector.patterns) == 3
        assert detector.patterns[0]['id'] == 'test-missing-readme'
    finally:
        Path(patterns_file).unlink()


def test_detect_missing_readme():
    """Test detection of missing README.md."""
    patterns_file = create_test_patterns_yaml()

    try:
        detector = PatternDetector(patterns_file)

        # Project structure without README
        project_structure = {
            'project_name': 'test-project',
            'project_types': [],
            'frameworks': [],
            'files': ['.gitignore', 'package.json'],
            'directories': []
        }

        results = detector.detect(project_structure)

        # Should detect missing README
        readme_detection = next(
            (d for d in results['detections'] if d['id'] == 'test-missing-readme'),
            None
        )
        assert readme_detection is not None
        assert readme_detection['issue_found'] == True
        assert readme_detection['severity'] == 'high'
    finally:
        Path(patterns_file).unlink()


def test_detect_existing_readme():
    """Test that existing README is not flagged."""
    patterns_file = create_test_patterns_yaml()

    try:
        detector = PatternDetector(patterns_file)

        # Project structure WITH README
        project_structure = {
            'project_name': 'test-project',
            'project_types': [],
            'frameworks': [],
            'files': ['README.md', '.gitignore', 'package.json'],
            'directories': []
        }

        results = detector.detect(project_structure)

        # Should NOT detect missing README
        readme_detection = next(
            (d for d in results['detections'] if d['id'] == 'test-missing-readme'),
            None
        )
        assert readme_detection is not None
        assert readme_detection['issue_found'] == False
    finally:
        Path(patterns_file).unlink()


def test_detect_missing_ci_directory():
    """Test detection of missing CI/CD configuration."""
    patterns_file = create_test_patterns_yaml()

    try:
        detector = PatternDetector(patterns_file)

        # Project structure without CI
        project_structure = {
            'project_name': 'test-project',
            'project_types': [],
            'frameworks': [],
            'files': ['README.md'],
            'directories': ['src', 'tests']
        }

        results = detector.detect(project_structure)

        # Should detect missing CI
        ci_detection = next(
            (d for d in results['detections'] if d['id'] == 'test-missing-ci'),
            None
        )
        assert ci_detection is not None
        assert ci_detection['issue_found'] == True
    finally:
        Path(patterns_file).unlink()


def test_recommendation_generation():
    """Test that recommendations are generated correctly."""
    patterns_file = create_test_patterns_yaml()

    try:
        detector = PatternDetector(patterns_file)

        # Project missing README and .gitignore
        project_structure = {
            'project_name': 'test-project',
            'project_types': [],
            'frameworks': [],
            'files': ['package.json'],
            'directories': []
        }

        results = detector.detect(project_structure)

        # Should have 2 recommendations
        assert len(results['recommendations']) == 3  # README, gitignore, CI

        # Check that recommendations are sorted by priority
        assert results['recommendations'][0]['severity'] == 'high'
    finally:
        Path(patterns_file).unlink()


def test_priority_score_calculation():
    """Test priority score calculation."""
    patterns_file = create_test_patterns_yaml()

    try:
        detector = PatternDetector(patterns_file)

        # Create detection with high severity and high confidence
        detection = {
            'confidence': 'high',
            'severity': 'high'
        }

        priority = detector._calculate_priority(detection)

        # High confidence (1.0) × high multiplier (1.0) × high priority (10) = 10.0
        assert priority == 10.0

        # Create detection with medium severity and medium confidence
        detection = {
            'confidence': 'medium',
            'severity': 'medium'
        }

        priority = detector._calculate_priority(detection)

        # Medium confidence (0.7) × medium multiplier (0.6) × medium priority (5) = 2.1
        assert priority == 2.1
    finally:
        Path(patterns_file).unlink()


def test_summary_statistics():
    """Test that summary statistics are calculated correctly."""
    patterns_file = create_test_patterns_yaml()

    try:
        detector = PatternDetector(patterns_file)

        # Project missing README (high severity) and .gitignore (medium severity)
        project_structure = {
            'project_name': 'test-project',
            'project_types': [],
            'frameworks': [],
            'files': ['package.json'],
            'directories': []
        }

        results = detector.detect(project_structure)
        summary = results['summary']

        assert summary['total_patterns'] == 3
        assert summary['issues_found'] == 3
        assert summary['high_severity'] == 2  # README and CI
        assert summary['medium_severity'] == 1  # .gitignore
    finally:
        Path(patterns_file).unlink()


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
